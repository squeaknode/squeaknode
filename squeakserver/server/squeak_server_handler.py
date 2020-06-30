import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeakserver.server.buy_offer import BuyOffer
from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.server.lightning_address import LightningAddressHostPort
from squeakserver.server.postgres_db import PostgresDb
from squeakserver.server.util import generate_offer_nonce
from squeakserver.server.util import bxor
from squeakserver.server.util import get_hash


logger = logging.getLogger(__name__)


class SqueakServerHandler(object):
    """Handles server commands.
    """

    def __init__(
            self,
            lightning_host_port: LightningAddressHostPort,
            lightning_client: LNDLightningClient,
            postgres_db: PostgresDb,
            price: int,
    ) -> None:
        self.lightning_host_port = lightning_host_port
        self.lightning_client = lightning_client
        self.postgres_db = postgres_db
        self.price = price

    def handle_posted_squeak(self, squeak):
        logger.info("Handle posted squeak with hash: {}".format(str(get_hash(squeak))))
        # Insert the squeak in the database
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        return

    def handle_get_squeak(self, squeak_hash):
        logger.info("Handle get squeak by hash: {}".format(str(squeak_hash)))
        squeak = self.postgres_db.get_squeak(squeak_hash)
        # Remove the data key before sending response.
        squeak.ClearDataKey()
        return squeak

    def handle_lookup_squeaks(self, addresses, min_block, max_block):
        logger.info("Handle lookup squeaks with addresses: {}, min_block: {}, max_block: {}".format(str(addresses), min_block, max_block))
        hashes = self.postgres_db.lookup_squeaks(addresses, min_block, max_block)
        logger.info("Got number of hashes from db: {}".format(len(hashes)))
        return hashes

    def handle_buy_squeak(self, squeak_hash):
        logger.info("Handle buy squeak by hash: {}".format(str(squeak_hash)))
        # Get the squeak from the database
        squeak = self.postgres_db.get_squeak(squeak_hash)
        # Get the datakey from the squeak
        data_key = squeak.GetDataKey()
        # Generate a new random offer nonce
        nonce = generate_offer_nonce()
        # Get the invoice preimage from the nonce and the squeak data key
        preimage = bxor(nonce, data_key)
        # Get the offer price
        amount = self.price
        # Create the lightning invoice
        add_invoice_response = self.lightning_client.add_invoice(preimage, amount)
        preimage_hash = add_invoice_response.r_hash
        invoice_payment_request = add_invoice_response.payment_request
        # Get the lightning network node pubkey
        get_info_response = self.lightning_client.get_info()
        pubkey = get_info_response.identity_pubkey
        # Return the buy offer
        return BuyOffer(
            squeak_hash,
            nonce,
            amount,
            preimage_hash,
            invoice_payment_request,
            pubkey,
            self.lightning_host_port.host,
            self.lightning_host_port.port,
        )

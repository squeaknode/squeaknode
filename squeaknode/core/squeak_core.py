import logging
import time
from typing import Optional

from squeak.core import CSqueak
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey

from squeaknode.core.buy_offer import BuyOffer
from squeaknode.core.offer import Offer
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import add_tweak
from squeaknode.core.util import generate_tweak
from squeaknode.core.util import get_hash
from squeaknode.core.util import subtract_tweak
from squeaknode.node.received_payments_subscription_client import (
    OpenReceivedPaymentsSubscriptionClient,
)


logger = logging.getLogger(__name__)


class SqueakCore:
    def __init__(
        self,
        blockchain_client,
        lightning_client,
    ):
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client

    def make_squeak(self, signing_profile: SqueakProfile, content_str: str, replyto_hash: Optional[bytes] = None) -> SqueakEntry:
        if signing_profile.private_key is None:
            raise Exception("Can't make squeak with a contact profile.")
        signing_key_str = signing_profile.private_key.decode()
        signing_key = CSigningKey(signing_key_str)
        block_info = self.blockchain_client.get_best_block_info()
        block_height = block_info.block_height
        block_hash = block_info.block_hash
        timestamp = int(time.time())
        if replyto_hash is None or len(replyto_hash) == 0:
            squeak = MakeSqueakFromStr(
                signing_key,
                content_str,
                block_height,
                block_hash,
                timestamp,
            )
        else:
            squeak = MakeSqueakFromStr(
                signing_key,
                content_str,
                block_height,
                block_hash,
                timestamp,
                replyto_hash,
            )
        return SqueakEntry(
            squeak=squeak,
            block_header=block_info.block_header,
        )

    def validate_squeak(self, squeak: CSqueak) -> SqueakEntry:
        block_info = self.blockchain_client.get_block_info_by_height(
            squeak.nBlockHeight)
        if squeak.hashBlock != block_info.block_hash:
            raise Exception("Block hash incorrect.")
        return SqueakEntry(
            squeak=squeak,
            block_header=block_info.block_header,
        )

    def get_best_block_height(self) -> int:
        block_info = self.blockchain_client.get_best_block_info()
        return block_info.block_height

    def create_offer(self, squeak: CSqueak, client_addr: str, price_msat: int) -> SentOffer:
        # Get the squeak hash
        squeak_hash = get_hash(squeak)
        # Generate a new random nonce
        nonce = generate_tweak()
        # Get the squeak secret key
        secret_key = squeak.GetDecryptionKey()
        # Calculate the preimage
        # preimage = bxor(nonce, secret_key)
        preimage = add_tweak(secret_key, nonce)
        # Create the lightning invoice
        add_invoice_response = self.lightning_client.add_invoice(
            preimage, price_msat
        )
        payment_hash = add_invoice_response.r_hash
        invoice_payment_request = add_invoice_response.payment_request
        # invoice_expiry = add_invoice_response.expiry
        lookup_invoice_response = self.lightning_client.lookup_invoice(
            payment_hash.hex()
        )
        invoice_time = lookup_invoice_response.creation_date
        invoice_expiry = lookup_invoice_response.expiry
        # Save the incoming potential payment in the databse.
        return SentOffer(
            sent_offer_id=None,
            squeak_hash=squeak_hash,
            payment_hash=payment_hash.hex(),
            secret_key=preimage.hex(),
            nonce=nonce,
            price_msat=price_msat,
            payment_request=invoice_payment_request,
            invoice_time=invoice_time,
            invoice_expiry=invoice_expiry,
            client_addr=client_addr,
        )

    def create_buy_offer(self, sent_offer: SentOffer, lnd_external_host: str, lnd_port: int) -> BuyOffer:
        # Get the lightning network node pubkey
        get_info_response = self.lightning_client.get_info()
        pubkey = get_info_response.identity_pubkey
        # Return the buy offer
        return BuyOffer(
            squeak_hash=sent_offer.squeak_hash,
            price_msat=sent_offer.price_msat,
            nonce=sent_offer.nonce,
            payment_request=sent_offer.payment_request,
            pubkey=pubkey,
            host=lnd_external_host,
            port=lnd_port,
        )

    def pay_offer(self, offer: Offer) -> SentPayment:
        if offer.offer_id is None:
            raise Exception("Offer must have a non-null offer_id.")
        # Pay the invoice
        payment = self.lightning_client.pay_invoice_sync(offer.payment_request)
        preimage = payment.payment_preimage
        if not preimage:
            raise Exception(
                "Payment failed with error: {}".format(payment.payment_error)
            )

        # Calculate the secret key
        nonce = offer.nonce
        # secret_key = bxor(nonce, preimage)
        secret_key = subtract_tweak(preimage, nonce)
        # Save the preimage of the sent payment
        return SentPayment(
            sent_payment_id=None,
            created=None,
            offer_id=offer.offer_id,
            peer_id=offer.peer_id,
            squeak_hash=offer.squeak_hash,
            payment_hash=offer.payment_hash,
            secret_key=secret_key,
            price_msat=offer.price_msat,
            node_pubkey=offer.destination,
        )

import logging
import time
from typing import Iterator
from typing import Optional

from squeak.core import CSqueak
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey

from squeaknode.core.buy_offer import BuyOffer
from squeaknode.core.offer import Offer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
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
            payment_hash=payment_hash,
            secret_key=preimage,
            nonce=nonce,
            price_msat=price_msat,
            payment_request=invoice_payment_request,
            invoice_time=invoice_time,
            invoice_expiry=invoice_expiry,
            client_addr=client_addr,
        )

    def create_buy_offer(self, sent_offer: SentOffer, lnd_external_host: str, lnd_port: int) -> BuyOffer:
        return BuyOffer(
            squeak_hash=sent_offer.squeak_hash,
            nonce=sent_offer.nonce,
            payment_request=sent_offer.payment_request,
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

    def get_received_payments(self, get_sent_offer_fn, latest_settle_index) -> Iterator[ReceivedPayment]:
        for invoice in self.lightning_client.subscribe_invoices(
                settle_index=latest_settle_index,
        ):
            if invoice.settled:
                payment_hash = invoice.r_hash
                settle_index = invoice.settle_index
                sent_offer = get_sent_offer_fn(payment_hash)
                received_payment = ReceivedPayment(
                    received_payment_id=None,
                    created=None,
                    squeak_hash=sent_offer.squeak_hash,
                    payment_hash=sent_offer.payment_hash,
                    price_msat=sent_offer.price_msat,
                    settle_index=settle_index,
                    client_addr=sent_offer.client_addr,
                )
                yield received_payment

    def get_offer(self, squeak: CSqueak, offer: BuyOffer, peer: SqueakPeer) -> Offer:
        if peer.peer_id is None:
            raise Exception("Peer must have a non-null peer_id.")
        # Get the squeak hash
        squeak_hash = get_hash(squeak)
        # TODO: check if squeak hash matches squeak_hash in buy_offer.
        if squeak_hash != offer.squeak_hash:
            raise Exception("Squeak hash in offer {!r} does not match squeak hash {!r}.".format(
                offer.squeak_hash, squeak_hash
            ))
        # Decode the payment request
        pay_req = self.lightning_client.decode_pay_req(
            offer.payment_request)
        squeak_payment_point = squeak.paymentPoint
        payment_hash = bytes.fromhex(pay_req.payment_hash)
        price_msat = pay_req.num_msat
        destination = pay_req.destination
        invoice_timestamp = pay_req.timestamp
        invoice_expiry = pay_req.expiry
        node_host = offer.host or peer.host
        node_port = offer.port
        decoded_offer = Offer(
            offer_id=None,
            squeak_hash=squeak_hash,
            price_msat=price_msat,
            payment_hash=payment_hash,
            nonce=offer.nonce,
            payment_point=squeak_payment_point,
            invoice_timestamp=invoice_timestamp,
            invoice_expiry=invoice_expiry,
            payment_request=offer.payment_request,
            destination=destination,
            node_host=node_host,
            node_port=node_port,
            peer_id=peer.peer_id,
        )
        # TODO: Check the payment point
        # payment_point = offer.payment_point
        # logger.info("Payment point: {}".format(payment_point.hex()))
        # expected_payment_point = squeak.paymentPoint
        # logger.info("Expected payment point: {}".format(expected_payment_point.hex()))
        # if payment_point != expected_payment_point:
        #     raise Exception(
        #         "Invalid offer payment point: {}, expected: {}".format(
        #             payment_point.hex(),
        #             expected_payment_point.hex(),
        #         )
        #     )
        return decoded_offer

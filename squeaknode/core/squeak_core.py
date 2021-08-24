import logging
import time
from typing import Callable
from typing import Iterator
from typing import NamedTuple
from typing import Optional

import grpc
from bitcoin.core import CBlockHeader
from squeak.core import CheckSqueak
from squeak.core import CSqueak
from squeak.core import MakeSqueakFromStr
from squeak.core.elliptic import payment_point_bytes_from_scalar_bytes
from squeak.core.signing import CSigningKey

from squeaknode.bitcoin.bitcoin_client import BitcoinClient
from squeaknode.bitcoin.util import parse_block_header
from squeaknode.core.exception import InvoiceSubscriptionError
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import add_tweak
from squeaknode.core.util import generate_tweak
from squeaknode.core.util import get_hash
from squeaknode.core.util import subtract_tweak
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient


logger = logging.getLogger(__name__)


class ReceivedPaymentsResult(NamedTuple):
    """Represents the result of a received payment subscription."""
    cancel_fn: Callable[[], None]
    result_stream: Iterator[ReceivedPayment]


class SqueakCore:
    def __init__(
        self,
        bitcoin_client: BitcoinClient,
        lightning_client: LNDLightningClient,
    ):
        self.bitcoin_client = bitcoin_client
        self.lightning_client = lightning_client

    def make_squeak(self, signing_profile: SqueakProfile, content_str: str, replyto_hash: Optional[bytes] = None) -> CSqueak:
        """Create a new squeak.

        Args:
            signing_profile: The profile of the author of the squeak.
            content_str: The content of the squeak as a string.
            replyto_hash: The hash of the squeak to which this one is replying.

        Returns:
            CSqueak: the squeak that was created.

        Raises:
            Exception: If the profile does not have a signing key.
        """
        if signing_profile.private_key is None:
            raise Exception("Can't make squeak with a contact profile.")
        signing_key_str = signing_profile.private_key.decode()
        signing_key = CSigningKey(signing_key_str)
        block_info = self.bitcoin_client.get_best_block_info()
        block_height = block_info.block_height
        block_hash = block_info.block_hash
        timestamp = int(time.time())
        return MakeSqueakFromStr(
            signing_key,
            content_str,
            block_height,
            block_hash,
            timestamp,
            replyto_hash,
        )

    def get_block_header(self, squeak: CSqueak) -> CBlockHeader:
        """Checks if the embedded block hash in the squeak is valid for its
        block height and return the associtated block header.

        Args:
            squeak: The squeak to be validated.

        Returns:
            CBlockHeader: the block header associated with the given squeak.

        Raises:
            Exception: If the block hash is not valid.
        """
        CheckSqueak(squeak, skipDecryptionCheck=True)
        block_info = self.bitcoin_client.get_block_info_by_height(
            squeak.nBlockHeight)
        if squeak.hashBlock != block_info.block_hash:
            raise Exception("Block hash incorrect.")
        return parse_block_header(block_info.block_header)

    def get_decrypted_content(self, squeak: CSqueak, secret_key: bytes) -> str:
        """Checks if the secret key is valid for the given squeak and returns
        the decrypted content.

        Args:
            squeak: The squeak to be validated.
            secret_key: The secret key.

        Returns:
            bytes: the decrypted content

        Raises:
            Exception: If the secret key is not valid.
        """
        squeak.SetDecryptionKey(secret_key)
        CheckSqueak(squeak)
        return squeak.GetDecryptedContentStr()

    def get_best_block_height(self) -> int:
        """Get the current height of the latest block in the blockchain.

        Returns:
            int: the current latest block height.
        """
        block_info = self.bitcoin_client.get_best_block_info()
        return block_info.block_height

    def create_offer(self, squeak: CSqueak, peer_address: PeerAddress, price_msat: int) -> SentOffer:
        """Creates an offer to sell a squeak key to another node.

        Args:
            squeak: The squeak to be sold.
            peer_address: The address of the buyer.
            price_msat: The price in msats.

        Returns:
            SentOffer: A record of the details of the offer for the seller.
        """
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
            peer_address=peer_address,
        )

    def package_offer(self, sent_offer: SentOffer, lnd_external_host: str, lnd_port: int) -> Offer:
        """Package the offer details into a message that will be sent from
        seller to buyer.

        Args:
            sent_offer: The offer that was already generated by the seller.
            lnd_external_host: The host of the lnd node.
            lnd_port: The port of the lnd node.

        Returns:
            SentOffer: A record of the details of the offer for the seller.
        """
        return Offer(
            squeak_hash=sent_offer.squeak_hash,
            nonce=sent_offer.nonce,
            payment_request=sent_offer.payment_request,
            host=lnd_external_host,
            port=lnd_port,
        )

    def unpack_offer(self, squeak: CSqueak, offer: Offer, peer_address: PeerAddress) -> ReceivedOffer:
        """Get the offer details from the message that the buyer
        receives from the seller.

        Args:
            squeak: The squeak that will be unlocked upon payment.
            offer: The offer details received from the seller.
            peer: The peer that sent the offer.

        Returns:
            ReceivedOffer: A record of the details of the offer for the buyer.
        """
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
        lightning_address = LightningAddressHostPort(
            host=offer.host or peer_address.host,
            port=offer.port,
        )
        # TODO: Check the payment point
        # payment_point = offer.payment_point
        # expected_payment_point = squeak.paymentPoint
        # if payment_point != expected_payment_point:
        #     raise Exception("Invalid payment point.")
        return ReceivedOffer(
            received_offer_id=None,
            squeak_hash=squeak_hash,
            price_msat=price_msat,
            payment_hash=payment_hash,
            nonce=offer.nonce,
            payment_point=squeak_payment_point,
            invoice_timestamp=invoice_timestamp,
            invoice_expiry=invoice_expiry,
            payment_request=offer.payment_request,
            destination=destination,
            lightning_address=lightning_address,
            peer_address=peer_address,
        )

    def pay_offer(self, received_offer: ReceivedOffer) -> SentPayment:
        """Pay the offer that the buyer received from the seller.

        Args:
            received_offer: The details of the offer received by the buyer.

        Returns:
            SentPayment: A record of the sent payment.
        """
        # Pay the invoice
        payment = self.lightning_client.pay_invoice_sync(
            received_offer.payment_request)
        preimage = payment.payment_preimage
        if not preimage:
            raise Exception(
                "Payment failed with error: {}".format(payment.payment_error)
            )
        # Calculate the secret key
        nonce = received_offer.nonce
        # secret_key = bxor(nonce, preimage)
        secret_key = subtract_tweak(preimage, nonce)
        # Check if the secret key is valid for the preimage
        point = payment_point_bytes_from_scalar_bytes(secret_key)
        valid = point == received_offer.payment_point
        # Save the preimage of the sent payment
        peer_address = PeerAddress(
            host=received_offer.peer_address.host,
            port=received_offer.peer_address.port,
        )
        return SentPayment(
            sent_payment_id=None,
            created=None,
            peer_address=peer_address,
            squeak_hash=received_offer.squeak_hash,
            payment_hash=received_offer.payment_hash,
            secret_key=secret_key,
            price_msat=received_offer.price_msat,
            node_pubkey=received_offer.destination,
            valid=valid,
        )

    def get_received_payments(
            self,
            latest_settle_index: int,
            get_sent_offer_fn: Callable[[bytes], SentOffer],
    ) -> ReceivedPaymentsResult:
        """Get an iterator of received payments.

        Args:
            latest_settle_index: The latest settle index of the lnd invoice database.
            get_sent_offer_fn: Function that takes a payment hash and returns
                the corresponding SentOffer.

        Returns:
            ReceivedPaymentsResult: An object containing an iterator of received
            payments and a callback function to cancel the iteration.
        """
        # Get the stream of settled invoices.
        invoice_stream = self.lightning_client.subscribe_invoices(
            settle_index=latest_settle_index,
        )

        def cancel_subscription():
            invoice_stream.cancel()

        def get_payment_stream():
            # Yield the received payments.
            try:
                for invoice in invoice_stream:
                    if invoice.settled:
                        payment_hash = invoice.r_hash
                        settle_index = invoice.settle_index
                        sent_offer = get_sent_offer_fn(payment_hash)
                        yield ReceivedPayment(
                            received_payment_id=None,
                            created=None,
                            squeak_hash=sent_offer.squeak_hash,
                            payment_hash=sent_offer.payment_hash,
                            price_msat=sent_offer.price_msat,
                            settle_index=settle_index,
                            peer_address=sent_offer.peer_address,
                        )
            except grpc.RpcError as e:
                if e.code() != grpc.StatusCode.CANCELLED:
                    raise InvoiceSubscriptionError()

        return ReceivedPaymentsResult(
            cancel_fn=cancel_subscription,
            result_stream=get_payment_stream(),
        )

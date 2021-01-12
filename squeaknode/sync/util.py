import logging

from proto import squeak_server_pb2
from squeaknode.core.offer import Offer


logger = logging.getLogger(__name__)


def parse_buy_offer(buy_offer_msg: squeak_server_pb2.SqueakBuyOffer) -> Offer:
    return Offer(
        squeak_hash=buy_offer_msg.squeak_hash,
        nonce=buy_offer_msg.nonce,
        payment_request=buy_offer_msg.payment_request,
        host=buy_offer_msg.host,
        port=buy_offer_msg.port,
    )

import logging

from proto import squeak_server_pb2
from squeaknode.core.buy_offer import BuyOffer


logger = logging.getLogger(__name__)


def parse_buy_offer(buy_offer_msg: squeak_server_pb2.SqueakBuyOffer) -> BuyOffer:
    return BuyOffer(
        squeak_hash=buy_offer_msg.squeak_hash,
        price_msat=0,
        nonce=buy_offer_msg.nonce,
        payment_request=buy_offer_msg.payment_request,
        pubkey="",
        host=buy_offer_msg.host,
        port=buy_offer_msg.port,
    )

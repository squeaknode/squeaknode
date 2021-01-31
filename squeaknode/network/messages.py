import logging

from squeak.core import CheckSqueak
from squeak.core import CSqueak

from proto import squeak_server_pb2
from squeaknode.core.offer import Offer
from squeaknode.core.util import get_hash


logger = logging.getLogger(__name__)


def squeak_to_msg(squeak: CSqueak) -> squeak_server_pb2.Squeak:
    return squeak_server_pb2.Squeak(
        hash=get_hash(squeak),
        serialized_squeak=squeak.serialize(),
    )


def squeak_from_msg(squeak_msg: squeak_server_pb2.Squeak) -> CSqueak:
    squeak = CSqueak.deserialize(squeak_msg.serialized_squeak)
    CheckSqueak(squeak, skipDecryptionCheck=True)
    squeak_hash = get_hash(squeak)
    if squeak_msg.hash != squeak_hash:
        raise Exception("Invalid squeak hash: {}".format(
            squeak_hash
        ))
    return squeak


def offer_from_msg(buy_offer_msg: squeak_server_pb2.Offer) -> Offer:
    return Offer(
        squeak_hash=buy_offer_msg.squeak_hash,
        nonce=buy_offer_msg.nonce,
        payment_request=buy_offer_msg.payment_request,
        host=buy_offer_msg.host,
        port=buy_offer_msg.port,
    )

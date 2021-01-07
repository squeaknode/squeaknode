from typing import NamedTuple

from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_peer import SqueakPeer


class SentPaymentWithPeer(NamedTuple):
    sent_payment: SentPayment
    peer: SqueakPeer

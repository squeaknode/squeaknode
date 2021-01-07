from datetime import datetime
from typing import NamedTuple
from typing import Optional

from squeaknode.core.offer import Offer
from squeaknode.core.squeak_peer import SqueakPeer


class ReceivedPayment(NamedTuple):
    received_payment_id: Optional[int]
    created: Optional[datetime]
    squeak_hash: bytes
    payment_hash: bytes
    price_msat: int
    settle_index: int
    client_addr: str

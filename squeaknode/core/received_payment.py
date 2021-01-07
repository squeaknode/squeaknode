from datetime import datetime
from typing import NamedTuple
from typing import Optional


class ReceivedPayment(NamedTuple):
    received_payment_id: Optional[int]
    created: Optional[datetime]
    squeak_hash: bytes
    payment_hash: bytes
    price_msat: int
    settle_index: int
    client_addr: str

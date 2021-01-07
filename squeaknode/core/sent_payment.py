from datetime import datetime
from typing import NamedTuple
from typing import Optional


class SentPayment(NamedTuple):
    sent_payment_id: Optional[int]
    created: Optional[datetime]
    offer_id: int
    peer_id: int
    squeak_hash: bytes
    payment_hash: bytes
    secret_key: bytes
    price_msat: int
    node_pubkey: bytes

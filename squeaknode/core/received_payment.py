from datetime import datetime
from typing import NamedTuple
from typing import Optional

from squeaknode.core.peer_address import PeerAddress


class ReceivedPayment(NamedTuple):
    """Represents an payment received by a seller."""
    received_payment_id: Optional[int]
    created: Optional[datetime]
    squeak_hash: bytes
    payment_hash: bytes
    price_msat: int
    settle_index: int
    peer_address: PeerAddress

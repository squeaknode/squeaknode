from typing import NamedTuple
from typing import Optional

from squeaknode.core.peer_address import PeerAddress


class ReceivedOffer(NamedTuple):
    """Represents an offer received by a buyer."""
    received_offer_id: Optional[int]
    squeak_hash: bytes
    price_msat: int
    payment_hash: bytes
    nonce: bytes
    payment_point: bytes
    invoice_timestamp: int
    invoice_expiry: int
    payment_request: str
    destination: str
    node_host: str
    node_port: int
    peer_address: PeerAddress

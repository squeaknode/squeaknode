from typing import NamedTuple
from typing import Optional


class Offer(NamedTuple):
    """Class for saving an offer from a remote peer."""
    offer_id: Optional[int]
    squeak_hash: bytes
    price_msat: int
    payment_hash: bytes
    nonce: str
    payment_point: bytes
    invoice_timestamp: int
    invoice_expiry: int
    payment_request: str
    destination: str
    node_host: str
    node_port: int
    peer_id: int

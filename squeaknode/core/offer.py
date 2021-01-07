from typing import NamedTuple
from typing import Optional


class Offer(NamedTuple):
    """Class for saving an offer from a remote peer."""
    offer_id: Optional[int]
    squeak_hash: str
    price_msat: bytes
    payment_hash: str
    nonce: str
    payment_point: str
    invoice_timestamp: int
    invoice_expiry: int
    payment_request: str
    destination: str
    node_host: str
    node_port: int
    peer_id: int

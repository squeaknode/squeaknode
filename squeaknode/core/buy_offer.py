from typing import NamedTuple


class BuyOffer(NamedTuple):
    """Represents the offer details that are sent from seller
    to buyer.
    """
    squeak_hash: bytes
    nonce: bytes
    payment_request: str
    host: str
    port: int

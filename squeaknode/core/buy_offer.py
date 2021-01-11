from typing import NamedTuple


class BuyOffer(NamedTuple):
    """Class for representing a generated offer on a seller node."""
    squeak_hash: bytes
    nonce: bytes
    payment_request: str
    host: str
    port: int

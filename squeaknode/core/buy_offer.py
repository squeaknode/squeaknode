from dataclasses import dataclass


@dataclass
class BuyOffer:
    """Class for representing a generated offer on a seller node."""

    squeak_hash: str
    price_msat: int
    nonce: bytes
    payment_request: str
    pubkey: str
    host: str
    port: int

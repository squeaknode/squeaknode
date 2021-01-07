from typing import NamedTuple
from typing import Optional

from squeaknode.core.offer import Offer
from squeaknode.core.squeak_peer import SqueakPeer


class SentOffer(NamedTuple):
    sent_offer_id: Optional[int]
    squeak_hash: bytes
    payment_hash: bytes
    secret_key: bytes
    nonce: bytes
    price_msat: int
    payment_request: str
    invoice_time: int
    invoice_expiry: int
    client_addr: str

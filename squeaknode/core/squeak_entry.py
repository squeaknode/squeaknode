from typing import NamedTuple
from typing import Optional


class SqueakEntry(NamedTuple):
    squeak_hash: bytes
    address: str
    block_height: int
    block_hash: bytes
    block_time: int
    reply_to: Optional[bytes]
    is_unlocked: bool
    liked_time: Optional[int] = None
    content: Optional[str] = None

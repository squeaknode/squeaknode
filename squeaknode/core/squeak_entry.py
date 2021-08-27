from typing import NamedTuple
from typing import Optional

from squeaknode.core.squeak_profile import SqueakProfile


class SqueakEntry(NamedTuple):
    squeak_hash: bytes
    address: str
    block_height: int
    block_hash: bytes
    block_time: int
    squeak_time: int
    reply_to: Optional[bytes]
    is_unlocked: bool
    squeak_profile: Optional[SqueakProfile]
    liked_time: Optional[int] = None
    content: Optional[str] = None

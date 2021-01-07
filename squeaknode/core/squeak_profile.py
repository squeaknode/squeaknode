from typing import NamedTuple
from typing import Optional


class SqueakProfile(NamedTuple):
    profile_id: Optional[int]
    profile_name: str
    private_key: bytes
    address: str
    sharing: bool
    following: bool

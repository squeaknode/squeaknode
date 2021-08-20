from typing import NamedTuple
from typing import Optional


class SqueakProfile(NamedTuple):
    """Represents a user who can author squeaks."""
    profile_id: Optional[int]
    profile_name: str
    private_key: Optional[bytes]
    address: str
    following: bool
    profile_image: Optional[bytes]

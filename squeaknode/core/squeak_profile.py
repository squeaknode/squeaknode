from typing import NamedTuple
from typing import Optional


class SqueakProfile(NamedTuple):
    """Represents a user who can author squeaks."""
    address: str
    profile_name: str
    private_key: Optional[bytes]
    sharing: bool
    following: bool
    profile_image: Optional[bytes]

from typing import List
from typing import NamedTuple


class LookupResponse(NamedTuple):
    """Represents a response to a lookup."""
    hashes: List[bytes]
    allowed_addresses: List[str]

from typing import NamedTuple
from typing import Optional


class SqueakPeer(NamedTuple):
    """Represents another node in the network."""
    peer_id: Optional[int]
    peer_name: str
    host: str
    port: int
    uploading: bool
    downloading: bool

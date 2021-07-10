from typing import NamedTuple
from typing import Optional

from squeaknode.core.peer_address import PeerAddress


class ConnectedPeer(NamedTuple):
    """Represents another node in the network."""
    peer_id: Optional[int]
    peer_name: str
    address: PeerAddress
    uploading: bool
    downloading: bool

from typing import NamedTuple

from squeaknode.core.peer_address import PeerAddress


class ConnectedPeer(NamedTuple):
    """Represents another node in the network."""
    peer_address: PeerAddress
    connect_time_s: int

from typing import NamedTuple

from squeaknode.core.util import get_peer_hash


class SqueakPeer(NamedTuple):
    """Represents another node in the network."""
    peer_hash: bytes
    peer_name: str
    host: str
    port: int
    uploading: bool
    downloading: bool


def make_squeak_peer(
        peer_name: str,
        host: str,
        port: int,
        uploading: bool,
        downloading: bool,
):
    return SqueakPeer(
        get_peer_hash(host, port),
        peer_name,
        host,
        port,
        uploading,
        downloading,
    )

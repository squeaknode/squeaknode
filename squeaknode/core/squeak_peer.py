from typing import NamedTuple


class SqueakPeer(NamedTuple):
    peer_id: int
    peer_name: str
    host: str
    port: int
    uploading: bool
    downloading: bool

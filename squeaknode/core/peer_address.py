from typing import NamedTuple


class PeerAddress(NamedTuple):
    """Class for representing a remote peer address."""
    host: str
    port: int

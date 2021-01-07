from typing import NamedTuple


class LightningAddressHostPort(NamedTuple):
    """Class for representing a remote lightning peer address."""
    host: str
    port: int

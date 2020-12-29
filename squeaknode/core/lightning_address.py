from dataclasses import dataclass


@dataclass
class LightningAddressHostPort:
    """Class for representing a remote lightning peer address."""

    host: str
    port: int

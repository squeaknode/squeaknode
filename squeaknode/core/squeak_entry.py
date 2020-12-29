from dataclasses import dataclass

from squeak.core import CSqueak


@dataclass
class SqueakEntry:
    """Class for saving an offer from a remote peer."""

    squeak: CSqueak
    block_header: bytes

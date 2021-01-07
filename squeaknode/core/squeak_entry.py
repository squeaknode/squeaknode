from typing import NamedTuple

from squeak.core import CSqueak


class SqueakEntry(NamedTuple):
    squeak: CSqueak
    block_header: bytes

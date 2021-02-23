from typing import NamedTuple

from bitcoin.core import CBlockHeader
from squeak.core import CSqueak


class SqueakEntry(NamedTuple):
    squeak: CSqueak
    block_header: CBlockHeader
    liked: bool = False

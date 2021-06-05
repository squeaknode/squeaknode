from typing import NamedTuple
from typing import Optional

from bitcoin.core import CBlockHeader
from squeak.core import CSqueak


class SqueakEntry(NamedTuple):
    squeak: CSqueak
    block_header: CBlockHeader
    liked_time: Optional[int] = None

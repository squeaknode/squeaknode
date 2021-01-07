from typing import NamedTuple
from typing import Optional

from squeak.core import CSqueak

from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.squeak_peer import SqueakPeer


class SqueakEntry(NamedTuple):
    squeak: CSqueak
    block_header: bytes

from typing import NamedTuple
from typing import Optional

from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.squeak_peer import SqueakPeer


class ReceivedOfferWithPeer(NamedTuple):
    """Class for saving an offer from a remote peer."""
    received_offer: ReceivedOffer
    peer: Optional[SqueakPeer]

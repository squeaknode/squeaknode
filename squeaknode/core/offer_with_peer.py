from typing import NamedTuple

from squeaknode.core.offer import Offer
from squeaknode.core.squeak_peer import SqueakPeer


class OfferWithPeer(NamedTuple):
    """Class for saving an offer from a remote peer."""
    offer: Offer
    peer: SqueakPeer

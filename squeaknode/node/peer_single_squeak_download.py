import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_get_offer import PeerGetOffer
from squeaknode.node.peer_task import PeerSyncTask

logger = logging.getLogger(__name__)


class PeerSingleSqueakDownload(PeerSyncTask):
    def __init__(
        self,
        peer,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        super().__init__(peer, squeak_store, postgres_db, lightning_client)

    def download_single_squeak(self, squeak_hash):
        # Download squeak if not already present.
        saved_squeak = self._get_saved_squeak(squeak_hash)
        if not saved_squeak:
            self._download_squeak(squeak_hash)

        # Download offer from peer if not already present.
        saved_offer = self._get_saved_offer(squeak_hash)
        if not saved_offer:
            self._download_offer(squeak_hash)

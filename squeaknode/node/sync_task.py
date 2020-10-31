import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_get_offer import PeerGetOffer

logger = logging.getLogger(__name__)


class SyncTask:
    def __init__(
        self,
        peer,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        self.peer = peer
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )

        self._stop_event = threading.Event()

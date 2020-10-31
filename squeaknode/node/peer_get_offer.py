import logging
import threading

from squeak.core.encryption import generate_data_key

from squeaknode.core.offer import Offer
from squeaknode.network.peer_client import PeerClient

logger = logging.getLogger(__name__)


class PeerGetOffer:
    def __init__(self, peer, squeak_hash, squeak_store, postgres_db, lightning_client):
        self.peer = peer
        self.squeak_hash = squeak_hash
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )

        self._stop_event = threading.Event()

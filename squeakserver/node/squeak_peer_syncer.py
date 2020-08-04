import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.network.peer_client import PeerClient

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


class PeerDownloadTask:
    def __init__(
            self,
            peer,
            block_height,
            squeak_store,
            lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
    ):
        self.peer = peer
        self.block_height = block_height
        self.squeak_store = squeak_store
        self.lookup_block_interval = lookup_block_interval
        self._stop_event = threading.Event()

    def download(self):
        logger.info("Downloading from peer: {} with current block: {}".format(
            self.peer,
            self.block_height,
        ))

        # TODO: get list of followed addresses.
        addresses = []
        min_block = self.block_height - self.lookup_block_interval
        max_block = self.block_height

        # Get remote hashes
        remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
        logger.info("Got remote hashes: {}".format(remote_hashes))
        # Get local hashes
        local_hashes = self._get_local_hashes(addresses, min_block, max_block)
        logger.info("Got local hashes: {}".format(local_hashes))

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_local_hashes(self, addresses, min_block, max_block):
        return self.squeak_store.lookup_squeaks(addresses, min_block, max_block)

    def _get_remote_hashes(self, addresses, min_block, max_block):
        peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
        )
        return peer_client.lookup_squeaks(addresses, min_block, max_block)

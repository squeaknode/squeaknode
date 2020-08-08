import logging
import threading

from squeakserver.server.util import get_hash
from squeakserver.node.peer_download import PeerDownload
from squeakserver.node.peer_get_offer import PeerGetOffer

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakGetOfferStatus:
    def __init__(self):
        self.downloads = {}

    def add_download(self, peer, squeak_hash, peer_download):
        key = (peer.peer_id, squeak_hash)
        self.downloads[key] = peer_download

    def is_downloading(self, peer, squeak_hash):
        key = (peer.peer_id, squeak_hash)
        return key in self.downloads

    def remove_download(self, peer, squeak_hash):
        key = (peer.peer_id, squeak_hash)
        del self.downloads[key]

    def get_current_downloads(self):
        return self.downloads.values()


class SqueakGetOfferController:
    def __init__(self, squeak_store, postgres_db, lightning_client):
        self.squeak_get_offer_status = SqueakGetOfferStatus()
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

    def get_offers(self, peers, squeak_hash):
        self._download_from_peers(peers, squeak_hash)

    def _download_from_peers(self, peers, squeak_hash):
        for peer in peers:
            if peer.downloading:
                download_thread = threading.Thread(
                    target=self._download_from_peer,
                    args=(peer, squeak_hash,),
                )
                download_thread.start()

    def _download_from_peer(self, peer, squeak_hash):
        peer_get_offer = PeerGetOffer(
            peer,
            squeak_hash,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        try:
            logger.debug("Trying to get offer from peer: {} for squeak: {}".format(peer.peer_id, squeak_hash))
            with self.DownloadingContextManager(peer, squeak_hash, peer_get_offer, self.squeak_get_offer_status) as downloading_manager:
                peer_get_offer.get_offer()
        except Exception as e:
            logger.error("Get offer from peer failed.", exc_info=True)

    class DownloadingContextManager():
        def __init__(self, peer, squeak_hash, peer_download, squeak_get_offer_status):
            self.peer = peer
            self.squeak_hash = squeak_hash
            self.peer_download = peer_download
            self.squeak_get_offer_status = squeak_get_offer_status

            if self.squeak_get_offer_status.is_downloading(self.peer, self.squeak_hash):
                raise Exception("Peer {} is already getting offer for squeak hash: {}".format(
                    self.peer.peer_id,
                    self.squeak_hash,
                ))

        def __enter__(self):
            self.squeak_get_offer_status.add_download(self.peer, self.squeak_hash, self.peer_download)
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.squeak_get_offer_status.remove_download(self.peer, self.squeak_hash)

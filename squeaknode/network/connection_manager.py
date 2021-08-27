import logging
import threading
from typing import Dict
from typing import List
from typing import Optional

from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.peer import Peer


MIN_PEERS = 5
MAX_PEERS = 10
UPDATE_THREAD_SLEEP_TIME = 10


logger = logging.getLogger(__name__)


class ConnectionManager(object):
    """Maintains connections to other peers in the network.
    """

    def __init__(self):
        self._peers: Dict[PeerAddress, Peer] = {}
        self.peers_lock = threading.Lock()
        self.peers_changed_callbacks = {}

    @property
    def peers(self) -> List[Peer]:
        return list(self._peers.values())

    def has_connection(self, address):
        """Return True if the address is already connected."""
        return address in self._peers

    def on_peers_changed(self):
        peers = self.peers
        logger.info('Current number of peers {}'.format(len(peers)))
        logger.info('Current peers:--------')
        for peer in peers:
            logger.info(peer)
        logger.info('--------------')
        for callback in self.peers_changed_callbacks.values():
            callback(peers)

    # def listen_peers_changed(self, callback):
    #     self.peers_changed_callback = callback

    def _is_duplicate_nonce(self, peer):
        for other_peer in self.peers:
            if other_peer.local_version:
                if peer.remote_version == other_peer.local_version.nNonce:
                    return True
        return False

    def add_peer(self, peer: Peer):
        """Add a peer.
        """
        with self.peers_lock:
            if self._is_duplicate_nonce(peer):
                logger.debug('Failed to add peer {}'.format(peer))
                raise DuplicateNonceError()
            if self.has_connection(peer.remote_address):
                logger.debug('Failed to add peer {}'.format(peer))
                raise DuplicatePeerError()
            self._peers[peer.remote_address] = peer
            logger.debug('Added peer {}'.format(peer))
            self.on_peers_changed()

    def remove_peer(self, peer: Peer):
        """Add a peer.
        """
        with self.peers_lock:
            if not self.has_connection(peer.remote_address):
                logger.debug('Failed to remove peer {}'.format(peer))
                raise MissingPeerError()
            del self._peers[peer.remote_address]
            logger.debug('Removed peer {}'.format(peer))
            self.on_peers_changed()

    def get_peer(self, address) -> Optional[Peer]:
        """Get a peer info by address.
        """
        return self._peers.get(address)

    def stop_connection(self, address):
        """Stop peer connections for address.
        """
        with self.peers_lock:
            peer = self.get_peer(address)
            if peer is not None:
                peer.stop()

    def stop_all_connections(self):
        """Stop all peer connections.
        """
        with self.peers_lock:
            for peer in self.peers:
                peer.stop()

    def add_peers_changed_callback(self, name, callback):
        self.peers_changed_callbacks[name] = callback

    def remove_peers_changed_callback(self, name):
        del self.peers_changed_callbacks[name]


class DuplicatePeerError(Exception):
    pass


class DuplicateNonceError(Exception):
    pass


class MissingPeerError(Exception):
    pass

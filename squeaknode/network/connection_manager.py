# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import queue
import socket
import threading
from contextlib import contextmanager
from typing import Dict
from typing import List
from typing import Optional

from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.connection import Connection
from squeaknode.network.peer import Peer
from squeaknode.network.peer_client import ConnectPeerResult
from squeaknode.node.listener_subscription_client import EventListener
from squeaknode.node.squeak_controller import SqueakController


MIN_PEERS = 5
MAX_PEERS = 10
UPDATE_THREAD_SLEEP_TIME = 10


logger = logging.getLogger(__name__)


class ConnectionManager(object):
    """Maintains connections to other peers in the network.
    """

    def __init__(self, local_address):
        self._peers: Dict[PeerAddress, Peer] = {}
        self.peers_lock = threading.Lock()
        self.peer_changed_listener = EventListener()
        self.single_peer_changed_listener = EventListener()
        self.accept_connections = True
        self.local_address = local_address

    @contextmanager
    def connect(
            self,
            peer_socket: socket.socket,
            address: PeerAddress,
            outgoing: bool,
            squeak_controller: SqueakController,
            result_queue: queue.Queue,
    ):
        try:
            peer = Peer(
                peer_socket,
                self.local_address,
                address,
                outgoing,
                self.single_peer_changed_listener,
            )
            connection = Connection(peer, squeak_controller)
            logger.debug("Doing handshake.")
            connection.handshake()
            logger.debug("Adding peer.")
            self._add_peer(peer)
            result_queue.put(
                ConnectPeerResult.from_success(peer.remote_address))
            logger.debug("Yielding connection.")
            yield connection
            logger.debug("Removing peer.")
            self._remove_peer(peer)
        except Exception as e:
            logger.exception("Error in connection.")
            result_queue.put(ConnectPeerResult.from_failure(e))
            raise
        finally:
            logger.info("Disconnected peer.")
            peer.stop()

    @property
    def peers(self) -> List[Peer]:
        return list(self._peers.values())

    def has_connection(self, address):
        """Return True if the address is already connected."""
        return address in self._peers

    def _on_peers_changed(self):
        peers = self.peers
        logger.info('Current number of peers {}'.format(len(peers)))
        logger.info('Current peers:--------')
        for peer in peers:
            logger.info(peer)
        logger.info('--------------')
        self.peer_changed_listener.handle_new_item(peers)

    def _is_duplicate_nonce(self, peer):
        for other_peer in self.peers:
            if other_peer.local_version:
                if peer.remote_version == other_peer.local_version.nNonce:
                    return True
        return False

    def _add_peer(self, peer: Peer):
        """Add a peer.
        """
        with self.peers_lock:
            if not self.accept_connections:
                raise NotAcceptingConnectionsError()
            if self._is_duplicate_nonce(peer):
                logger.debug('Failed to add peer {}'.format(peer))
                raise DuplicateNonceError()
            if self.has_connection(peer.remote_address):
                logger.debug('Failed to add peer {}'.format(peer))
                raise DuplicatePeerError()
            self._peers[peer.remote_address] = peer
            logger.debug('Added peer {}'.format(peer))
            self._on_peers_changed()

    def _remove_peer(self, peer: Peer):
        """Remove a peer.
        """
        with self.peers_lock:
            if not self.has_connection(peer.remote_address):
                return
            del self._peers[peer.remote_address]
            logger.debug('Removed peer {}'.format(peer))
            self._on_peers_changed()

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
        self.accept_connections = False
        with self.peers_lock:
            for peer in self.peers:
                peer.stop()

    def yield_peers_changed(self, stopped: threading.Event):
        yield from self.peer_changed_listener.yield_items(stopped)

    def yield_single_peer_changed(self, peer_address: PeerAddress, stopped: threading.Event):
        for peer in self.single_peer_changed_listener.yield_items(stopped):
            logger.debug('yield_single_peer_changed: {}'.format(peer))
            if peer.remote_address == peer_address:
                if peer.connect_time is None:
                    yield None
                else:
                    yield peer


class DuplicatePeerError(Exception):
    pass


class DuplicateNonceError(Exception):
    pass


class NotAcceptingConnectionsError(Exception):
    pass

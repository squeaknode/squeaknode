import logging
import socket

import squeak.params


logger = logging.getLogger(__name__)


class NetworkManager(object):
    """Used to manage the peer networking.
    """

    def __init__(self, connection_manager, peer_server):
        self.connection_manager = connection_manager
        self.peer_server = peer_server
        self.peer_blacklist = set()

    def get_peers(self):
        """Get all currently connected peers."""
        return self.connection_manager.peers

    def connect_peer(self, address):
        """Connect to a peer by address."""
        logger.debug('Connecting to address {}'.format(address))
        peer = self.connection_manager.get_peer(address)
        if peer:
            return
        self.peer_server.connect_address(address)

    def disconnect_peer(self, address):
        """Disconnect from a peer by address."""
        logger.debug('Disconnecting from address {}'.format(address))
        peer = self.connection_manager.get_peer(address)
        if peer:
            peer.stop()

    def connect_host(self, host):
        """Connect to a peer by hostname."""
        address = resolve_hostname(host)
        self.connect_peer(address)

    def connect_seed_peers(self):
        """Find more peers.
        """
        for address in get_seed_peer_addresses():
            self.connect_peer(address)

    def __enter__(self):
        logger.debug('Starting network manager')
        self.peer_server.start()
        return self

    def __exit__(self, *exc):
        self.peer_server.stop()
        logger.debug('Stopped network manager.')


def resolve_hostname(hostname):
    """Get the ip address from hostname."""
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        return None
    port = squeak.params.params.DEFAULT_PORT
    return (ip, port)


def get_seed_peer_addresses():
    """Get addresses of seed peers"""
    for _, seed_host in squeak.params.params.DNS_SEEDS:
        address = resolve_hostname(seed_host)
        if address:
            yield address

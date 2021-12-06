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
from typing import List
from typing import Optional

from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.seed_peer import SeedPeer
from squeaknode.core.seed_peer import SeedPeerConfig
from squeaknode.db.squeak_db import SqueakDb


MAINNET_SEED_PEERS = {
    'squeakhub': PeerAddress(
        network=Network.IPV4,
        host='squeakhub.com',
        port=8555,
    )
}

TESTNET_SEED_PEERS = {
    'docker-squeaknode': PeerAddress(
        network=Network.IPV4,
        host='localhost',
        port=18557,
    )
}

SIMNET_SEED_PEERS = {
    'simnet_seed_peer': PeerAddress(
        network=Network.IPV4,
        host='simnet-seed-peer.com',
        port=18555,
    )
}


def get_seed_peer_dict(network: str):
    if network == 'mainnet':
        return MAINNET_SEED_PEERS
    elif network == 'testnet':
        return TESTNET_SEED_PEERS
    elif network == 'simnet':
        return SIMNET_SEED_PEERS
    else:
        return {}


class SeedPeers:

    def __init__(self, squeak_db: SqueakDb, seed_peer_dict: dict):
        self.squeak_db = squeak_db
        self.seed_peer_dict = seed_peer_dict

    @property
    def seed_peers(self):
        return self.seed_peer_dict

    def get_seed_peers(self) -> List[SeedPeer]:
        ret = []
        for name, peer_address in self.seed_peers.items():
            config = self.get_config(name)
            seed_peer = SeedPeer(
                peer_name=name,
                address=peer_address,
                config=config,
            )
            ret.append(seed_peer)
        return ret

    def get_seed_peer(self, name: str) -> Optional[SeedPeer]:
        peer_address = self.seed_peers.get(name)
        if peer_address is None:
            return None
        config = self.get_config(name)
        return SeedPeer(
            peer_name=name,
            address=peer_address,
            config=config,
        )

    def get_config(self, name: str) -> SeedPeerConfig:
        return self.get_config_from_db(name) or \
            self.get_default_config(name)

    def get_config_from_db(self, name: str) -> Optional[SeedPeerConfig]:
        return self.squeak_db.get_seed_peer_config(name)

    def get_default_config(self, name: str) -> SeedPeerConfig:
        return SeedPeerConfig(
            peer_name=name,
            autoconnect=True,
            share_for_free=False,
        )

    def insert_default_config(self, name: str) -> Optional[str]:
        config = self.get_default_config(name)
        return self.squeak_db.insert_seed_peer_config(config)

    def set_seed_peer_autoconnect(self, name: str, autoconnect: bool) -> None:
        self.insert_default_config(name)
        self.squeak_db.set_seed_peer_config_autoconnect(name, autoconnect)

    def set_seed_peer_share_for_free(self, name: str, share_for_free: bool) -> None:
        self.insert_default_config(name)
        self.squeak_db.set_seed_peer_config_share_for_free(
            name, share_for_free)

    def get_autoconnect_seed_peer_addresses(self) -> List[PeerAddress]:
        seed_peers = self.get_seed_peers()
        return [
            seed_peer.address
            for seed_peer in seed_peers
            if seed_peer.config.autoconnect
        ]

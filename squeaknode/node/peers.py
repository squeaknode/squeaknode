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

from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.seed_peer import SeedPeer
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.saved_peers import SavedPeers
from squeaknode.node.seed_peers import SeedPeers


class Peers:

    def __init__(self, squeak_db: SqueakDb, seed_peer_dict: dict):
        self.saved_peers = SavedPeers(squeak_db)
        self.seed_peers = SeedPeers(squeak_db, seed_peer_dict)

    def create_saved_peer(self, peer_name: str, peer_address: PeerAddress):
        # TODO: Check if peer name or peer address is in seed peers config dict.
        self.saved_peers.create_saved_peer(peer_name, peer_address)

    def get_saved_peer(self, peer_id: int) -> Optional[SqueakPeer]:
        return self.saved_peers.get_saved_peer(peer_id)

    def get_saved_peer_by_address(self, peer_address: PeerAddress) -> Optional[SqueakPeer]:
        return self.saved_peers.get_saved_peer_by_address(peer_address)

    def get_saved_peers(self):
        return self.saved_peers.get_saved_peers()

    def set_saved_peer_autoconnect(self, peer_id: int, autoconnect: bool):
        self.saved_peers.set_peer_autoconnect(peer_id, autoconnect)

    def set_saved_peer_share_for_free(self, peer_id: int, share_for_free: bool):
        self.saved_peers.set_peer_share_for_free(peer_id, share_for_free)

    def rename_save_peer(self, peer_id: int, peer_name: str):
        self.saved_peers.rename_peer(peer_id, peer_name)

    def delete_saved_peer(self, peer_id: int):
        self.saved_peers.delete_peer(peer_id)

    def get_seed_peers(self) -> List[SeedPeer]:
        return self.seed_peers.get_seed_peers()

    def get_seed_peer(self, name: str) -> Optional[SeedPeer]:
        return self.seed_peers.get_seed_peer(name)

    def set_seed_peer_autoconnect(self, name: str, autoconnect: bool) -> None:
        self.seed_peers.set_seed_peer_autoconnect(name, autoconnect)

    def set_seed_peer_share_for_free(self, name: str, share_for_free: bool) -> None:
        self.seed_peers.set_seed_peer_share_for_free(name, share_for_free)

    def get_autoconnect_addresses(self) -> List[PeerAddress]:
        return self.saved_peers.get_autoconnect_addresses() + \
            self.seed_peers.get_autoconnect_seed_peer_addresses()

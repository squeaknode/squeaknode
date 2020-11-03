import logging
import threading
import queue

from dataclasses import dataclass
from typing import Any
from typing import List

from collections import namedtuple

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_task import PeerSyncTask
from squeaknode.node.peer_connection import PeerConnection

logger = logging.getLogger(__name__)


class NetworkSync:

    def __init__(
        self,
        squeak_store,
        postgres_db,
        lightning_client,
    ):
        self.squeak_store = squeak_store
        self.postgres_db = postgres_db
        self.lightning_client = lightning_client

    def sync_timeline_download(self, peer, block_height):
        if not peer.downloading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_sync_task.download(block_height)

    def sync_timeline_upload(self, peer, block_height):
        if not peer.uploading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_sync_task.upload(block_height)

    def sync_single_squeak_download(self, peer, squeak_hash):
        if not peer.downloading:
            return
        peer_connection = PeerConnection(peer)
        peer_sync_task = PeerSyncTask(
            peer_connection,
            self.squeak_store,
            self.postgres_db,
            self.lightning_client,
        )
        peer_sync_task.download_single_squeak(squeak_hash)

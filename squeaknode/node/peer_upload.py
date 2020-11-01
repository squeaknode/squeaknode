import logging
import threading

from squeaknode.network.peer_client import PeerClient
from squeaknode.node.peer_task import PeerSyncTask

logger = logging.getLogger(__name__)


LOOKUP_BLOCK_INTERVAL = 1008  # 1 week


# class PeerUpload(PeerSyncTask):
#     def __init__(
#         self,
#         peer,
#         squeak_store,
#         postgres_db,
#         lightning_client,
#     ):
#         super().__init__(peer, squeak_store, postgres_db, lightning_client)

#     def upload(
#         self,
#         block_height,
#         lookup_block_interval=LOOKUP_BLOCK_INTERVAL,
#     ):
#         # Get list of sharing addresses.
#         addresses = self._get_sharing_addresses()
#         logger.debug("Sharing addresses: {}".format(addresses))
#         min_block = block_height - lookup_block_interval
#         max_block = block_height

#         # Get remote hashes
#         remote_hashes = self._get_remote_hashes(addresses, min_block, max_block)
#         logger.debug("Got remote hashes: {}".format(len(remote_hashes)))
#         for hash in remote_hashes:
#             logger.debug("remote hash: {}".format(hash.hex()))

#         # Get local hashes
#         local_hashes = self._get_local_hashes(addresses, min_block, max_block)
#         logger.debug("Got local hashes: {}".format(len(local_hashes)))
#         for hash in local_hashes:
#             logger.debug("local hash: {}".format(hash.hex()))

#         # Get hashes to upload
#         hashes_to_upload = set(local_hashes) - set(remote_hashes)
#         logger.debug("Hashes to upload: {}".format(len(hashes_to_upload)))
#         for hash in hashes_to_upload:
#             logger.debug("hash to upload: {}".format(hash.hex()))

#         # Upload squeaks for the hashes
#         # TODO: catch exception uploading individual squeak
#         for hash in hashes_to_upload:
#             if self.stopped():
#                 return
#             self._upload_squeak(hash)

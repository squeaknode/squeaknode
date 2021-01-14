import logging


logger = logging.getLogger(__name__)


# class NetworkSync:
#     def __init__(
#         self,
#         squeak_controller,
#     ):
#         self.squeak_controller = squeak_controller

#     def sync_timeline(self, peer, min_block, max_block):
#         if not peer.downloading:
#             return
#         # peer_connection = PeerConnection(peer)
#         # with PeerConnection(peer).open_connection() as peer_connection:
#         with PeerSyncTask(
#                 self.squeak_controller,
#                 peer,
#                 None,
#         ).open_peer_sync_task() as peer_sync_task:
#             if peer.uploading:
#                 peer_sync_task.upload(min_block, max_block)
#             if peer.downloading:
#                 peer_sync_task.download(min_block, max_block)

#     def sync_single_squeak(self, peer, squeak_hash: bytes):
#         if not peer.downloading:
#             return
#         # peer_connection = PeerConnection(peer)
#         # with PeerConnection(peer).open_connection() as peer_connection:
#         with PeerSyncTask(
#                 self.squeak_controller,
#                 peer,
#                 None,
#         ).open_peer_sync_task() as peer_sync_task:
#             if peer.uploading:
#                 peer_sync_task.upload_single_squeak(squeak_hash)
#             if peer.downloading:
#                 peer_sync_task.download_single_squeak(squeak_hash)

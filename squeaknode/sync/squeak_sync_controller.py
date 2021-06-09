# import logging
# from squeaknode.sync.network_sync import SingleSqueakDownloadSync
# from squeaknode.sync.network_sync import SingleSqueakUploadSync
# from squeaknode.sync.network_sync import TimelineDownloadSync
# from squeaknode.sync.network_sync import TimelineUploadSync
# logger = logging.getLogger(__name__)
# class SqueakSyncController:
#     def __init__(self, squeak_controller, sync_block_interval, timeout_s):
#         self.squeak_controller = squeak_controller
#         self.sync_block_interval = sync_block_interval
#         self.timeout_s = timeout_s
#     def download_timeline(self, block_interval=None):
#         TimelineDownloadSync(
#             self.squeak_controller,
#             self.timeout_s,
#             block_interval,
#         ).sync()
#     def upload_timeline(self):
#         TimelineUploadSync(
#             self.squeak_controller,
#             self.timeout_s,
#         ).sync()
#     def download_single_squeak(self, squeak_hash):
#         SingleSqueakDownloadSync(
#             self.squeak_controller,
#             self.timeout_s,
#             squeak_hash,
#         ).sync()
#     def upload_single_squeak(self, squeak_hash):
#         SingleSqueakUploadSync(
#             self.squeak_controller,
#             self.timeout_s,
#             squeak_hash,
#         ).sync()

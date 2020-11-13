# import logging
# from hashlib import sha256

# from squeak.core.encryption import (
#     CEncryptedDecryptionKey,
#     generate_initialization_vector,
# )
# from squeak.core.signing import CSigningKey, CSqueakAddress
# from squeak.core import CheckSqueak

# from squeaknode.node.squeak_controller import SqueakCo


# logger = logging.getLogger(__name__)


# class SqueakNode:
#     def __init__(
#         self,
#         squeak_db,
#         blockchain_client,
#         lightning_client,
#         lightning_host_port,
#         price_msat,
#         max_squeaks_per_address_per_hour,
#         sync_interval_s,
#     ):
#         self.squeak_db = squeak_db
#         self.blockchain_client = blockchain_client
#         self.lightning_client = lightning_client
#         self.lightning_host_port = lightning_host_port
#         self.price_msat = price_msat
#         self.sync_interval_s = sync_interval_s
#         self.squeak_block_verifier = SqueakBlockVerifier(squeak_db, blockchain_client)
#         self.squeak_block_periodic_worker = SqueakBlockPeriodicWorker(
#             self.squeak_block_verifier
#         )
#         self.squeak_block_queue_worker = SqueakBlockQueueWorker(
#             self.squeak_block_verifier
#         )
#         self.squeak_rate_limiter = SqueakRateLimiter(
#             squeak_db,
#             blockchain_client,
#             lightning_client,
#             max_squeaks_per_address_per_hour,
#         )
#         self.squeak_whitelist = SqueakWhitelist(
#             squeak_db,
#         )
#         self.squeak_store = SqueakStore(
#             squeak_db,
#             self.squeak_block_verifier,
#             self.squeak_rate_limiter,
#             self.squeak_whitelist,
#         )
#         self.squeak_sync_controller = SqueakSyncController(
#             self.blockchain_client,
#             self.squeak_store,
#             self.squeak_db,
#             self.lightning_client,
#         )
#         self.squeak_peer_sync_worker = SqueakPeerSyncWorker(
#             self.squeak_sync_controller,
#             self.sync_interval_s,
#         )
#         self.squeak_expired_offer_cleaner = SqueakExpiredOfferCleaner(
#             self,
#         )
#         self.squeak_offer_expiry_worker = SqueakOfferExpiryWorker(
#             self.squeak_expired_offer_cleaner,
#         )
#         self.sent_offers_verifier = SentOffersVerifier(
#             self.squeak_db,
#             self.lightning_client,
#         )
#         self.sent_offers_worker = SentOffersWorker(
#             self.sent_offers_verifier,
#         )

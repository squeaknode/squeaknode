import logging
import queue

from squeakserver.server.util import get_hash
from squeakserver.node.block_info import BlockInfo

logger = logging.getLogger(__name__)


class SqueakRateLimiter:
    def __init__(self, postgres_db, blockchain_client, lightning_client, max_squeaks_per_block_per_address):
        self.postgres_db = postgres_db
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client
        self.max_squeaks_per_block_per_address = max_squeaks_per_block_per_address

    def should_rate_limit_allow(self, squeak):
        squeak_hash = get_hash(squeak)
        logger.info("Checking rate limit for squeak: {}".format(squeak_hash))
        current_squeak_count = self._get_current_squeak_count(squeak)
        return current_squeak_count < self.max_squeaks_per_block_per_address

    def _get_current_squeak_count(self, squeak):
        current_block_info = self._get_latest_block()
        current_block_height = current_block_info.block_height
        squeak_address = self._get_squeak_address(squeak)
        return self._get_num_squeaks_in_block(current_block_height, squeak_address)

    def _get_latest_block(self):
        get_info_response = self.lightning_client.get_info()
        block_hash = bytes.fromhex(get_info_response.block_hash)
        block_height = get_info_response.block_height
        return BlockInfo(block_hash, block_height)

    def _get_num_squeaks_in_block(self, block_height, squeak_address):
        hashes = self.postgres_db.lookup_squeaks(squeak_address, block_height, block_height)
        return len(hashes)

    def _get_squeak_address(self, squeak):
        address = squeak.GetAddress()
        return str(address)

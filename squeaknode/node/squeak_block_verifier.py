import logging

logger = logging.getLogger(__name__)


class SqueakBlockVerifier:
    def __init__(self, blockchain_client):
        self.blockchain_client = blockchain_client

    def _get_block_info_for_height(self, block_height):
        return self.blockchain_client.get_block_info_by_height(block_height)

    def get_block_header(self, squeak):
        try:
            block_info = self._get_block_info_for_height(squeak.nBlockHeight)
        except Exception:
            logger.error("Failed to get block info for squeak.", exc_info=False)
            return None
        if squeak.hashBlock != block_info.block_hash:
            logger.info("block hash incorrect: {}".format(block_info))
            return None
        return block_info.block_header

import logging
import time

from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey

logger = logging.getLogger(__name__)


class SqueakMaker:
    def __init__(self, blockchain_client):
        self.blockchain_client = blockchain_client

    def make_squeak(self, signing_profile, content_str, replyto_hash=None):
        signing_key_str = signing_profile.private_key.decode()
        signing_key = CSigningKey(signing_key_str)
        logger.info("Creating squeak with signing key: {}".format(signing_key))
        logger.info(
            "Creating squeak with replyto_hash: {}".format(replyto_hash))
        block_info = self._get_latest_block_info()
        logger.info("Creating squeak with block_info: {}".format(block_info))
        block_height = block_info.block_height
        block_hash = block_info.block_hash
        timestamp = self._get_current_time_s()
        if replyto_hash is None or len(replyto_hash) == 0:
            return MakeSqueakFromStr(
                signing_key,
                content_str,
                block_height,
                block_hash,
                timestamp,
            )
        else:
            return MakeSqueakFromStr(
                signing_key,
                content_str,
                block_height,
                block_hash,
                timestamp,
                replyto_hash,
            )

    # def _get_latest_block(self):
    #     get_info_response = self.lightning_client.get_info()
    #     block_hash = bytes.fromhex(get_info_response.block_hash)
    #     block_height = get_info_response.block_height
    #     return BlockInfo(block_hash, block_height)

    def _get_latest_block_info(self):
        return self.blockchain_client.get_best_block_info()

    def _get_current_time_s(self):
        return int(time.time())

import time

from squeak.core import CSqueak
from squeak.core import HASH_LENGTH
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey

from squeaknode.common.blockchain_client import BlockchainClient


class SqueakMaker(object):
    """A factory for creating squeaks"""

    def __init__(self, signing_key: CSigningKey, blockchain_client: BlockchainClient) -> None:
        self.signing_key = signing_key
        self.blockchain_client = blockchain_client

    def make_squeak(self, content: str, reply_to: bytes = b'\x00'*HASH_LENGTH) -> CSqueak:
        """Create a CSqueak instance.

        content: content of the squeak
        reply_to: hash of the reply_to squeak
        """
        block_height = self.blockchain_client.get_block_count()
        block_hash = self.blockchain_client.get_block_hash(block_height)
        timestamp = int(time.time())

        return MakeSqueakFromStr(
            self.signing_key,
            content,
            block_height,
            block_hash,
            timestamp,
        )

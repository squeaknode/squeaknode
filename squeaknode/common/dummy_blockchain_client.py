import json
from typing import Optional

import requests

from squeaknode.common.blockchain_client import BlockchainClient


class DummyBlockchainClient(BlockchainClient):
    """Gets only the genesis block of the main chain."""

    def __init__(self) -> None:
        pass

    def get_latest_block_height(self) -> int:
        return 0

    def get_block_hash(self, block_height: int) -> Optional[bytes]:
        # return the genesis block hash
        if block_height == 0:
            return lx('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b')
        return None

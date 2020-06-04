import json
from typing import Optional

import requests

from squeaknode.common.blockchain_client import BlockchainClient


class BTCDBlockchainClient(BlockchainClient):
    """Access a blockchain using RPC."""

    def __init__(
            self,
            host: str,
            port: int,
            rpc_user: str,
            rpc_password: str,
    ) -> None:
        self.url = f'https://{rpc_user}:{rpc_password}@{host}:{port}'
        self.headers = {'content-type': 'application/json'}

    def get_latest_block_height(self) -> int:
        payload = {
            "method": "getblockcount",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url,
            data=json.dumps(payload),
            headers=self.headers,
        ).json()

        block_count = response["result"]
        return block_count

    def get_block_hash(self, block_height: int) -> Optional[bytes]:
        # return self.access.getblockhash(block_height)
        payload = {
            "method": "getblockhash",
            "params": [block_height],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url,
            data=json.dumps(payload),
            headers=self.headers,
        ).json()

        result = response["result"]
        block_hash = bytes.fromhex(result)

        return block_hash

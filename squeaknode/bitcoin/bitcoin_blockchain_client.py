import json
import logging
from typing import Optional

import requests

from squeaknode.bitcoin.block_info import BlockInfo
from squeaknode.bitcoin.blockchain_client import BlockchainClient

logger = logging.getLogger(__name__)


class BitcoinBlockchainClient(BlockchainClient):
    """Access a bitcoin daemon using RPC."""

    def __init__(
        self,
        host: str,
        port: int,
        rpc_user: str,
        rpc_password: str,
    ) -> None:
        self.url = f"https://{rpc_user}:{rpc_password}@{host}:{port}"
        self.headers = {"content-type": "application/json"}

    def get_best_block_info(self) -> BlockInfo:
        block_height = self.get_block_count()
        logger.info("Best block height: {}".format(block_height))
        return self.get_block_info_by_height(block_height)

    def get_block_info_by_height(self, block_height: int) -> BlockInfo:
        block_hash = self.get_block_hash(block_height)
        block_header = self.get_block_header(block_hash, False)
        return BlockInfo(block_height, block_hash, block_header)

    def get_block_count(self) -> Optional[int]:
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

        logger.debug("Got response for get_block_count: {}".format(response))
        result = response["result"]
        block_count = int(result)
        logger.debug("Got block_count: {}".format(block_count))
        return block_count

    def get_block_hash(self, block_height: int) -> Optional[str]:
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

        logger.debug("Got response for get_block_hash: {}".format(response))
        result = response["result"]
        block_hash = result
        logger.debug("Got block_hash: {}".format(block_hash))
        return block_hash

    # def get_best_block_hash(self) -> Optional[bytes]:
    #     payload = {
    #         "method": "getblockhash",
    #         "params": [],
    #         "jsonrpc": "2.0",
    #         "id": 0,
    #     }
    #     response = requests.post(
    #         self.url, data=json.dumps(payload), headers=self.headers,
    #     ).json()

    #     result = response["result"]
    #     block_hash = bytes.fromhex(result)
    #     return block_hash

    def get_block_header(self, block_hash: str, verbose: bool) -> Optional[bytes]:
        payload = {
            "method": "getblockheader",
            "params": [block_hash, verbose],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url,
            data=json.dumps(payload),
            headers=self.headers,
        ).json()

        logger.debug("Got response for get_block_header: {}".format(response))
        result = response["result"]
        logger.debug("Got block_header: {}".format(result))
        return result

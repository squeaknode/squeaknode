import logging
from abc import ABC, abstractmethod

from squeaknode.bitcoin.block_info import BlockInfo

logger = logging.getLogger(__name__)


class BlockchainClient(ABC):
    @abstractmethod
    def get_best_block_info(self) -> BlockInfo:
        pass

    @abstractmethod
    def get_block_info_by_height(self, block_height: int) -> BlockInfo:
        pass

    @abstractmethod
    def get_block_hash(self, block_height: int) -> bytes:
        pass

    @abstractmethod
    def get_block_header(self, block_hash: bytes, verbose: bool) -> bytes:
        pass

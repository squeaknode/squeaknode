import logging
from abc import ABC, abstractmethod

from squeakserver.blockchain.block_info import BlockInfo

logger = logging.getLogger(__name__)


class BlockchainClient(ABC):
    @abstractmethod
    def get_best_block_info(self) -> BlockInfo:
        pass

    @abstractmethod
    def get_block_info_by_height(self) -> BlockInfo:
        pass

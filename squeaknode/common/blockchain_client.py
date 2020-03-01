from abc import ABC
from abc import abstractmethod
from typing import Optional


class BlockchainClient(ABC):
    """Used to get info from the blockchain."""

    @abstractmethod
    def get_block_count(self) -> int:
        pass

    @abstractmethod
    def get_block_hash(self, block_height: int) -> Optional[bytes]:
        pass

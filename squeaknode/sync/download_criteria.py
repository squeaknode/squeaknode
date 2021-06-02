import logging
from abc import ABC
from abc import abstractmethod
from typing import List

from squeak.core import CSqueak

from squeaknode.core.block_range import BlockRange
from squeaknode.core.util import get_hash


logger = logging.getLogger(__name__)


class DownloadCriteria(ABC):

    @abstractmethod
    def is_interested(self, squeak: CSqueak) -> bool:
        pass


class RangeCriteria(DownloadCriteria):

    def __init__(
        self,
        block_range: BlockRange,
        follow_list: List[str],
    ):
        self.block_range = block_range
        self.follow_list = follow_list

    def is_interested(self, squeak: CSqueak) -> bool:
        # Check block range.
        if squeak.nBlockHeight < self.block_range.min_block or \
           squeak.nBlockHeight > self.block_range.max_block:
            return False
        # Check if address is in followed list.
        squeak_address = str(squeak.GetAddress())
        if squeak_address not in self.follow_list:
            return False
        return True


class HashCriteria(DownloadCriteria):

    def __init__(
        self,
        squeak_hash: bytes,
    ):
        self.squeak_hash = squeak_hash

    def is_interested(self, squeak: CSqueak) -> bool:
        # Check hash.
        return get_hash(squeak) == self.squeak_hash

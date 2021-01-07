import logging
from abc import ABC
from abc import abstractmethod
from typing import List

from squeak.core import CSqueak


logger = logging.getLogger(__name__)


class SqueakWhitelist(ABC):

    @abstractmethod
    def should_allow_squeak(self, squeak: CSqueak) -> bool:
        pass

    @abstractmethod
    def get_allowed_addresses(self, addresses: List[str]):
        pass

    @abstractmethod
    def refresh(self):
        pass

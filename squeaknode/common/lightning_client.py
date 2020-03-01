from abc import ABC
from abc import abstractmethod


class LightningClient(ABC):
    """Used to get interact with the lightning wallet."""

    @abstractmethod
    def get_wallet_balance(self):
        # Retrieve and display the wallet balance
        pass

    # @abstractmethod
    # def get_block_height(self) -> int:
    #     pass

    # @abstractmethod
    # def get_block_hash(self) -> bytes:
    #     pass

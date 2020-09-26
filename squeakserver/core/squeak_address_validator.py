import logging

from bitcoin.base58 import Base58ChecksumError
from bitcoin.wallet import CBitcoinAddressError
from squeak.core.signing import CSqueakAddress

logger = logging.getLogger(__name__)


class SqueakAddressValidator(object):
    """Validates addresses"""

    def __init__(self) -> None:
        pass

    def validate(self, squeak_address_str: str) -> bool:
        if not squeak_address_str:
            return False
        try:
            CSqueakAddress(squeak_address_str)
            return True
        except (Base58ChecksumError, CBitcoinAddressError) as e:
            logger.info("Got invalid address with error: {}".format(e))
            return False

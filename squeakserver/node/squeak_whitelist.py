import logging
import queue

from squeakserver.server.util import get_hash
from squeakserver.node.block_info import BlockInfo

logger = logging.getLogger(__name__)


class SqueakWhitelist:
    def __init__(self, postgres_db):
        self.postgres_db = postgres_db
        self.allowed_addresses = []
        self.refresh()

    def should_allow_squeak(self, squeak):
        squeak_hash = get_hash(squeak)
        squeak_address = CSqueakAddress.from_verifying_key(verifying_key)
        squeak_address_str = str(squeak_address_str)
        logger.info("Checking whitelist for squeak hash: {}, squeak address".format(squeak_hash, squeak_address_str))
        is_allowed = squeak_address_str in self.allowed_addresses
        logger.info("Is squeak in whitelist: {}".format(is_allowed))
        return is_allowed

    def refresh(self):
        whitelisted_addresses = self._get_whitelisted_addresses()
        self.allowed_addresses = whitelisted_addresses

    def _get_whitelisted_addresses(self):
        whitelisted_profiles = self.postgres_db.get_whitelisted_profiles()
        return [
            profile.address
            for profile in whitelisted_profiles
        ]

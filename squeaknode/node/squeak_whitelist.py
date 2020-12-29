import logging

from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


class SqueakWhitelist:
    def __init__(self, squeak_db):
        self.squeak_db = squeak_db
        self.allowed_addresses = []
        self.refresh()

    def should_allow_squeak(self, squeak):
        squeak_hash = get_hash(squeak)
        squeak_address = squeak.GetAddress()
        squeak_address_str = str(squeak_address)
        logger.info(
            "Checking whitelist for squeak hash: {}, squeak address: {}".format(
                squeak_hash, squeak_address_str
            )
        )
        logger.info("Allowed addresses: {}".format(self.allowed_addresses))
        is_allowed = squeak_address_str in self.allowed_addresses
        logger.info("Is squeak in whitelist: {}".format(is_allowed))
        return is_allowed

    def refresh(self):
        whitelisted_addresses = self._get_whitelisted_addresses()
        self.allowed_addresses = whitelisted_addresses

    def _get_whitelisted_addresses(self):
        whitelisted_profiles = self.squeak_db.get_following_profiles()
        return [profile.address for profile in whitelisted_profiles]

    def get_allowed_addresses(self, addresses):
        return set(self.allowed_addresses) & set(addresses)

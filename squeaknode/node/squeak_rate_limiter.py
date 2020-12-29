import logging

from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakRateLimiter:
    def __init__(
        self,
        squeak_db,
        blockchain_client,
        lightning_client,
        max_squeaks_per_address_per_hour,
    ):
        self.squeak_db = squeak_db
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client
        self.max_squeaks_per_address_per_hour = max_squeaks_per_address_per_hour

    def should_rate_limit_allow(self, squeak):
        squeak_hash = get_hash(squeak)
        logger.info("Checking rate limit for squeak: {}".format(squeak_hash))
        current_squeak_count = self._get_current_squeak_count(squeak)
        logger.info(
            "Current squeak count: {}, limit: {}".format(
                current_squeak_count, self.max_squeaks_per_address_per_hour
            )
        )
        return current_squeak_count < self.max_squeaks_per_address_per_hour

    def _get_current_squeak_count(self, squeak):
        squeak_address = self._get_squeak_address(squeak)
        return self._get_num_squeaks_in_last_hour(squeak_address)

    def _get_num_squeaks_in_last_hour(self, squeak_address):
        logger.info(
            "Getting squeak count for last hour for squeak address: {}".format(
                squeak_address
            )
        )
        hashes = self.squeak_db.lookup_squeaks_by_time(
            [squeak_address],
            HOUR_IN_SECONDS,
            include_unverified=True,
        )
        return len(hashes)

    def _get_squeak_address(self, squeak):
        address = squeak.GetAddress()
        return str(address)

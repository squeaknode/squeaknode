import logging

from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakRateLimiter:
    def __init__(
        self,
        squeak_db,
        max_squeaks_per_address_per_hour,
    ):
        self.squeak_db = squeak_db
        self.max_squeaks_per_address_per_hour = max_squeaks_per_address_per_hour

    def should_rate_limit_allow(self, squeak):
        logger.info("Checking rate limit for squeak: {!r}".format(
            get_hash(squeak)
        ))
        current_squeak_count = self._get_num_squeaks_with_address_with_block(
            squeak)
        logger.info(
            "Current squeak count: {}, limit: {}".format(
                current_squeak_count, self.max_squeaks_per_address_per_hour
            )
        )
        return current_squeak_count < self.max_squeaks_per_address_per_hour

    def _get_num_squeaks_with_address_with_block(self, squeak):
        address = str(squeak.GetAddress())
        block_height = squeak.nBlockHeight
        logger.info(
            "Getting squeak count for address: {} with height: {}".format(
                address,
                block_height,
            )
        )
        return self.squeak_db.number_of_squeaks_with_address_with_block(
            address,
            block_height,
        )

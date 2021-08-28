# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging

from squeaknode.core.util import get_hash

logger = logging.getLogger(__name__)


HOUR_IN_SECONDS = 3600


class SqueakRateLimiter:
    def __init__(
        self,
        squeak_db,
        max_squeaks_per_address_per_block,
    ):
        self.squeak_db = squeak_db
        self.max_squeaks_per_address_per_block = max_squeaks_per_address_per_block

    def should_rate_limit_allow(self, squeak):
        logger.info("Checking rate limit for squeak: {!r}".format(
            get_hash(squeak).hex(),
        ))
        current_squeak_count = self._get_num_squeaks_with_address_with_block(
            squeak)
        logger.info(
            "Current squeak count: {}, limit: {}".format(
                current_squeak_count, self.max_squeaks_per_address_per_block
            )
        )
        return current_squeak_count < self.max_squeaks_per_address_per_block

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

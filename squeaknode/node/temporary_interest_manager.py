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
from typing import Optional

from squeak.core import CSqueak
from squeak.net import CInterested

from squeaknode.core.util import get_hash
from squeaknode.core.util import squeak_matches_interest

logger = logging.getLogger(__name__)


class TemporaryInterestCounter:

    def __init__(self):
        self.count = 0
        self.limit = 0

    def increment(self):
        self.count += 1


class TemporaryInterestManager:

    def __init__(self):
        self.interests = {}
        self.hashes = {}

    def lookup_counter(self, squeak: CSqueak) -> Optional[TemporaryInterestCounter]:
        for interest, counter in self.interests.items():
            if squeak_matches_interest(squeak, interest):
                return counter
        for squeak_hash, counter in self.hashes.items():
            if squeak_hash == get_hash(squeak):
                return counter
        return None

    def add_interest(self, interest: CInterested) -> None:
        self.interests[interest] = TemporaryInterestCounter()

    def add_hash(self, squeak_hash: bytes) -> None:
        self.hashes[squeak_hash] = TemporaryInterestCounter()

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
import uuid
from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Optional

from expiringdict import ExpiringDict
from squeak.core import CSqueak
from squeak.net import CInterested

from squeaknode.core.util import get_hash
from squeaknode.core.util import squeak_matches_interest

logger = logging.getLogger(__name__)


class TemporaryInterest(ABC):

    @abstractmethod
    def is_interested(self, squeak: CSqueak) -> bool:
        pass

    @abstractmethod
    def increment(self) -> bool:
        pass

    @abstractmethod
    def is_under_limit(self) -> bool:
        pass


class TemporaryRangeInterest(TemporaryInterest):

    def __init__(self, interest: CInterested):
        self.interest = interest

    def is_interested(self, squeak: CSqueak) -> bool:
        return squeak_matches_interest(squeak, self.interest)

    def increment(self) -> bool:
        pass

    def is_under_limit(self) -> bool:
        pass


class TemporaryHashInterest(TemporaryInterest):

    def __init__(self, squeak_hash: bytes):
        self.squeak_hash = squeak_hash

    def is_interested(self, squeak: CSqueak) -> bool:
        return self.squeak_hash == get_hash(squeak)

    def increment(self) -> bool:
        pass

    def is_under_limit(self) -> bool:
        pass


class TemporaryInterestManager:

    def __init__(self):
        self.interests: Dict[str, TemporaryInterest] = ExpiringDict(
            max_len=100, max_age_seconds=10)

    def lookup_counter(self, squeak: CSqueak) -> Optional[TemporaryInterest]:
        for name, interest in self.interests.items():
            if interest.is_interested(squeak):
                return interest
        return None

    def add_interest(self, interest: TemporaryInterest) -> None:
        name_key = "interest_key_{}".format(uuid.uuid1())
        self.interests[name_key] = interest

    def add_range_interest(self, interest: CInterested) -> None:
        self.add_interest(TemporaryRangeInterest(interest))

    def add_hash_interest(self, squeak_hash: bytes) -> None:
        self.add_interest(TemporaryHashInterest(squeak_hash))

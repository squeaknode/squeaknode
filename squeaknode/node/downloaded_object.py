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
from squeak.core import CSqueak
from squeak.net import CInterested

from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.offer import Offer
from squeaknode.core.squeaks import get_hash


class DownloadedObject:

    def matches_requested_squeak_range(self, interest: CInterested) -> bool:
        """Return True if the object matches the requested interest.
        """

    def matches_requested_squeak_hash(self, squeak_hash: bytes) -> bool:
        """Return True if the object matches the requested offer hash.
        """

    def matches_requested_offer_hash(self, squeak_hash: bytes) -> bool:
        """Return True if the object matches the requested squeak hash.
        """


class DownloadedSqueak(DownloadedObject):

    def __init__(self, squeak: CSqueak):
        self.squeak = squeak

    def matches_requested_squeak_range(self, interest: CInterested) -> bool:
        return squeak_matches_interest(self.squeak, interest)

    def matches_requested_squeak_hash(self, squeak_hash: bytes) -> bool:
        return squeak_hash == get_hash(self.squeak)

    def matches_requested_offer_hash(self, squeak_hash: bytes) -> bool:
        return False


class DownloadedOffer(DownloadedObject):

    def __init__(self, offer: Offer):
        self.offer = offer

    def matches_requested_squeak_range(self, interest: CInterested) -> bool:
        return False

    def matches_requested_squeak_hash(self, squeak_hash: bytes) -> bool:
        return False

    def matches_requested_offer_hash(self, squeak_hash: bytes) -> bool:
        return self.offer.squeak_hash == squeak_hash

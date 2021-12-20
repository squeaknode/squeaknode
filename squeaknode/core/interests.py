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
from typing import Iterable

from squeak.core import CSqueak
from squeak.net import CInterested


EMPTY_HASH = b'\x00' * 32


def squeak_matches_interest(squeak: CSqueak, interest: CInterested) -> bool:
    if len(interest.pubkeys) > 0 \
       and squeak.GetPubKey() not in interest.pubkeys:
        return False
    if interest.nMinBlockHeight != -1 \
       and squeak.nBlockHeight < interest.nMinBlockHeight:
        return False
    if interest.nMaxBlockHeight != -1 \
       and squeak.nBlockHeight > interest.nMaxBlockHeight:
        return False
    if interest.hashReplySqk != EMPTY_HASH \
       and squeak.hashReplySqk != interest.hashReplySqk:
        return False
    return True


def get_differential_squeaks(
        interest: CInterested,
        old_interest: CInterested,
) -> Iterable[CInterested]:
    # Get new squeaks below the current min_block
    if interest.nMinBlockHeight < old_interest.nMinBlockHeight:
        yield CInterested(
            pubkeys=old_interest.pubkeys,
            nMinBlockHeight=interest.nMinBlockHeight,
            nMaxBlockHeight=old_interest.nMinBlockHeight - 1,
        )
    # Get new squeaks above the current max_block
    if (interest.nMaxBlockHeight == -1 and old_interest.nMaxBlockHeight != -1) or \
       interest.nMaxBlockHeight > old_interest.nMaxBlockHeight:
        yield CInterested(
            pubkeys=old_interest.pubkeys,
            nMinBlockHeight=old_interest.nMaxBlockHeight + 1,
            nMaxBlockHeight=interest.nMaxBlockHeight,
        )
    # Get new squeaks for new pubkeys
    follow_pubkeys = set(interest.pubkeys)
    old_follow_pubkeys = set(old_interest.pubkeys)
    new_pubkeys = tuple(follow_pubkeys - old_follow_pubkeys)
    if len(new_pubkeys) > 0:
        yield CInterested(
            pubkeys=new_pubkeys,
            nMinBlockHeight=interest.nMinBlockHeight,
            nMaxBlockHeight=interest.nMaxBlockHeight,
        )

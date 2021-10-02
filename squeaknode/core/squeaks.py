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
import time
from typing import Optional
from typing import Tuple

from squeak.core import CSqueak
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey


DATA_KEY_LENGTH = 32
VERSION_NONCE_LENGTH = 8

HASH_LENGTH = 32
EMPTY_HASH = b'\x00' * HASH_LENGTH


def get_hash(squeak):
    return squeak.GetHash()[::-1]


def make_squeak_with_block(
        signing_key: CSigningKey,
        content_str: str,
        block_height: int,
        block_hash: bytes,
        replyto_hash: Optional[bytes] = None,
) -> Tuple[CSqueak, bytes]:
    """Create a new squeak.

    Args:
        signing_key: The private key to sign the squeak.
        content_str: The content of the squeak as a string.
        block_height: The height of the latest block in the bitcoin blockchain.
        block_hahs: The hash of the latest block in the bitcoin blockchain.
        replyto_hash: The hash of the squeak to which this one is replying.

    Returns:
        Tuple[CSqueak, bytes]: the squeak that was created together
    with its decryption key.
    """
    timestamp = int(time.time())
    return MakeSqueakFromStr(
        signing_key,
        content_str,
        block_height,
        block_hash,
        timestamp,
        replyto_hash,
    )

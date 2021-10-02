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
import pytest
from bitcoin.core import CoreMainParams
from squeak.core.signing import CSigningKey

from squeaknode.bitcoin.block_info import BlockInfo
from squeaknode.core.squeaks import check_squeak
from squeaknode.core.squeaks import make_squeak_with_block


@pytest.fixture
def signing_key():
    yield CSigningKey.generate()


@pytest.fixture
def genesis_block_info():
    yield BlockInfo(
        block_height=0,
        block_hash=CoreMainParams.GENESIS_BLOCK.GetHash(),
        block_header=CoreMainParams.GENESIS_BLOCK.get_header().serialize(),
    )


def test_make_squeak_with_block(signing_key, genesis_block_info):
    squeak, secret_key = make_squeak_with_block(
        signing_key,
        "hello!",
        genesis_block_info.block_height,
        genesis_block_info.block_hash,
    )

    check_squeak(squeak)
    assert squeak.nBlockHeight == 0

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
import mock
import pytest

from squeaknode.node.active_download_manager import HashDownload


@pytest.fixture()
def download_hash(squeak_hash):
    yield HashDownload(limit=1, squeak_hash=squeak_hash)


def test_download_hash_is_interested(download_hash, squeak):

    assert download_hash.is_interested(squeak)


def test_download_hash_mark_complete(download_hash, squeak):
    with mock.patch.object(download_hash, 'mark_complete', autospec=True) as mock_mark_complete:
        mock_mark_complete.return_value = None
        download_hash.increment()

        mock_mark_complete.assert_called_once_with()


def test_download_hash_mark_complete_not_called(download_hash, squeak):
    with mock.patch.object(download_hash, 'mark_complete', autospec=True) as mock_mark_complete:
        mock_mark_complete.return_value = None

        mock_mark_complete.assert_not_called()

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

from squeaknode.node.price_policy import PricePolicy


@pytest.fixture()
def price_policy():
    yield PricePolicy(None, None)


def test_get_price(price_policy, squeak, peer_address):
    with mock.patch.object(price_policy, 'get_peer', autospec=True) as mock_get_peer, \
            mock.patch.object(price_policy, 'get_profile', autospec=True) as mock_get_profile, \
            mock.patch.object(price_policy, 'get_default_price', autospec=True) as mock_get_default_price:
        mock_get_peer.return_value = None
        mock_get_profile.return_value = None
        mock_get_default_price.return_value = 555

        assert price_policy.get_price(squeak, peer_address) == 555


def test_get_price_profile_custom_price(price_policy, squeak, peer_address, signing_profile):
    with mock.patch.object(price_policy, 'get_peer', autospec=True) as mock_get_peer, \
            mock.patch.object(price_policy, 'get_profile', autospec=True) as mock_get_profile, \
            mock.patch.object(price_policy, 'get_default_price', autospec=True) as mock_get_default_price:
        mock_get_peer.return_value = None
        mock_get_profile.return_value = signing_profile._replace(
            use_custom_price=True,
            custom_price_msat=54321,
        )
        mock_get_default_price.return_value = 555

        assert price_policy.get_price(squeak, peer_address) == 54321


def test_get_price_profile_no_custom_price(price_policy, squeak, peer_address, signing_profile):
    with mock.patch.object(price_policy, 'get_peer', autospec=True) as mock_get_peer, \
            mock.patch.object(price_policy, 'get_profile', autospec=True) as mock_get_profile, \
            mock.patch.object(price_policy, 'get_default_price', autospec=True) as mock_get_default_price:
        mock_get_peer.return_value = None
        mock_get_profile.return_value = signing_profile._replace(
            use_custom_price=False,
            custom_price_msat=54321,
        )
        mock_get_default_price.return_value = 555

        assert price_policy.get_price(squeak, peer_address) == 555


def test_get_price_profile_share_free_peer(price_policy, squeak, peer_address, peer):
    with mock.patch.object(price_policy, 'get_peer', autospec=True) as mock_get_peer, \
            mock.patch.object(price_policy, 'get_profile', autospec=True) as mock_get_profile, \
            mock.patch.object(price_policy, 'get_default_price', autospec=True) as mock_get_default_price:
        mock_get_peer.return_value = peer._replace(
            share_for_free=True,
        )
        mock_get_profile.return_value = None
        mock_get_default_price.return_value = 555

        assert price_policy.get_price(squeak, peer_address) == 0


def test_get_price_profile_no_share_free_peer(price_policy, squeak, peer_address, peer):
    with mock.patch.object(price_policy, 'get_peer', autospec=True) as mock_get_peer, \
            mock.patch.object(price_policy, 'get_profile', autospec=True) as mock_get_profile, \
            mock.patch.object(price_policy, 'get_default_price', autospec=True) as mock_get_default_price:
        mock_get_peer.return_value = peer._replace(
            share_for_free=False,
        )
        mock_get_profile.return_value = None
        mock_get_default_price.return_value = 555

        assert price_policy.get_price(squeak, peer_address) == 555

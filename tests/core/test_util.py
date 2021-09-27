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
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress
from squeak.net import CInterested

from squeaknode.core.util import get_differential_squeaks


def gen_address():
    signing_key = CSigningKey.generate()
    verifying_key = signing_key.get_verifying_key()
    return CSqueakAddress.from_verifying_key(verifying_key)


def gen_squeak_addresses(n):
    return [gen_address() for i in range(n)]


def test_get_differential_squeaks():
    squeak_addresses = tuple(gen_squeak_addresses(3))
    old_interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )
    interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=11,
        nMaxBlockHeight=21,
    )

    differential_results = get_differential_squeaks(interest, old_interest)
    first_result = next(differential_results)
    assert first_result.addresses == squeak_addresses
    assert first_result.nMinBlockHeight == 21
    assert first_result.nMaxBlockHeight == 21


def test_get_differential_squeaks_no_difference():
    squeak_addresses = tuple(gen_squeak_addresses(3))
    old_interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )
    interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )

    differential_results = get_differential_squeaks(interest, old_interest)
    with pytest.raises(StopIteration):
        next(differential_results)


def test_get_differential_squeaks_new_addresses():
    squeak_addresses = tuple(gen_squeak_addresses(3))
    old_interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )
    additional_addresses = tuple(gen_squeak_addresses(3))
    interest = CInterested(
        addresses=tuple(list(squeak_addresses) + list(additional_addresses)),
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )

    differential_results = get_differential_squeaks(interest, old_interest)
    first_result = next(differential_results)
    print(first_result.addresses)
    print(additional_addresses)
    assert set(first_result.addresses) == set(additional_addresses)
    assert first_result.nMinBlockHeight == 10
    assert first_result.nMaxBlockHeight == 20


def test_get_differential_squeaks_default_min():
    squeak_addresses = tuple(gen_squeak_addresses(3))
    old_interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )
    interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=-1,
        nMaxBlockHeight=20,
    )

    differential_results = get_differential_squeaks(interest, old_interest)
    first_result = next(differential_results)
    assert first_result.addresses == squeak_addresses
    assert first_result.nMinBlockHeight == -1
    assert first_result.nMaxBlockHeight == 9


def test_get_differential_squeaks_default_max():
    squeak_addresses = tuple(gen_squeak_addresses(3))
    old_interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )
    interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=-1,
    )

    differential_results = get_differential_squeaks(interest, old_interest)
    first_result = next(differential_results)
    assert first_result.addresses == squeak_addresses
    assert first_result.nMinBlockHeight == 21
    assert first_result.nMaxBlockHeight == -1


def test_get_differential_squeaks_new_addresses_and_min_max():
    squeak_addresses = tuple(gen_squeak_addresses(3))
    old_interest = CInterested(
        addresses=squeak_addresses,
        nMinBlockHeight=10,
        nMaxBlockHeight=20,
    )
    new_addresses = tuple(gen_squeak_addresses(3))
    interest = CInterested(
        addresses=new_addresses,
        nMinBlockHeight=-1,
        nMaxBlockHeight=-1,
    )

    differential_results = get_differential_squeaks(interest, old_interest)
    first_result = next(differential_results)
    assert set(first_result.addresses) == set(squeak_addresses)
    assert first_result.nMinBlockHeight == -1
    assert first_result.nMaxBlockHeight == 9

    second_result = next(differential_results)
    assert set(second_result.addresses) == set(squeak_addresses)
    assert second_result.nMinBlockHeight == 21
    assert second_result.nMaxBlockHeight == -1

    third_result = next(differential_results)
    assert set(third_result.addresses) == set(new_addresses)
    assert third_result.nMinBlockHeight == -1
    assert third_result.nMaxBlockHeight == -1

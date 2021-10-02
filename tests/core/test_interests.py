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
import os
import uuid

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress
from squeak.net import CInterested

from squeaknode.core.interests import get_differential_squeaks
from squeaknode.core.interests import squeak_matches_interest
from squeaknode.core.squeaks import HASH_LENGTH
from squeaknode.core.squeaks import make_squeak_with_block


def gen_signing_key():
    return CSigningKey.generate()


def gen_random_hash():
    return os.urandom(HASH_LENGTH)


def address_from_signing_key(signing_key):
    verifying_key = signing_key.get_verifying_key()
    return CSqueakAddress.from_verifying_key(verifying_key)


def gen_address():
    signing_key = gen_signing_key()
    return address_from_signing_key(signing_key)


def gen_squeak_addresses(n):
    return [gen_address() for i in range(n)]


def gen_squeak(signing_key, block_height, replyto_hash=None):
    random_content = "random_content_{}".format(uuid.uuid1())
    random_hash = gen_random_hash()
    squeak, secret_key = make_squeak_with_block(
        signing_key,
        random_content,
        block_height,
        random_hash,
        replyto_hash=replyto_hash,
    )
    return squeak


def test_squeak_matches_interest():
    signing_key = gen_signing_key()
    address = address_from_signing_key(signing_key)
    squeak = gen_squeak(signing_key, 5678)
    interest = CInterested(
        addresses=(address,),
        nMinBlockHeight=5000,
        nMaxBlockHeight=6000,
    )

    assert squeak_matches_interest(squeak, interest)


def test_squeak_matches_interest_empty_addresses():
    signing_key = gen_signing_key()
    address_from_signing_key(signing_key)
    squeak = gen_squeak(signing_key, 5678)
    interest = CInterested(
        nMinBlockHeight=5000,
        nMaxBlockHeight=6000,
    )

    assert squeak_matches_interest(squeak, interest)


def test_squeak_matches_interest_above_block_range():
    signing_key = gen_signing_key()
    address = address_from_signing_key(signing_key)
    squeak = gen_squeak(signing_key, 5678)
    interest = CInterested(
        addresses=(address,),
        nMinBlockHeight=4000,
        nMaxBlockHeight=5000,
    )

    assert not squeak_matches_interest(squeak, interest)


def test_squeak_matches_interest_below_block_range():
    signing_key = gen_signing_key()
    address = address_from_signing_key(signing_key)
    squeak = gen_squeak(signing_key, 5678)
    interest = CInterested(
        addresses=(address,),
        nMinBlockHeight=6000,
        nMaxBlockHeight=7000,
    )

    assert not squeak_matches_interest(squeak, interest)


def test_squeak_matches_interest_address_no_match():
    signing_key = gen_signing_key()
    address_from_signing_key(signing_key)
    squeak = gen_squeak(signing_key, 5678)
    other_addresses = tuple(gen_squeak_addresses(3))
    interest = CInterested(
        addresses=other_addresses,
        nMinBlockHeight=5000,
        nMaxBlockHeight=6000,
    )

    assert not squeak_matches_interest(squeak, interest)


def test_squeak_matches_interest_is_reply():
    signing_key = gen_signing_key()
    address_from_signing_key(signing_key)
    replyto_hash = gen_random_hash()
    squeak = gen_squeak(signing_key, 5678, replyto_hash=replyto_hash)
    interest = CInterested(
        hashReplySqk=replyto_hash,
    )

    assert squeak_matches_interest(squeak, interest)


def test_squeak_matches_interest_is_not_reply():
    signing_key = gen_signing_key()
    address_from_signing_key(signing_key)
    replyto_hash = gen_random_hash()
    squeak = gen_squeak(signing_key, 5678, replyto_hash=replyto_hash)
    other_replyto_hash = gen_random_hash()
    interest = CInterested(
        hashReplySqk=other_replyto_hash,
    )

    assert not squeak_matches_interest(squeak, interest)


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
    differential_results = list(
        get_differential_squeaks(interest, old_interest))

    assert differential_results == [
        CInterested(
            addresses=squeak_addresses,
            nMinBlockHeight=21,
            nMaxBlockHeight=21,
        )
    ]


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
    differential_results = list(
        get_differential_squeaks(interest, old_interest))

    assert differential_results == []


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
    differential_results = list(
        get_differential_squeaks(interest, old_interest))

    assert len(differential_results) == 1
    first_result = differential_results[0]
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
    differential_results = list(
        get_differential_squeaks(interest, old_interest))

    assert differential_results == [
        CInterested(
            addresses=squeak_addresses,
            nMinBlockHeight=-1,
            nMaxBlockHeight=9,
        )
    ]


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
    differential_results = list(
        get_differential_squeaks(interest, old_interest))

    assert differential_results == [
        CInterested(
            addresses=squeak_addresses,
            nMinBlockHeight=21,
            nMaxBlockHeight=-1,
        )
    ]


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

    differential_results = list(
        get_differential_squeaks(interest, old_interest))
    assert len(differential_results) == 3

    first_result = differential_results[0]
    assert set(first_result.addresses) == set(squeak_addresses)
    assert first_result.nMinBlockHeight == -1
    assert first_result.nMaxBlockHeight == 9

    second_result = differential_results[1]
    assert set(second_result.addresses) == set(squeak_addresses)
    assert second_result.nMinBlockHeight == 21
    assert second_result.nMaxBlockHeight == -1

    third_result = differential_results[2]
    assert set(third_result.addresses) == set(new_addresses)
    assert third_result.nMinBlockHeight == -1
    assert third_result.nMaxBlockHeight == -1

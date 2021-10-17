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
from typing import Optional

from bitcoin.base58 import Base58ChecksumError
from bitcoin.wallet import CBitcoinAddressError
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.core.squeak_profile import SqueakProfile


def create_signing_profile(profile_name: str, private_key: Optional[str] = None) -> SqueakProfile:
    validate_profile_name(profile_name)
    if private_key is None:
        signing_key = CSigningKey.generate()
    else:
        signing_key = CSigningKey(private_key)
    verifying_key = signing_key.get_verifying_key()
    address = CSqueakAddress.from_verifying_key(verifying_key)
    signing_key_str = str(signing_key)
    signing_key_bytes = signing_key_str.encode()
    return SqueakProfile(
        profile_name=profile_name,
        private_key=signing_key_bytes,
        address=str(address),
        following=True,
    )


def create_contact_profile(profile_name: str, squeak_address: str) -> SqueakProfile:
    validate_profile_name(profile_name)
    try:
        CSqueakAddress(squeak_address)
    except (Base58ChecksumError, CBitcoinAddressError):
        raise Exception(
            "Invalid squeak address: {}".format(
                squeak_address
            ),
        )
    return SqueakProfile(
        profile_name=profile_name,
        address=squeak_address,
    )


def validate_profile_name(profile_name: str) -> None:
    if len(profile_name) == 0:
        raise Exception(
            "Profile name cannot be empty.",
        )


def get_profile_private_key(profile: SqueakProfile) -> bytes:
    if profile.private_key is None:
        raise Exception("Profile: {} does not have a private key.".format(
            profile,
        ))
    return profile.private_key

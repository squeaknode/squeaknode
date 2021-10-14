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
from squeaknode.admin.messages import message_to_peer_address
from squeaknode.admin.messages import peer_address_to_message
from squeaknode.admin.messages import squeak_entry_to_message
from squeaknode.admin.messages import squeak_profile_to_message


def test_peer_address_to_message(peer_address, peer_address_message):
    msg = peer_address_to_message(peer_address)

    assert msg == peer_address_message


def test_msg_to_peer_address(peer_address, peer_address_message):
    address = message_to_peer_address(peer_address_message)

    assert address == peer_address


def test_squeak_entry_to_message(squeak_entry_locked, squeak_entry_msg_locked):
    msg = squeak_entry_to_message(squeak_entry_locked)

    assert msg == squeak_entry_msg_locked


def test_profile_to_message(signing_profile, signing_profile_msg):
    msg = squeak_profile_to_message(signing_profile)

    assert msg == signing_profile_msg

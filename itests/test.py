# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide client."""
from __future__ import print_function

import logging
import random
import time

from squeak.core import CSqueak

import grpc
import route_guide_pb2
import route_guide_pb2_grpc


def build_squeak_msg(squeak):
    return route_guide_pb2.Squeak(
        hash=squeak.GetHash(),
        serialized_squeak=squeak.serialize(),
    )


def squeak_from_msg(squeak_msg):
    if not squeak_msg:
        return None
    if not squeak_msg.serialized_squeak:
        return None
    return CSqueak.deserialize(squeak_msg.serialized_squeak)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('sqkclient_alice:50051') as alice_channel, \
         grpc.insecure_channel('sqkclient_bob:50051') as bob_channel, \
         grpc.insecure_channel('sqkclient_carol:50051') as carol_channel:

        # Make the stubs
        alice_stub = route_guide_pb2_grpc.RouteGuideStub(alice_channel)
        bob_stub = route_guide_pb2_grpc.RouteGuideStub(bob_channel)
        carol_stub = route_guide_pb2_grpc.RouteGuideStub(carol_channel)

        print("-------------- WalletBalance --------------")
        balance = alice_stub.WalletBalance(route_guide_pb2.WalletBalanceRequest())
        print("Balance: %s" % balance)
        print("Balance confirmed %s %s" % (balance.total_balance, balance.total_balance))
        assert balance.total_balance == 1505000000000

        print("-------------- MakeSqueak --------------")
        squeak_resp_msg = alice_stub.MakeSqueak(route_guide_pb2.MakeSqueakRequest(
            content='hello squeak.',
        ))
        print("squeak_resp_msg: %s" % squeak_resp_msg.squeak)
        squeak_resp = squeak_from_msg(squeak_resp_msg.squeak)
        print("squeak: %s" % squeak_resp)
        assert squeak_resp.GetDecryptedContentStr() == 'hello squeak.'

        print("-------------- GetSqueak --------------")
        get_squeak_resp_msg = alice_stub.GetSqueak(route_guide_pb2.GetSqueakRequest(
            hash=squeak_resp.GetHash(),
        ))
        get_squeak_resp = squeak_from_msg(get_squeak_resp_msg.squeak)
        print("get_squeak_resp: %s" % get_squeak_resp)
        assert get_squeak_resp.GetDecryptedContentStr() == 'hello squeak.'

        print("-------------- GetSqueak from other client --------------")
        bob_get_squeak_resp_msg = bob_stub.GetSqueak(route_guide_pb2.GetSqueakRequest(
            hash=squeak_resp.GetHash(),
        ))
        print("bob_get_squeak_resp_msg: %s" % bob_get_squeak_resp_msg.squeak)
        bob_get_squeak_resp = squeak_from_msg(bob_get_squeak_resp_msg.squeak)
        print("bob_get_squeak_resp: %s" % bob_get_squeak_resp)
        assert bob_get_squeak_resp.GetDecryptedContentStr()  == 'hello squeak.'


if __name__ == '__main__':
    logging.basicConfig()
    run()

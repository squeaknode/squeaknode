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


from bitcoin.core import lx, x
from squeak.core import CSqueak
from squeak.core import HASH_LENGTH
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey


import lnd_pb2 as ln
import lnd_pb2_grpc as lnrpc

import grpc
import route_guide_pb2
import route_guide_pb2_grpc
import squeak_server_pb2
import squeak_server_pb2_grpc

from lnd_lightning_client import LNDLightningClient


def build_squeak_msg(squeak):
    return route_guide_pb2.Squeak(
        hash=squeak.GetHash(),
        serialized_squeak=squeak.serialize(),
    )

def build_squeak_msg_2(squeak):
    return squeak_server_pb2.Squeak(
        hash=squeak.GetHash(),
        serialized_squeak=squeak.serialize(),
    )


def squeak_from_msg(squeak_msg):
    if not squeak_msg:
        return None
    if not squeak_msg.serialized_squeak:
        return None
    return CSqueak.deserialize(squeak_msg.serialized_squeak)


def generate_signing_key():
    return CSigningKey.generate()


def make_squeak(signing_key: CSigningKey, content: str, reply_to: bytes = b'\x00'*HASH_LENGTH):
    block_height = 0
    block_hash = lx('4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b')
    timestamp = int(time.time())
    return MakeSqueakFromStr(
        signing_key,
        content,
        block_height,
        block_hash,
        timestamp,
    )


def load_lightning_client() -> LNDLightningClient:
    return LNDLightningClient(
        'lnd',
        10009,
        'simnet',
        ln,
        lnrpc,
    )


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('sqkserver:50052') as server_channel, \
         grpc.insecure_channel('sqkclient_alice:50051') as alice_channel, \
         grpc.insecure_channel('sqkclient_bob:50051') as bob_channel, \
         grpc.insecure_channel('sqkclient_carol:50051') as carol_channel:

        # load lnd client
        lnd_lightning_client = load_lightning_client()
        balance_from_client = lnd_lightning_client.get_wallet_balance()
        print("Balance from direct client: %s" % balance_from_client)
        assert balance_from_client.total_balance == 1505000000000

        # Make the stubs
        server_stub = squeak_server_pb2_grpc.SqueakServerStub(server_channel)
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


        # Make a direct request to the server
        server_response = server_stub.GetSqueak(squeak_server_pb2.GetSqueakRequest(hash=squeak_resp.GetHash()))
        print("Direct server response: " + str(server_response.squeak))
        server_response_squeak = squeak_from_msg(server_response.squeak)
        assert server_response_squeak.GetDecryptedContentStr()  == 'hello squeak.'

        # Post a squeak with a direct request to the server
        signing_key = generate_signing_key()
        direct_squeak = make_squeak(signing_key, 'hello from itest!')

        direct_squeak_msg = build_squeak_msg_2(direct_squeak)
        server_post_response = server_stub.PostSqueak(squeak_server_pb2.PostSqueakRequest(squeak=direct_squeak_msg))
        print("Direct server post response: " + str(server_post_response))
        assert server_post_response.hash == direct_squeak.GetHash()


if __name__ == '__main__':
    logging.basicConfig()
    run()

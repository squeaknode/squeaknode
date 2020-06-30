from __future__ import print_function

import logging
import random
import time

from bitcoin.core import lx, x
from squeak.params import SelectParams
from squeak.core import CSqueak
from squeak.core import CheckSqueak
from squeak.core import HASH_LENGTH
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

import lnd_pb2 as ln
import lnd_pb2_grpc as lnrpc

import grpc
import squeak_server_pb2
import squeak_server_pb2_grpc

from lnd_lightning_client import LNDLightningClient


def build_squeak_msg(squeak):
    return squeak_server_pb2.Squeak(
        hash=get_hash(squeak),
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


def get_address(signing_key):
    verifying_key = signing_key.get_verifying_key()
    address = CSqueakAddress.from_verifying_key(verifying_key)
    return str(address)


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


def get_hash(squeak):
    """ Needs to be reversed because hash is stored as little-endian """
    return squeak.GetHash()[::-1]


def load_lightning_client() -> LNDLightningClient:
    tls_cert_path = '~/.lnd/tls.cert'
    macaroon_path = '~/.lnd/data/chain/bitcoin/simnet/admin.macaroon'
    return LNDLightningClient(
        'lnd',
        10009,
        tls_cert_path,
        macaroon_path,
        ln,
        lnrpc,
    )



def bxor(b1, b2): # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


def run():
    # Set the network to simnet for itest.
    SelectParams("mainnet")

    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('sqkserver:8774') as server_channel:

        # load lnd client
        lnd_lightning_client = load_lightning_client()
        balance_from_client = lnd_lightning_client.get_wallet_balance()
        print("Balance from direct client: %s" % balance_from_client)
        assert balance_from_client.total_balance >= 1505000000000

        # Make the stubs
        server_stub = squeak_server_pb2_grpc.SqueakServerStub(server_channel)

        # Post a squeak with a direct request to the server
        signing_key = generate_signing_key()
        squeak = make_squeak(signing_key, 'hello from itest!')
        squeak_hash = get_hash(squeak)

        squeak_msg = build_squeak_msg(squeak)
        post_response = server_stub.PostSqueak(squeak_server_pb2.PostSqueakRequest(squeak=squeak_msg))
        print("Direct server post response: " + str(post_response))

        # Get the same squeak from the server
        get_response = server_stub.GetSqueak(squeak_server_pb2.GetSqueakRequest(hash=squeak_hash))
        print("Direct server get response: " + str(get_response))
        get_response_squeak = squeak_from_msg(get_response.squeak)
        CheckSqueak(get_response_squeak, skipDecryptionCheck=True)
        assert get_hash(get_response_squeak) == get_hash(squeak)

        # Lookup squeaks based on address
        signing_address = get_address(signing_key)
        addresses = [
            signing_address,
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
        ]
        lookup_response = server_stub.LookupSqueaks(squeak_server_pb2.LookupSqueaksRequest(
            addresses=addresses,
            min_block=0,
            max_block=99999999,
        ))
        print("Lookup response: " + str(lookup_response))
        assert get_hash(squeak) in set(lookup_response.hashes)

        # Lookup again without the relevant address
        addresses = [
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
        ]
        lookup_response = server_stub.LookupSqueaks(squeak_server_pb2.LookupSqueaksRequest(
            addresses=addresses,
            min_block=0,
            max_block=99999999,
        ))
        assert get_hash(squeak) not in set(lookup_response.hashes)

        # Lookup again with a different block range
        addresses = [
            signing_address,
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
        ]
        lookup_response = server_stub.LookupSqueaks(squeak_server_pb2.LookupSqueaksRequest(
            addresses=addresses,
            min_block=600,
            max_block=99999999,
        ))
        assert get_hash(squeak) not in set(lookup_response.hashes)

        # Buy the squeak data key
        buy_response = server_stub.BuySqueak(squeak_server_pb2.BuySqueakRequest(hash=squeak_hash))
        print("Server buy response: " + str(buy_response))
        assert buy_response.offer.payment_request.startswith('ln')

        # Connect to the server lightning node
        connect_peer_response = lnd_lightning_client.connect_peer(buy_response.offer.pubkey, buy_response.offer.host)
        print("Server connect peer response: " + str(connect_peer_response))

        # List peers
        list_peers_response = lnd_lightning_client.list_peers()
        print("Server list peers response: " + str(list_peers_response))

        # Open channel to the server lightning node
        open_channel_response = lnd_lightning_client.open_channel_sync(buy_response.offer.pubkey, 1000000)
        print("Server open channel response: " + str(open_channel_response))

        # List channels
        list_channels_response = lnd_lightning_client.list_channels()
        print("Server list channels response: " + str(list_channels_response))

        # Sleep for 60 seconds to confirm the channel open transaction
        time.sleep(60)

        # List channels
        list_channels_response = lnd_lightning_client.list_channels()
        print("Server list channels response: " + str(list_channels_response))

        # Pay the invoice
        payment = lnd_lightning_client.pay_invoice_sync(buy_response.offer.payment_request)
        print("Server pay invoice response: " + str(payment))
        preimage = payment.payment_preimage
        print("preimage: " + str(preimage))

        # Clear the data key from the squeak and verify with the payment preimage
        new_data_key = bxor(buy_response.offer.nonce, preimage)
        print("new data key: " + str(new_data_key))
        get_response_squeak.SetDataKey(new_data_key)
        CheckSqueak(get_response_squeak)
        assert get_response_squeak.GetDecryptedContentStr() == 'hello from itest!'
        print("Finished checking squeak.")



if __name__ == '__main__':
    logging.basicConfig()
    run()

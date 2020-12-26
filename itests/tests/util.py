from __future__ import print_function

import time
from contextlib import contextmanager

from lnd_lightning_client import LNDLightningClient
from squeak.core import HASH_LENGTH, CSqueak, MakeSqueakFromStr
from squeak.core.elliptic import scalar_difference, scalar_from_bytes, scalar_to_bytes
from squeak.core.signing import CSigningKey, CSqueakAddress

from proto import squeak_server_pb2


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


def get_latest_block_info(lightning_client):
    get_info_response = lightning_client.get_info()
    block_hash = bytes.fromhex(get_info_response.block_hash)
    block_height = get_info_response.block_height
    return block_hash, block_height


def make_squeak(
    signing_key: CSigningKey,
    content: str,
    block_height,
    block_hash,
    reply_to: bytes = b"\x00" * HASH_LENGTH,
):
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
    hash_bytes = squeak.GetHash()[::-1]
    return hash_bytes.hex()


def load_lightning_client() -> LNDLightningClient:
    tls_cert_path = "~/.lnd/tls.cert"
    macaroon_path = "~/.lnd/data/chain/bitcoin/simnet/admin.macaroon"
    return LNDLightningClient(
        "lnd",
        10009,
        tls_cert_path,
        macaroon_path,
    )


def bxor(b1, b2):  # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


def string_to_hex(s):
    return bytes.fromhex(s)


def subtract_tweak(n, tweak):
    n_int = scalar_from_bytes(n)
    tweak_int = scalar_from_bytes(tweak)
    sum_int = scalar_difference(n_int, tweak_int)
    return scalar_to_bytes(sum_int)


@contextmanager
def connect_peer(lightning_client, lightning_host, remote_pubkey):
    # Connect the peer
    lightning_client.connect_peer(remote_pubkey, lightning_host)
    try:
        yield
    finally:
        # Disconnect the peer
        lightning_client.disconnect_peer(
            remote_pubkey,
        )


@contextmanager
def open_channel(lightning_client, remote_pubkey, amount):
    # Open channel to the server lightning node
    pubkey_bytes = string_to_hex(remote_pubkey)
    open_channel_response = lightning_client.open_channel(pubkey_bytes, amount)
    print("Opening channel...")
    for update in open_channel_response:
        if update.HasField("chan_open"):
            channel_point = update.chan_open.channel_point
            print("Channel now open: " + str(channel_point))
            break
    try:
        yield
    finally:
        # Code to release resource, e.g.:
        # Close the channel
        time.sleep(2)
        for update in lightning_client.close_channel(channel_point):
            if update.HasField("chan_close"):
                print("Channel closed.")
                break

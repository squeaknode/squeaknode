from __future__ import print_function

import logging
import time

import grpc
from lnd_lightning_client import LNDLightningClient
from squeak.core import HASH_LENGTH, CheckSqueak, CSqueak, MakeSqueakFromStr
from squeak.core.encryption import CEncryptedDecryptionKey, generate_data_key
from squeak.core.signing import CSigningKey, CSqueakAddress
from squeak.params import SelectParams

from proto import lnd_pb2 as ln
from proto import lnd_pb2_grpc as lnrpc
from proto import (
    squeak_admin_pb2,
    squeak_admin_pb2_grpc,
    squeak_server_pb2,
    squeak_server_pb2_grpc,
)


def build_squeak_msg(squeak):
    return squeak_server_pb2.Squeak(
        hash=get_hash(squeak), serialized_squeak=squeak.serialize(),
    )


def squeak_from_msg(squeak_msg):
    if not squeak_msg:
        return None
    if not squeak_msg.serialized_squeak:
        return None
    return CSqueak.deserialize(squeak_msg.serialized_squeak)


def generate_signing_key():
    return CSigningKey.generate()


def generate_challenge_proof():
    return generate_data_key()


def get_challenge(encryption_key, challenge_proof):
    return encryption_key.encrypt(challenge_proof)


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
    return MakeSqueakFromStr(signing_key, content, block_height, block_hash, timestamp,)


def get_hash(squeak):
    """ Needs to be reversed because hash is stored as little-endian """
    return squeak.GetHash()[::-1]


def load_lightning_client() -> LNDLightningClient:
    tls_cert_path = "~/.lnd/tls.cert"
    macaroon_path = "~/.lnd/data/chain/bitcoin/simnet/admin.macaroon"
    return LNDLightningClient("lnd", 10009, tls_cert_path, macaroon_path, ln, lnrpc,)


def bxor(b1, b2):  # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return bytes(result)


def string_to_hex(s):
    return bytes.fromhex(s)

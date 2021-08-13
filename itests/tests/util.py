from __future__ import print_function

import base64
import time
from contextlib import contextmanager

from lnd_lightning_client import LNDLightningClient
from squeak.core import HASH_LENGTH
from squeak.core import MakeSqueakFromStr
from squeak.core.elliptic import scalar_difference
from squeak.core.elliptic import scalar_from_bytes
from squeak.core.elliptic import scalar_to_bytes
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from proto import squeak_admin_pb2


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


def bytes_to_base64_string(data: bytes) -> str:
    encoded_string = base64.b64encode(data)
    return encoded_string.decode('utf-8')


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
        time.sleep(2)


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


@contextmanager
def open_peer_connection(node_stub, peer_name, peer_host, peer_port):
    # Add the main node as a peer
    create_peer_response = node_stub.CreatePeer(
        squeak_admin_pb2.CreatePeerRequest(
            peer_name=peer_name,
            host=peer_host,
            port=peer_port,
        )
    )
    peer_id = create_peer_response.peer_id
    try:
        # Set the peer to be downloading
        node_stub.SetPeerDownloading(
            squeak_admin_pb2.SetPeerDownloadingRequest(
                peer_id=peer_id,
                downloading=True,
            )
        )
        # Connect the peer
        node_stub.ConnectPeer(
            squeak_admin_pb2.ConnectPeerRequest(
                host=peer_host,
                port=peer_port,
            )
        )
        yield peer_id
    except Exception as e:
        print("Failed to connect to peer: {}:{}.".format(peer_host, peer_port))
        print(e)
    finally:
        # Disconnect the peer
        node_stub.DisconnectPeer(
            squeak_admin_pb2.DisconnectPeerRequest(
                peer_id=peer_id,
            )
        )
        # Delete the peer
        node_stub.DeletePeer(
            squeak_admin_pb2.DeletePeerRequest(
                peer_id=peer_id,
            )
        )


def get_connected_peers(node_stub):
    get_connected_peers_response = node_stub.GetConnectedPeers(
        squeak_admin_pb2.GetConnectedPeersRequest()
    )
    return get_connected_peers_response.connected_peers

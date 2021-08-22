from __future__ import print_function

import base64
import queue
import threading
import time
from contextlib import contextmanager

from lnd_lightning_client import LNDLightningClient
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


# def make_squeak(
#     signing_key: CSigningKey,
#     content: str,
#     block_height,
#     block_hash,
#     reply_to: bytes = b"\x00" * HASH_LENGTH,
# ):
#     timestamp = int(time.time())
#     return MakeSqueakFromStr(
#         signing_key,
#         content,
#         block_height,
#         block_hash,
#         timestamp,
#     )


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
    peer_id = create_saved_peer(
        node_stub,
        peer_name,
        peer_host,
        peer_port,
    )
    try:
        # Connect the peer
        node_stub.ConnectPeer(
            squeak_admin_pb2.ConnectPeerRequest(
                peer_address=squeak_admin_pb2.PeerAddress(
                    host=peer_host,
                    port=peer_port,
                )
            )
        )
        yield peer_id
    except Exception as e:
        print("Failed to connect to peer: {}:{}.".format(peer_host, peer_port))
        print(e)
        raise
    finally:
        # Disconnect the peer
        node_stub.DisconnectPeer(
            squeak_admin_pb2.DisconnectPeerRequest(
                peer_address=squeak_admin_pb2.PeerAddress(
                    host=peer_host,
                    port=peer_port,
                )
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


def get_connected_peer(node_stub, host, port):
    get_connected_peer_response = node_stub.GetConnectedPeer(
        squeak_admin_pb2.GetConnectedPeerRequest(
            peer_address=squeak_admin_pb2.PeerAddress(
                host=host,
                port=port,
            )
        )
    )
    return get_connected_peer_response.connected_peer


def create_saved_peer(node_stub, name, host, port):
    create_peer_response = node_stub.CreatePeer(
        squeak_admin_pb2.CreatePeerRequest(
            peer_name=name,
            peer_address=squeak_admin_pb2.PeerAddress(
                host=host,
                port=port,
            )
        )
    )
    return create_peer_response.peer_id


@contextmanager
def subscribe_connected_peers(node_stub):
    q = queue.Queue()
    subscribe_connected_peers_response = node_stub.SubscribeConnectedPeers(
        squeak_admin_pb2.SubscribeConnectedPeersRequest()
    )

    def enqueue_results():
        for result in subscribe_connected_peers_response:
            q.put(result.connected_peers)

    threading.Thread(
        target=enqueue_results,
    ).start()
    yield q
    subscribe_connected_peers_response.cancel()


def get_squeak_display(node_stub, squeak_hash):
    get_squeak_display_response = node_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=squeak_hash,
        )
    )
    if not get_squeak_display_response.HasField("squeak_display_entry"):
        return None
    return get_squeak_display_response.squeak_display_entry


def download_squeak(node_stub, squeak_hash):
    node_stub.SyncSqueak(
        squeak_admin_pb2.SyncSqueakRequest(
            squeak_hash=squeak_hash,
        ),
    )


def download_squeaks(node_stub):
    node_stub.SyncSqueaks(
        squeak_admin_pb2.SyncSqueaksRequest(),
    )


def download_offers(node_stub, squeak_hash):
    node_stub.DownloadOffers(
        squeak_admin_pb2.DownloadOffersRequest(
            squeak_hash=squeak_hash,
        ),
    )


def get_squeak_profile(node_stub, profile_id):
    get_squeak_profile_response = node_stub.GetSqueakProfile(
        squeak_admin_pb2.GetSqueakProfileRequest(
            profile_id=profile_id,
        )
    )
    if not get_squeak_profile_response.HasField("squeak_profile"):
        return None
    return get_squeak_profile_response.squeak_profile


def get_network(node_stub):
    get_network_response = node_stub.GetNetwork(
        squeak_admin_pb2.GetNetworkRequest()
    )
    return get_network_response.network


def make_squeak(node_stub, profile_id, squeak_content, reply_to_hash=None):
    make_squeak_response = node_stub.MakeSqueak(
        squeak_admin_pb2.MakeSqueakRequest(
            profile_id=profile_id,
            content=squeak_content,
            replyto=reply_to_hash,
        )
    )
    return make_squeak_response.squeak_hash


def delete_squeak(node_stub, squeak_hash):
    node_stub.DeleteSqueak(
        squeak_admin_pb2.DeleteSqueakRequest(squeak_hash=squeak_hash)
    )


def create_contact_profile(node_stub, profile_name, squeak_address):
    create_contact_profile_response = node_stub.CreateContactProfile(
        squeak_admin_pb2.CreateContactProfileRequest(
            profile_name=profile_name,
            address=squeak_address,
        )
    )
    return create_contact_profile_response.profile_id


def create_signing_profile(node_stub, profile_name):
    create_signing_profile_response = node_stub.CreateSigningProfile(
        squeak_admin_pb2.CreateSigningProfileRequest(
            profile_name=profile_name,
        )
    )
    return create_signing_profile_response.profile_id


def import_signing_profile(node_stub, profile_name, private_key):
    import_response = node_stub.ImportSigningProfile(
        squeak_admin_pb2.ImportSigningProfileRequest(
            profile_name=profile_name,
            private_key=private_key,
        )
    )
    return import_response.profile_id


def delete_profile(node_stub, profile_id):
    node_stub.DeleteSqueakProfile(
        squeak_admin_pb2.DeleteSqueakProfileRequest(
            profile_id=profile_id,
        )
    )

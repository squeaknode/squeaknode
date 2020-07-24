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


def run():
    # Set the network to simnet for itest.
    SelectParams("mainnet")

    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(
        "sqkserver:8774"
    ) as server_channel, grpc.insecure_channel("sqkserver:8994") as admin_channel:

        # load lnd client
        lnd_lightning_client = load_lightning_client()
        balance_from_client = lnd_lightning_client.get_wallet_balance()
        print("Balance from direct client: %s" % balance_from_client)
        assert balance_from_client.total_balance >= 1505000000000

        # Make the stubs
        server_stub = squeak_server_pb2_grpc.SqueakServerStub(server_channel)
        admin_stub = squeak_admin_pb2_grpc.SqueakAdminStub(admin_channel)

        # Post a squeak with a direct request to the server
        signing_key = generate_signing_key()
        block_height, block_hash = get_latest_block_info(lnd_lightning_client)
        squeak = make_squeak(signing_key, "hello from itest!", block_hash, block_height)
        squeak_hash = get_hash(squeak)

        squeak_msg = build_squeak_msg(squeak)
        post_response = server_stub.PostSqueak(
            squeak_server_pb2.PostSqueakRequest(squeak=squeak_msg)
        )
        print("Direct server post response: " + str(post_response))

        # Wait a few seconds for the squeak to be verified on the server.
        time.sleep(5)

        # Get the same squeak from the server
        get_response = server_stub.GetSqueak(
            squeak_server_pb2.GetSqueakRequest(hash=squeak_hash)
        )
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
        lookup_response = server_stub.LookupSqueaks(
            squeak_server_pb2.LookupSqueaksRequest(
                addresses=addresses, min_block=0, max_block=99999999,
            )
        )
        print("Lookup response: " + str(lookup_response))
        assert get_hash(squeak) in set(lookup_response.hashes)

        # Lookup again without the relevant address
        addresses = [
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
        ]
        lookup_response = server_stub.LookupSqueaks(
            squeak_server_pb2.LookupSqueaksRequest(
                addresses=addresses, min_block=0, max_block=99999999,
            )
        )
        assert get_hash(squeak) not in set(lookup_response.hashes)

        # Lookup again with a different block range
        addresses = [
            signing_address,
            get_address(generate_signing_key()),
            get_address(generate_signing_key()),
        ]
        lookup_response = server_stub.LookupSqueaks(
            squeak_server_pb2.LookupSqueaksRequest(
                addresses=addresses, min_block=600, max_block=99999999,
            )
        )
        assert get_hash(squeak) not in set(lookup_response.hashes)

        # Generate a challenge to verify the offer
        expected_proof = generate_challenge_proof()
        encryption_key = squeak.GetEncryptionKey()
        challenge = get_challenge(encryption_key, expected_proof)

        # Buy the squeak data key
        buy_response = server_stub.BuySqueak(
            squeak_server_pb2.BuySqueakRequest(hash=squeak_hash, challenge=challenge,)
        )
        print("Server buy response: " + str(buy_response))
        assert buy_response.offer.payment_request.startswith("ln")

        # Check the offer challenge proof
        print("Server offer proof: " + str(buy_response.offer.proof))
        assert buy_response.offer.proof == expected_proof

        # Connect to the server lightning node
        connect_peer_response = lnd_lightning_client.connect_peer(
            buy_response.offer.pubkey, buy_response.offer.host
        )
        print("Server connect peer response: " + str(connect_peer_response))

        # List peers
        list_peers_response = lnd_lightning_client.list_peers()
        print("Server list peers response: " + str(list_peers_response))

        # Open channel to the server lightning node
        pubkey_bytes = string_to_hex(buy_response.offer.pubkey)
        open_channel_response = lnd_lightning_client.open_channel(pubkey_bytes, 1000000)
        print("Opening channel...")
        for update in open_channel_response:
            if update.HasField("chan_open"):
                channel_point = update.chan_open.channel_point
                print("Channel now open: " + str(channel_point))
                break

        # List channels
        list_channels_response = lnd_lightning_client.list_channels()
        print("Server list channels response: " + str(list_channels_response))

        # Pay the invoice
        payment = lnd_lightning_client.pay_invoice_sync(
            buy_response.offer.payment_request
        )
        print("Server pay invoice response: " + str(payment))
        preimage = payment.payment_preimage
        print("preimage: " + str(preimage))

        # Verify with the payment preimage and decryption key ciphertext
        decryption_key_cipher_bytes = buy_response.offer.key_cipher
        iv = buy_response.offer.iv
        encrypted_decryption_key = CEncryptedDecryptionKey.from_bytes(
            decryption_key_cipher_bytes
        )

        # Decrypt the decryption key
        decryption_key = encrypted_decryption_key.get_decryption_key(preimage, iv)
        serialized_decryption_key = decryption_key.get_bytes()

        print("new decryption key: " + str(serialized_decryption_key))
        get_response_squeak.SetDecryptionKey(serialized_decryption_key)
        CheckSqueak(get_response_squeak)
        assert get_response_squeak.GetDecryptedContentStr() == "hello from itest!"
        print("Finished checking squeak.")

        # Check the server balance
        get_balance_response = admin_stub.LndWalletBalance(
            ln.WalletBalanceRequest()
        )
        print("Get balance response: " + str(get_balance_response))
        assert get_balance_response.total_balance == 0

        # Create a new signing profile
        profile_name = "bob"
        create_signing_profile_response = admin_stub.CreateSigningProfile(
            squeak_admin_pb2.CreateSigningProfileRequest(profile_name=profile_name,)
        )
        print(
            "Get create signing profile response: "
            + str(create_signing_profile_response)
        )
        profile_id = create_signing_profile_response.profile_id

        # Get the new squeak profile
        get_squeak_profile_response = admin_stub.GetSqueakProfile(
            squeak_admin_pb2.GetSqueakProfileRequest(profile_id=profile_id,)
        )
        print("Get squeak profile response: " + str(get_squeak_profile_response))
        assert get_squeak_profile_response.squeak_profile.profile_name == profile_name
        squeak_profile_address = get_squeak_profile_response.squeak_profile.address

        # Create a new squeak using the new profile
        make_squeak_content = "Hello from the profile on the server!"
        make_squeak_response = admin_stub.MakeSqueak(
            squeak_admin_pb2.MakeSqueakRequest(
                profile_id=profile_id, content=make_squeak_content,
            )
        )
        print("Get make squeak response: " + str(make_squeak_response))
        make_squeak_hash = make_squeak_response.hash
        assert len(make_squeak_hash) == 32

        # Get the new squeak from the server
        get_squeak_response = server_stub.GetSqueak(
            squeak_server_pb2.GetSqueakRequest(hash=make_squeak_hash)
        )
        print("Get squeak response: " + str(get_squeak_response))
        get_squeak_response_squeak = squeak_from_msg(get_squeak_response.squeak)
        CheckSqueak(get_response_squeak, skipDecryptionCheck=True)
        assert get_hash(get_squeak_response_squeak) == make_squeak_hash
        print("Squeak from make squeak request: " + str(get_squeak_response_squeak))

        # Close the channel
        time.sleep(10)
        for update in lnd_lightning_client.close_channel(channel_point):
            if update.HasField("chan_close"):
                print("Channel closed.")
                break

        # Check the server balance
        get_balance_response = admin_stub.LndWalletBalance(
            ln.WalletBalanceRequest()
        )
        print("Get balance response: " + str(get_balance_response))
        assert get_balance_response.total_balance == 1000

        # Get a squeak display item
        get_squeak_display_response = admin_stub.GetSqueakDisplay(
            squeak_admin_pb2.GetSqueakDisplayRequest(hash=make_squeak_hash,)
        )
        print("Get squeak display response: " + str(get_squeak_display_response))
        assert (
            get_squeak_display_response.squeak_display_entry.content_str
            == "Hello from the profile on the server!"
        )

        # Make another squeak
        admin_stub.MakeSqueak(
            squeak_admin_pb2.MakeSqueakRequest(
                profile_id=profile_id, content="Hello again!",
            )
        )

        # Wait a few seconds for the squeak to be verified on the server.
        time.sleep(5)

        # Get all followed squeak display items
        get_followed_squeak_display_response = admin_stub.GetFollowedSqueakDisplays(
            squeak_admin_pb2.GetFollowedSqueakDisplaysRequest()
        )
        print("Get followed squeak displays response: " + str(get_followed_squeak_display_response))
        assert (
            len(get_followed_squeak_display_response.squeak_display_entries) == 2
        )

        # Get all signing profiles
        get_signing_profiles_response = admin_stub.GetSigningProfiles(
            squeak_admin_pb2.GetSigningProfilesRequest()
        )
        print("Get signing profiles response: " + str(get_signing_profiles_response))
        assert (
            len(get_signing_profiles_response.squeak_profiles) == 1
        )

        # Get all squeak displays for the known address
        get_address_squeak_display_response = admin_stub.GetAddressSqueakDisplays(
            squeak_admin_pb2.GetAddressSqueakDisplaysRequest(
                address=squeak_profile_address
            )
        )
        print("Get address squeak displays response: " + str(get_address_squeak_display_response))
        assert (
            len(get_address_squeak_display_response.squeak_display_entries) == 2
        )
        for squeak_display_entry in get_address_squeak_display_response.squeak_display_entries:
            assert squeak_display_entry.author_name == "bob"
            assert squeak_display_entry.author_address == squeak_profile_address

        # Get squeak profile by address
        get_profile_by_address_response = admin_stub.GetSqueakProfileByAddress(
            squeak_admin_pb2.GetSqueakProfileByAddressRequest(
                address=squeak_profile_address
            )
        )
        print("Get profile by address response: " + str(get_profile_by_address_response))
        assert (
            get_profile_by_address_response.squeak_profile.profile_name == "bob"
        )


if __name__ == "__main__":
    logging.basicConfig()
    run()

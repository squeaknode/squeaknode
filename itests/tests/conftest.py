import os
import uuid

import grpc
import pytest
from squeak.params import SelectParams

from proto import squeak_admin_pb2
from proto import squeak_admin_pb2_grpc
from tests.util import bytes_to_base64_string
from tests.util import generate_signing_key
from tests.util import get_address
from tests.util import load_lightning_client


@pytest.fixture(autouse=True)
def select_mainnet_params():
    # Set the network to simnet
    SelectParams("simnet")


@pytest.fixture
def admin_stub():
    with grpc.insecure_channel("squeaknode:8994") as admin_channel:
        yield squeak_admin_pb2_grpc.SqueakAdminStub(admin_channel)


@pytest.fixture
def other_admin_stub():
    with grpc.insecure_channel("squeaknode_other:8994") as admin_channel:
        yield squeak_admin_pb2_grpc.SqueakAdminStub(admin_channel)


@pytest.fixture
def lightning_client():
    return load_lightning_client()


@pytest.fixture
def following_signing_key(admin_stub):
    # Create a signing key
    signing_key = generate_signing_key()
    # Create a new contact profile
    profile_name = "following_contact_{}".format(uuid.uuid1())
    profile_address = get_address(signing_key)
    create_contact_profile_response = admin_stub.CreateContactProfile(
        squeak_admin_pb2.CreateContactProfileRequest(
            profile_name=profile_name,
            address=profile_address,
        )
    )
    contact_profile_id = create_contact_profile_response.profile_id
    # Set the profile to be following
    admin_stub.SetSqueakProfileFollowing(
        squeak_admin_pb2.SetSqueakProfileFollowingRequest(
            profile_id=contact_profile_id,
            following=True,
        )
    )
    # Yield the signing key
    yield signing_key
    # Delete the profile
    admin_stub.DeleteSqueakProfile(
        squeak_admin_pb2.DeleteSqueakProfileRequest(
            profile_id=contact_profile_id,
        )
    )


@pytest.fixture
def nonfollowing_signing_key(admin_stub):
    # Create a signing key
    signing_key = generate_signing_key()

    # Yield the signing key
    yield signing_key


@pytest.fixture
def signing_profile_id(admin_stub):
    # Create a new signing profile
    profile_name = "fake_signing_profile_{}".format(uuid.uuid1())
    create_signing_profile_response = admin_stub.CreateSigningProfile(
        squeak_admin_pb2.CreateSigningProfileRequest(
            profile_name=profile_name,
        )
    )
    profile_id = create_signing_profile_response.profile_id
    yield profile_id
    # Delete the profile
    admin_stub.DeleteSqueakProfile(
        squeak_admin_pb2.DeleteSqueakProfileRequest(
            profile_id=profile_id,
        )
    )


@pytest.fixture
def contact_profile_id(admin_stub):
    # Create a new contact profile
    contact_name = "fake_contact_profile_{}".format(uuid.uuid1())
    contact_signing_key = generate_signing_key()
    contact_address = get_address(contact_signing_key)
    create_contact_profile_response = admin_stub.CreateContactProfile(
        squeak_admin_pb2.CreateContactProfileRequest(
            profile_name=contact_name,
            address=contact_address,
        )
    )
    contact_profile_id = create_contact_profile_response.profile_id
    yield contact_profile_id
    # Delete the profile
    admin_stub.DeleteSqueakProfile(
        squeak_admin_pb2.DeleteSqueakProfileRequest(
            profile_id=contact_profile_id,
        )
    )


@pytest.fixture
def saved_squeak_hash(admin_stub, signing_profile_id):
    # Create a new squeak using the new profile
    make_squeak_content = "Hello from the profile on the server!"
    make_squeak_response = admin_stub.MakeSqueak(
        squeak_admin_pb2.MakeSqueakRequest(
            profile_id=signing_profile_id,
            content=make_squeak_content,
        )
    )
    squeak_hash = make_squeak_response.squeak_hash
    yield squeak_hash
    # Delete the squeak
    admin_stub.DeleteSqueak(
        squeak_admin_pb2.DeleteSqueakRequest(
            squeak_hash=squeak_hash,
        )
    )


@pytest.fixture
def peer_id(admin_stub):
    # Create a new peer
    random_peer_name = "random_peer_name_{}".format(uuid.uuid1())
    create_peer_response = admin_stub.CreatePeer(
        squeak_admin_pb2.CreatePeerRequest(
            peer_name=random_peer_name,
            host=random_peer_name,
            port=1234,
        )
    )
    peer_id = create_peer_response.peer_id
    yield peer_id
    # Delete the peer
    admin_stub.DeletePeer(
        squeak_admin_pb2.DeletePeerRequest(
            peer_id=peer_id,
        )
    )


@pytest.fixture
def random_name():
    yield "random_name_{}".format(uuid.uuid1())


@pytest.fixture
def random_image():
    yield os.urandom(567)


@pytest.fixture
def random_image_base64_string(random_image):
    yield bytes_to_base64_string(random_image)


@pytest.fixture
def connected_peer_id(other_admin_stub):
    # Add the main node as a peer
    create_peer_response = other_admin_stub.CreatePeer(
        squeak_admin_pb2.CreatePeerRequest(
            peer_name="test_peer",
            host="squeaknode",
            port=8774,
        )
    )
    peer_id = create_peer_response.peer_id
    # Set the peer to be downloading
    other_admin_stub.SetPeerDownloading(
        squeak_admin_pb2.SetPeerDownloadingRequest(
            peer_id=peer_id,
            downloading=True,
        )
    )
    yield peer_id
    # Delete the peer
    other_admin_stub.DeletePeer(
        squeak_admin_pb2.DeletePeerRequest(
            peer_id=peer_id,
        )
    )


@pytest.fixture
def connected_tcp_peer_id(other_admin_stub):
    # Add the main node as a peer
    create_peer_response = other_admin_stub.CreatePeer(
        squeak_admin_pb2.CreatePeerRequest(
            peer_name="test_peer",
            host="squeaknode",
            port=18777,
        )
    )
    peer_id = create_peer_response.peer_id
    # Set the peer to be downloading
    other_admin_stub.SetPeerDownloading(
        squeak_admin_pb2.SetPeerDownloadingRequest(
            peer_id=peer_id,
            downloading=True,
        )
    )

    # Connect the peer
    other_admin_stub.ConnectPeer(
        squeak_admin_pb2.ConnectPeerRequest(
            peer_id=peer_id,
        )
    )

    yield peer_id
    # Delete the peer
    other_admin_stub.DeletePeer(
        squeak_admin_pb2.DeletePeerRequest(
            peer_id=peer_id,
        )
    )

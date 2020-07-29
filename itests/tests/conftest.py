import pytest

import grpc

from squeak.params import SelectParams

from proto import lnd_pb2 as ln
from proto import lnd_pb2_grpc as lnrpc
from proto import (
    squeak_admin_pb2,
    squeak_admin_pb2_grpc,
    squeak_server_pb2,
    squeak_server_pb2_grpc,
)

from tests.util import generate_signing_key
from tests.util import get_address
from tests.util import load_lightning_client


@pytest.fixture(autouse=True)
def select_mainnet_params():
    # Set the network to mainnet.
    SelectParams("mainnet")

@pytest.fixture
def server_stub():
    with grpc.insecure_channel(
        "sqkserver:8774"
    ) as server_channel:
        yield squeak_server_pb2_grpc.SqueakServerStub(server_channel)

@pytest.fixture
def admin_stub():
    with grpc.insecure_channel(
            "sqkserver:8994"
    ) as admin_channel:
        yield squeak_admin_pb2_grpc.SqueakAdminStub(admin_channel)

@pytest.fixture
def lightning_client():
    return load_lightning_client()

@pytest.fixture
def whitelisted_signing_key(server_stub, admin_stub):
    # Create a signing key
    signing_key = generate_signing_key()

    # Create a new contact profile
    profile_name = "whitelisted_contact"
    profile_address = get_address(signing_key)
    create_contact_profile_response = admin_stub.CreateContactProfile(
        squeak_admin_pb2.CreateContactProfileRequest(
            profile_name=profile_name,
            address=profile_address,
        )
    )
    contact_profile_id = create_contact_profile_response.profile_id

    # Set the profile to be whitelisted
    admin_stub.SetSqueakProfileWhitelisted(
        squeak_admin_pb2.SetSqueakProfileWhitelistedRequest(
            profile_id=contact_profile_id,
            whitelisted=True,
        )
    )

    # Yield the signing key
    yield signing_key

@pytest.fixture
def nonwhitelisted_signing_key(server_stub, admin_stub):
    # Create a signing key
    signing_key = generate_signing_key()

    # Yield the signing key
    yield signing_key

import mock
import pytest

from squeaknode.bitcoin.blockchain_client import BlockchainClient
from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.squeak_controller import SqueakController
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.squeak_store import SqueakStore
from squeaknode.node.squeak_whitelist import SqueakWhitelist


@pytest.fixture
def config():
    squeaknode_config = SqueaknodeConfig()
    squeaknode_config.read()
    return squeaknode_config


@pytest.fixture
def regtest_config():
    squeaknode_config = SqueaknodeConfig(
        dict_config={'core': {'network': 'regtest'}}
    )
    squeaknode_config.read()
    return squeaknode_config


@pytest.fixture
def squeak_db():
    # return SqueakDb(None, None, None)
    return mock.Mock(spec=SqueakDb)


@pytest.fixture
def blockchain_client():
    return mock.Mock(spec=BlockchainClient)


@pytest.fixture
def lightning_client():
    return mock.Mock()


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def max_squeaks_per_address_per_hour():
    return 5000


@pytest.fixture
def squeak_whitelist():
    return mock.Mock(spec=SqueakWhitelist)


@pytest.fixture
def squeak_store():
    return mock.Mock(spec=SqueakStore)


@pytest.fixture
def squeak_controller(
    squeak_db,
    blockchain_client,
    lightning_client,
    squeak_store,
    squeak_whitelist,
    config,
):
    return SqueakController(
        squeak_db,
        blockchain_client,
        lightning_client,
        squeak_store,
        squeak_whitelist,
        config,
    )


@pytest.fixture
def regtest_squeak_controller(
    squeak_db,
    blockchain_client,
    lightning_client,
    squeak_store,
    squeak_whitelist,
    regtest_config,
):
    return SqueakController(
        squeak_db,
        blockchain_client,
        lightning_client,
        squeak_store,
        squeak_whitelist,
        regtest_config,
    )


def test_nothing():
    assert True


def test_get_buy_offer(squeak_controller):
    assert squeak_controller.get_buy_offer is not None


def test_get_network_default(squeak_controller):
    assert squeak_controller.get_network() == "testnet"


def test_get_network_regtest(regtest_squeak_controller):
    assert regtest_squeak_controller.get_network() == "regtest"


# def test_get_network_regtest(config, squeak_controller):
#     # with mock.patch.object(Config, 'squeaknode_network', new_callable=mock.PropertyMock) as mock_config:
#     # mock_config.return_value = 'regtest'
#     config.squeaknode_network = "regtest"
#     print(config.squeaknode_network)

#     assert squeak_controller.get_network() == "regtest"


def test_create_peer(squeak_db, squeak_controller):
    squeak_controller.create_peer(
        "fake_name",
        "fake_host",
        5678,
    )

    squeak_db.insert_peer.assert_called_with(
        SqueakPeer(
            peer_id=None,
            peer_name="fake_name",
            host="fake_host",
            port=5678,
            uploading=False,
            downloading=False,
        )
    )

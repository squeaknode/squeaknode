import mock
import pytest

from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.network.connection_manager import ConnectionManager
from squeaknode.network.peer_client import PeerClient
from squeaknode.network.peer_server import PeerServer
from squeaknode.node.payment_processor import PaymentProcessor
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.node.squeak_rate_limiter import SqueakRateLimiter


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
def peer_server():
    return mock.Mock(spec=PeerServer)


@pytest.fixture
def peer_client():
    return mock.Mock(spec=PeerClient)


@pytest.fixture
def connection_manager():
    return mock.Mock(spec=ConnectionManager)


@pytest.fixture
def squeak_core():
    return mock.Mock(spec=SqueakCore)


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def squeak_rate_limiter():
    return mock.Mock(spec=SqueakRateLimiter)


@pytest.fixture
def payment_processor():
    return mock.Mock(spec=PaymentProcessor)


@pytest.fixture
def squeak_controller(
    squeak_db,
    squeak_core,
    squeak_rate_limiter,
    payment_processor,
    peer_server,
    peer_client,
    connection_manager,
    config,
):
    return SqueakController(
        squeak_db,
        squeak_core,
        squeak_rate_limiter,
        payment_processor,
        peer_server,
        peer_client,
        connection_manager,
        config,
    )


@pytest.fixture
def regtest_squeak_controller(
    squeak_db,
    squeak_core,
    squeak_rate_limiter,
    payment_processor,
    peer_server,
    peer_client,
    connection_manager,
    regtest_config,
):
    return SqueakController(
        squeak_db,
        squeak_core,
        squeak_rate_limiter,
        payment_processor,
        peer_server,
        peer_client,
        connection_manager,
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
        "fake_peer_name",
        "fake_host",
        5678,
    )

    squeak_db.insert_peer.assert_called_with(
        SqueakPeer(
            peer_id=None,
            peer_name="fake_peer_name",
            address=PeerAddress(
                host="fake_host",
                port=5678,
            ),
            uploading=False,
            downloading=False,
        )
    )


def test_create_peer_default_port(config, squeak_db, squeak_controller):
    squeak_controller.create_peer(
        "fake_peer_name",
        "fake_host",
        0,
    )

    squeak_db.insert_peer.assert_called_with(
        SqueakPeer(
            peer_id=None,
            peer_name="fake_peer_name",
            address=PeerAddress(
                host="fake_host",
                port=config.core.default_peer_rpc_port,
            ),
            uploading=False,
            downloading=False,
        )
    )

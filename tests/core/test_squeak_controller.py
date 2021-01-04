import mock
import pytest

from squeaknode.bitcoin.blockchain_client import BlockchainClient
from squeaknode.config.config import Config
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.squeak_controller import SqueakController
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.squeak_store import SqueakStore
from squeaknode.node.squeak_whitelist import SqueakWhitelist


@pytest.fixture
def config():
    return Config(None)


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


def test_nothing():
    assert True


def test_get_buy_offer(squeak_controller):
    assert squeak_controller.get_buy_offer is not None


def test_get_network(squeak_controller):
    assert squeak_controller.get_network() == "testnet"

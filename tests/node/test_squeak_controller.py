# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import threading

import mock
import pytest

from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.peer_address import Network
from squeaknode.core.peer_address import PeerAddress
from squeaknode.network.network_manager import NetworkManager
from squeaknode.node.active_download_manager import ActiveDownloadManager
from squeaknode.node.node_settings import NodeSettings
from squeaknode.node.payment_processor import PaymentProcessor
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.node.squeak_store import SqueakStore
from squeaknode.twitter.twitter_forwarder import TwitterForwarder


@pytest.fixture
def config():
    squeaknode_config = SqueaknodeConfig()
    squeaknode_config.read()
    return squeaknode_config


@pytest.fixture
def regtest_config():
    squeaknode_config = SqueaknodeConfig(
        dict_config={'node': {'network': 'regtest'}}
    )
    squeaknode_config.read()
    return squeaknode_config


# @pytest.fixture
# def squeak_db():
#     # return SqueakDb(None, None, None)
#     return mock.Mock(spec=SqueakDb)


@pytest.fixture
def network_manager():
    return mock.Mock(spec=NetworkManager)


# @pytest.fixture
# def squeak_core():
#     return mock.Mock(spec=SqueakCore)


@pytest.fixture
def squeak_store():
    return mock.Mock(spec=SqueakStore)


@pytest.fixture
def node_settings():
    return mock.Mock(spec=NodeSettings)


@pytest.fixture
def lightning_host_port():
    return LightningAddressHostPort(host="my_lightning_host", port=8765)


@pytest.fixture
def peer_address():
    return PeerAddress(
        network=Network.IPV4,
        host="fake_host",
        port=5678,
    )


@pytest.fixture
def peer_address_with_zero():
    return PeerAddress(
        network=Network.IPV4,
        host="fake_host",
        port=0,
    )


@pytest.fixture
def price_msat():
    return 777


@pytest.fixture
def payment_processor():
    return mock.Mock(spec=PaymentProcessor)


@pytest.fixture
def download_manager():
    return mock.Mock(spec=ActiveDownloadManager)


@pytest.fixture
def twitter_forwarder():
    return mock.Mock(spec=TwitterForwarder)


@pytest.fixture
def squeak_controller(
    squeak_store,
    node_settings,
    payment_processor,
    network_manager,
    download_manager,
    twitter_forwarder,
    config,
):
    return SqueakController(
        squeak_store,
        node_settings,
        payment_processor,
        network_manager,
        download_manager,
        twitter_forwarder,
        config,
    )


@pytest.fixture
def regtest_squeak_controller(
    squeak_store,
    node_settings,
    payment_processor,
    network_manager,
    download_manager,
    twitter_forwarder,
    regtest_config,
):
    return SqueakController(
        squeak_store,
        node_settings,
        payment_processor,
        network_manager,
        download_manager,
        twitter_forwarder,
        regtest_config,
    )


def test_get_network_default(squeak_controller):
    assert squeak_controller.get_network() == "testnet"


def test_get_network_regtest(regtest_squeak_controller):
    assert regtest_squeak_controller.get_network() == "regtest"


def test_save_squeak(squeak_controller, squeak_store, squeak):
    squeak_controller.save_squeak(squeak)

    squeak_store.save_squeak.assert_called_with(squeak)


def test_unlock_squeak(squeak_controller, squeak_store, squeak, secret_key):
    squeak_controller.unlock_squeak(squeak, secret_key)

    squeak_store.unlock_squeak.assert_called_with(squeak, secret_key)


def test_make_squeak(squeak_controller, squeak_store):
    squeak_controller.make_squeak(123, "hello!", None)

    squeak_store.make_squeak.assert_called_with(123, "hello!", None)


def test_get_squeak(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.get_squeak(squeak_hash)

    squeak_store.get_squeak.assert_called_with(squeak_hash)


def test_get_squeak_secret_key(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.get_squeak_secret_key(squeak_hash)

    squeak_store.get_squeak_secret_key.assert_called_with(squeak_hash)


def test_delete_squeak(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.delete_squeak(squeak_hash)

    squeak_store.delete_squeak.assert_called_with(squeak_hash)


def test_create_signing_profile(squeak_controller, squeak_store):
    squeak_controller.create_signing_profile("bob")

    squeak_store.create_signing_profile.assert_called_with("bob")


def test_import_signing_profile(squeak_controller, squeak_store, private_key):
    squeak_controller.import_signing_profile("bob", private_key)

    squeak_store.import_signing_profile.assert_called_with("bob", private_key)


def test_create_contact_profile(squeak_controller, squeak_store, public_key):
    squeak_controller.create_contact_profile("bob", public_key)

    squeak_store.create_contact_profile.assert_called_with("bob", public_key)


def test_get_profiles(squeak_controller, squeak_store):
    squeak_controller.get_profiles()

    squeak_store.get_profiles.assert_called_with()


def test_get_signing_profiles(squeak_controller, squeak_store):
    squeak_controller.get_signing_profiles()

    squeak_store.get_signing_profiles.assert_called_with()


def test_get_contact_profiles(squeak_controller, squeak_store):
    squeak_controller.get_contact_profiles()

    squeak_store.get_contact_profiles.assert_called_with()


def test_get_profile(squeak_controller, squeak_store):
    squeak_controller.get_squeak_profile(123)

    squeak_store.get_squeak_profile.assert_called_with(123)


def test_get_profile_by_public_key(squeak_controller, squeak_store, public_key):
    squeak_controller.get_squeak_profile_by_public_key(public_key)

    squeak_store.get_squeak_profile_by_public_key.assert_called_with(
        public_key)


def test_get_profile_by_name(squeak_controller, squeak_store):
    squeak_controller.get_squeak_profile_by_name("bob")

    squeak_store.get_squeak_profile_by_name.assert_called_with("bob")


def test_set_squeak_profile_following(squeak_controller, squeak_store):
    squeak_controller.set_squeak_profile_following(123, True)

    squeak_store.set_squeak_profile_following.assert_called_with(123, True)


def test_rename_squeak_profile(squeak_controller, squeak_store):
    squeak_controller.rename_squeak_profile(123, "carol")

    squeak_store.rename_squeak_profile.assert_called_with(123, "carol")


def test_delete_squeak_profile(squeak_controller, squeak_store):
    squeak_controller.delete_squeak_profile(123)

    squeak_store.delete_squeak_profile.assert_called_with(123)


def test_set_squeak_profile_image(squeak_controller, squeak_store):
    squeak_controller.set_squeak_profile_image(123, b"profile_image_bytes")

    squeak_store.set_squeak_profile_image.assert_called_with(
        123, b"profile_image_bytes")


def test_create_peer(squeak_controller, squeak_store, peer_address):
    squeak_controller.create_peer(
        "fake_peer_name",
        peer_address,
    )

    squeak_store.create_peer.assert_called_with(
        "fake_peer_name",
        peer_address,
    )


def test_get_peer(squeak_controller, squeak_store):
    squeak_controller.get_peer(123)

    squeak_store.get_peer.assert_called_with(123)


def test_get_peer_by_address(squeak_controller, squeak_store, peer_address):
    squeak_controller.get_peer_by_address(peer_address)

    squeak_store.get_peer_by_address.assert_called_with(peer_address)


def test_get_autoconnect_peers(squeak_controller, squeak_store):
    squeak_controller.get_autoconnect_peers()

    squeak_store.get_autoconnect_peers.assert_called_with()


def test_set_peer_autoconnect(squeak_controller, squeak_store):
    squeak_controller.set_peer_autoconnect(123, True)

    squeak_store.set_peer_autoconnect.assert_called_with(123, True)


def test_set_peer_share_for_free(squeak_controller, squeak_store):
    squeak_controller.set_peer_share_for_free(123, True)

    squeak_store.set_peer_share_for_free.assert_called_with(123, True)


def test_rename_peer(squeak_controller, squeak_store):
    squeak_controller.rename_peer(123, "carol")

    squeak_store.rename_peer.assert_called_with(123, "carol")


def test_get_received_offers(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.get_received_offers(squeak_hash)

    squeak_store.get_received_offers.assert_called_with(squeak_hash)


def test_get_received_offer(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.get_received_offer(123)

    squeak_store.get_received_offer.assert_called_with(123)


def test_pay_offer(squeak_controller, squeak_store):
    squeak_controller.pay_offer(123)

    squeak_store.pay_offer.assert_called_with(123)


def test_get_sent_payments(squeak_controller, squeak_store, sent_payment):
    squeak_controller.get_sent_payments(5, sent_payment)

    squeak_store.get_sent_payments.assert_called_with(5, sent_payment)


def test_get_sent_payment(squeak_controller, squeak_store):
    squeak_controller.get_sent_payment(123)

    squeak_store.get_sent_payment.assert_called_with(123)


def test_get_received_payments(squeak_controller, squeak_store, received_payment):
    squeak_controller.get_received_payments(5, received_payment)

    squeak_store.get_received_payments.assert_called_with(5, received_payment)


def test_subscribe_received_payments(squeak_controller, squeak_store, received_payment):
    event = threading.Event()
    squeak_controller.subscribe_received_payments(456, event)

    squeak_store.subscribe_received_payments.assert_called_with(456, event)


def test_get_squeak_entry(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.get_squeak_entry(squeak_hash)

    squeak_store.get_squeak_entry.assert_called_with(squeak_hash)


def test_get_timeline_squeak_entries(squeak_controller, squeak_store, squeak_entry_locked):
    squeak_controller.get_timeline_squeak_entries(5, squeak_entry_locked)

    squeak_store.get_timeline_squeak_entries.assert_called_with(
        5, squeak_entry_locked)


def test_get_liked_squeak_entries(squeak_controller, squeak_store, squeak_entry_locked):
    squeak_controller.get_liked_squeak_entries(5, squeak_entry_locked)

    squeak_store.get_liked_squeak_entries.assert_called_with(
        5,
        squeak_entry_locked,
    )


def test_get_squeak_entries_for_public_key(squeak_controller, squeak_store, public_key, squeak_entry_locked):
    squeak_controller.get_squeak_entries_for_public_key(
        public_key, 5, squeak_entry_locked)

    squeak_store.get_squeak_entries_for_public_key.assert_called_with(
        public_key,
        5,
        squeak_entry_locked,
    )


def test_get_squeak_entries_for_text_search(squeak_controller, squeak_store, squeak_entry_locked):
    squeak_controller.get_squeak_entries_for_text_search(
        "search_text", 5, squeak_entry_locked)

    squeak_store.get_squeak_entries_for_text_search.assert_called_with(
        "search_text",
        5,
        squeak_entry_locked,
    )


def test_get_ancestor_squeak_entries(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.get_ancestor_squeak_entries(squeak_hash)

    squeak_store.get_ancestor_squeak_entries.assert_called_with(squeak_hash)


def test_get_reply_squeak_entries(squeak_controller, squeak_store, squeak_hash, squeak_entry_locked):
    squeak_controller.get_reply_squeak_entries(
        squeak_hash, 5, squeak_entry_locked)

    squeak_store.get_reply_squeak_entries.assert_called_with(
        squeak_hash,
        5,
        squeak_entry_locked,
    )


def test_get_number_of_squeaks(squeak_controller, squeak_store):
    squeak_controller.get_number_of_squeaks()

    squeak_store.get_number_of_squeaks.assert_called_with()


def test_get_received_payment_summary(squeak_controller, squeak_store):
    squeak_controller.get_received_payment_summary()

    squeak_store.get_received_payment_summary.assert_called_with()


def test_get_sent_payment_summary(squeak_controller, squeak_store):
    squeak_controller.get_sent_payment_summary()

    squeak_store.get_sent_payment_summary.assert_called_with()


def test_reprocess_received_payments(squeak_controller, squeak_store, payment_processor):
    squeak_controller.reprocess_received_payments()

    squeak_store.clear_received_payment_settle_indices.assert_called_with()
    payment_processor.start_processing.assert_called_with()


def test_like_squeak(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.like_squeak(squeak_hash)

    squeak_store.like_squeak.assert_called_with(squeak_hash)


def test_unlike_squeak(squeak_controller, squeak_store, squeak_hash):
    squeak_controller.unlike_squeak(squeak_hash)

    squeak_store.unlike_squeak.assert_called_with(squeak_hash)


def test_get_connected_peer(squeak_controller, squeak_store, network_manager, peer_address):
    squeak_controller.get_connected_peer(peer_address)

    network_manager.get_connected_peer.assert_called_with(peer_address)
    squeak_store.get_peer_by_address.assert_called_with(peer_address)


def test_get_connected_peers(squeak_controller, squeak_store, network_manager, peer_address, peer):
    from collections import namedtuple
    Peer = namedtuple('Peer', ['name', 'remote_address'])
    fake_peer = Peer("peer1", peer_address)
    network_manager.get_connected_peers.return_value = [fake_peer] * 5
    squeak_controller.get_connected_peers()

    network_manager.get_connected_peers.assert_called_with()
    squeak_store.get_peer_by_address.assert_called_with(peer_address)

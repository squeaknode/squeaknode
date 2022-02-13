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
import logging

import squeak.params
from squeak.params import SelectParams

from squeaknode.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeaknode.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeaknode.admin.webapp.app import SqueakAdminWebServer
from squeaknode.bitcoin.bitcoin_block_subscription_client import BitcoinBlockSubscriptionClient
from squeaknode.bitcoin.bitcoin_core_client import BitcoinCoreClient
from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.db.db_engine import get_connection_string
from squeaknode.db.db_engine import get_engine
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient
from squeaknode.network.network_manager import NetworkManager
from squeaknode.node.active_download_manager import ActiveDownloadManager
from squeaknode.node.network_handler import NetworkHandler
from squeaknode.node.node_settings import NodeSettings
from squeaknode.node.payment_processor import PaymentProcessor
from squeaknode.node.peer_connection_worker import PeerConnectionWorker
from squeaknode.node.peer_subscription_update_worker import PeerSubscriptionUpdateWorker
from squeaknode.node.process_forward_tweets_worker import ProcessForwardTweetsWorker
from squeaknode.node.process_received_payments_worker import ProcessReceivedPaymentsWorker
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.node.squeak_deletion_worker import SqueakDeletionWorker
from squeaknode.node.squeak_offer_expiry_worker import SqueakOfferExpiryWorker
from squeaknode.node.squeak_store import SqueakStore
from squeaknode.node.update_follows_worker import UpdateFollowsWorker
from squeaknode.node.update_subscribed_secret_key_worker import UpdateSubscribedSecretKeysWorker
from squeaknode.node.update_subscribed_squeak_worker import UpdateSubscribedSqueaksWorker
from squeaknode.twitter.twitter_forwarder import TwitterForwarder

logger = logging.getLogger(__name__)


class SqueakNode:

    def __init__(self, config: SqueaknodeConfig):
        self.config = config
        self.set_network_params()
        self.create_db()
        self.create_node_settings()
        self.create_lightning_client()
        self.create_bitcoin_client()
        self.create_bitcoin_block_subscription_client()
        self.create_squeak_core()
        self.create_squeak_store()
        self.create_payment_processor()
        self.create_twitter_forwarder()
        self.create_network_manager()
        self.create_download_manager()
        self.create_squeak_controller()
        self.create_network_handler()
        self.create_admin_handler()
        self.create_admin_rpc_server()
        self.create_admin_web_server()
        self.create_received_payment_processor_worker()
        self.create_forward_tweets_processor_worker()
        self.create_peer_connection_worker()
        self.create_squeak_deletion_worker()
        self.create_offer_expiry_worker()
        self.create_new_squeak_worker()
        self.create_new_secret_key_worker()
        self.create_new_follow_worker()
        self.create_peer_subscription_update_worker()

    def start_running(self):
        self.squeak_db.init_with_retries()
        self.lightning_client.init()

        self.network_manager.start(self.network_handler)
        if self.config.rpc.enabled:
            self.admin_rpc_server.start()
        if self.config.webadmin.enabled:
            self.admin_web_server.start()
        self.received_payment_processor_worker.start_running()
        self.forward_tweets_processor_worker.start_running()
        self.peer_connection_worker.start()
        self.squeak_deletion_worker.start()
        self.offer_expiry_worker.start()
        self.new_squeak_worker.start_running()
        self.new_secret_key_worker.start_running()
        self.new_follow_worker.start_running()
        self.new_bitcoin_block_worker.start_running()
        self.download_manager.start()

    def stop_running(self):
        self.download_manager.stop()
        self.admin_web_server.stop()
        self.admin_rpc_server.stop()
        self.network_manager.stop()
        self.received_payment_processor_worker.stop_running()
        self.forward_tweets_processor_worker.stop_running()
        self.new_squeak_worker.stop_running()

    def set_network_params(self):
        SelectParams(self.config.node.network)

    def create_db(self):
        connection_string = get_connection_string(
            self.config,
            self.config.node.network,
        )
        logger.info("Using connection string: {}".format(
            connection_string))
        engine = get_engine(connection_string)
        self.squeak_db = SqueakDb(engine)

    def create_node_settings(self):
        self.node_settings = NodeSettings(self.squeak_db)

    def create_lightning_client(self):
        self.lightning_client = LNDLightningClient(
            self.config.lnd.host,
            self.config.lnd.rpc_port,
            self.config.lnd.tls_cert_path,
            self.config.lnd.macaroon_path,
        )

    def create_bitcoin_client(self):
        self.bitcoin_client = BitcoinCoreClient(
            self.config.bitcoin.rpc_host,
            self.config.bitcoin.rpc_port,
            self.config.bitcoin.rpc_user,
            self.config.bitcoin.rpc_pass,
            self.config.bitcoin.rpc_use_ssl,
            self.config.bitcoin.rpc_ssl_cert,
        )

    def create_bitcoin_block_subscription_client(self):
        self.bitcoin_block_subscription_client = BitcoinBlockSubscriptionClient(
            self.config.bitcoin.rpc_host,
            self.config.bitcoin.zeromq_hashblock_port,
        )

    def create_squeak_core(self):
        self.squeak_core = SqueakCore(
            self.bitcoin_client,
            self.lightning_client,
        )

    def create_squeak_store(self):
        self.squeak_store = SqueakStore(
            self.squeak_db,
            self.squeak_core,
            self.config.node.max_squeaks,
            self.config.node.max_squeaks_per_public_key_per_block,
            self.config.node.squeak_retention_s,
            self.config.node.received_offer_retention_s,
            self.config.node.sent_offer_retention_s,
        )

    def create_payment_processor(self):
        self.payment_processor = PaymentProcessor(
            self.squeak_db,
            self.squeak_core,
            self.config.node.subscribe_invoices_retry_s,
        )

    def create_twitter_forwarder(self):
        self.twitter_forwarder = TwitterForwarder(
            self.squeak_store,
            self.squeak_core,
            self.config.twitter.forward_tweets_retry_s,
        )

    def create_network_manager(self):
        self.network_manager = NetworkManager(
            self.config,
            squeak.params.params.DEFAULT_PORT,
        )

    def create_squeak_controller(self):
        self.squeak_controller = SqueakController(
            self.squeak_store,
            self.squeak_core,
            self.payment_processor,
            self.network_manager,
            self.download_manager,
            self.twitter_forwarder,
            self.node_settings,
            self.config,
            squeak.params.params.DEFAULT_PORT,
        )

    def create_network_handler(self):
        self.network_handler = NetworkHandler(
            self.squeak_store,
            self.squeak_core,
            self.network_manager,
            self.download_manager,
            self.node_settings,
            self.config,
        )

    def create_admin_handler(self):
        self.admin_handler = SqueakAdminServerHandler(
            self.lightning_client,
            self.squeak_controller,
        )

    def create_admin_rpc_server(self):
        self.admin_rpc_server = SqueakAdminServerServicer(
            self.config.rpc.host,
            self.config.rpc.port,
            self.admin_handler,
        )

    def create_admin_web_server(self):
        self.admin_web_server = SqueakAdminWebServer(
            self.config.webadmin.host,
            self.config.webadmin.port,
            self.config.webadmin.username,
            self.config.webadmin.password,
            self.config.webadmin.use_ssl,
            self.config.webadmin.login_disabled,
            self.config.webadmin.allow_cors,
            self.admin_handler,
        )

    def create_received_payment_processor_worker(self):
        self.received_payment_processor_worker = ProcessReceivedPaymentsWorker(
            self.payment_processor,
        )

    def create_forward_tweets_processor_worker(self):
        self.forward_tweets_processor_worker = ProcessForwardTweetsWorker(
            self.twitter_forwarder,
        )

    def create_peer_connection_worker(self):
        self.peer_connection_worker = PeerConnectionWorker(
            self.squeak_store,
            self.network_manager,
            self.config.node.peer_autoconnect_interval_s,
        )

    def create_squeak_deletion_worker(self):
        self.squeak_deletion_worker = SqueakDeletionWorker(
            self.squeak_store,
            self.config.node.squeak_deletion_interval_s,
        )

    def create_offer_expiry_worker(self):
        self.offer_expiry_worker = SqueakOfferExpiryWorker(
            self.squeak_store,
            self.config.node.offer_deletion_interval_s,
        )

    def create_new_squeak_worker(self):
        self.new_squeak_worker = UpdateSubscribedSqueaksWorker(
            self.squeak_store,
            self.network_manager,
        )

    def create_new_secret_key_worker(self):
        self.new_secret_key_worker = UpdateSubscribedSecretKeysWorker(
            self.squeak_store,
            self.network_manager,
        )

    def create_new_follow_worker(self):
        self.new_follow_worker = UpdateFollowsWorker(
            self.squeak_store,
            self.network_manager,
            self.network_handler,
        )

    def create_peer_subscription_update_worker(self):
        self.new_bitcoin_block_worker = PeerSubscriptionUpdateWorker(
            self.network_manager,
            self.network_handler,
            self.bitcoin_block_subscription_client,
        )

    def create_download_manager(self):
        self.download_manager = ActiveDownloadManager(
            self.network_manager,
        )

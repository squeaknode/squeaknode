import logging

from squeak.params import SelectParams

from squeaknode.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeaknode.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeaknode.admin.webapp.app import SqueakAdminWebServer
from squeaknode.bitcoin.bitcoin_core_bitcoin_client import BitcoinCoreBitcoinClient
from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.db.db_engine import get_connection_string
from squeaknode.db.db_engine import get_engine
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient
from squeaknode.network.network_manager import NetworkManager
from squeaknode.node.new_squeak_worker import NewSqueakWorker
from squeaknode.node.payment_processor import PaymentProcessor
from squeaknode.node.peer_connection_worker import PeerConnectionWorker
from squeaknode.node.process_received_payments_worker import ProcessReceivedPaymentsWorker
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.node.squeak_deletion_worker import SqueakDeletionWorker
from squeaknode.node.squeak_offer_expiry_worker import SqueakOfferExpiryWorker
from squeaknode.node.squeak_rate_limiter import SqueakRateLimiter


logger = logging.getLogger(__name__)


class SqueakNode:

    def __init__(self, config: SqueaknodeConfig):
        self.config = config

    def _initialize(self):
        # Print some configs
        logger.info("Config server rpc port: {}".format(
            self.config.server.rpc_port))

        self.initialize_network()
        self.initialize_db()
        self.initialize_lightning_client()
        self.initialize_bitcoin_client()
        self.initialize_squeak_core()
        self.initialize_rate_limiter()
        self.initialize_payment_processor()
        self.initialize_network_manager()
        self.initialize_squeak_controller()
        self.initialize_admin_handler()
        self.initialize_admin_rpc_server()
        self.initialize_admin_web_server()
        self.initialize_received_payment_processor_worker()
        self.initialize_peer_connection_worker()
        self.initialize_squeak_deletion_worker()
        self.initialize_offer_expiry_worker()
        self.initialize_new_squeak_worker()

    def start_running(self):
        self._initialize()

        self.network_manager.start(self.squeak_controller)
        if self.config.admin.rpc_enabled:
            self.admin_rpc_server.start()
        if self.config.webadmin.enabled:
            self.admin_web_server.start()
        self.received_payment_processor_worker.start_running()
        self.peer_connection_worker.start()
        self.squeak_deletion_worker.start()
        self.offer_expiry_worker.start()
        self.new_squeak_worker.start_running()

    def stop_running(self):
        self.admin_web_server.stop()
        self.admin_rpc_server.stop()
        self.network_manager.stop()
        self.received_payment_processor_worker.stop_running()
        self.new_squeak_worker.stop_running()

    def initialize_network(self):
        # load the network
        self.network = self.config.core.network
        SelectParams(self.network)

    def initialize_db(self):
        connection_string = get_connection_string(
            self.config,
            self.network,
        )
        logger.info("Using connection string: {}".format(
            connection_string))
        engine = get_engine(connection_string)
        self.squeak_db = SqueakDb(engine)
        self.squeak_db.init()

    def initialize_lightning_client(self):
        # load the lightning client
        self.lightning_client = LNDLightningClient(
            self.config.lnd.host,
            self.config.lnd.rpc_port,
            self.config.lnd.tls_cert_path,
            self.config.lnd.macaroon_path,
        )

    def initialize_bitcoin_client(self):
        # load the bitcoin client
        self.bitcoin_client = BitcoinCoreBitcoinClient(
            self.config.bitcoin.rpc_host,
            self.config.bitcoin.rpc_port,
            self.config.bitcoin.rpc_user,
            self.config.bitcoin.rpc_pass,
            self.config.bitcoin.rpc_use_ssl,
            self.config.bitcoin.rpc_ssl_cert,
        )

    def initialize_squeak_core(self):
        self.squeak_core = SqueakCore(
            self.bitcoin_client,
            self.lightning_client,
        )

    def initialize_rate_limiter(self):
        self.squeak_rate_limiter = SqueakRateLimiter(
            self.squeak_db,
            self.config.core.max_squeaks_per_address_per_block,
        )

    def initialize_payment_processor(self):
        self.payment_processor = PaymentProcessor(
            self.squeak_db,
            self.squeak_core,
            self.config.core.subscribe_invoices_retry_s,
        )

    def initialize_network_manager(self):
        self.network_manager = NetworkManager(self.config)

    def initialize_squeak_controller(self):
        self.squeak_controller = SqueakController(
            self.squeak_db,
            self.squeak_core,
            self.squeak_rate_limiter,
            self.payment_processor,
            self.network_manager,
            self.config,
        )

    def initialize_admin_handler(self):
        self.admin_handler = SqueakAdminServerHandler(
            self.lightning_client,
            self.squeak_controller,
        )

    def initialize_admin_rpc_server(self):
        self.admin_rpc_server = SqueakAdminServerServicer(
            self.config.admin.rpc_host,
            self.config.admin.rpc_port,
            self.admin_handler,
        )

    def initialize_admin_web_server(self):
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

    def initialize_received_payment_processor_worker(self):
        self.received_payment_processor_worker = ProcessReceivedPaymentsWorker(
            self.payment_processor,
        )

    def initialize_peer_connection_worker(self):
        self.peer_connection_worker = PeerConnectionWorker(
            self.squeak_controller,
            10,
        )

    def initialize_squeak_deletion_worker(self):
        self.squeak_deletion_worker = SqueakDeletionWorker(
            self.squeak_controller,
            self.config.core.squeak_deletion_interval_s,
        )

    def initialize_offer_expiry_worker(self):
        self.offer_expiry_worker = SqueakOfferExpiryWorker(
            self.squeak_controller,
            self.config.core.offer_deletion_interval_s,
        )

    def initialize_new_squeak_worker(self):
        self.new_squeak_worker = NewSqueakWorker(
            self.squeak_controller,
            self.network_manager,
        )

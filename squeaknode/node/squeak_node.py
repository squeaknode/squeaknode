import logging
import threading

from squeak.params import SelectParams

from squeaknode.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeaknode.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeaknode.admin.webapp.app import SqueakAdminWebServer
from squeaknode.bitcoin.bitcoin_core_bitcoin_client import BitcoinCoreBitcoinClient
from squeaknode.config.config import SqueaknodeConfig
from squeaknode.core.squeak_core import SqueakCore
from squeaknode.db.db_engine import get_engine
from squeaknode.db.db_engine import get_sqlite_connection_string
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient
from squeaknode.network.network_manager import NetworkManager
from squeaknode.node.payment_processor import PaymentProcessor
from squeaknode.node.peer_connection_worker import PeerConnectionWorker
from squeaknode.node.process_received_payments_worker import ProcessReceivedPaymentsWorker
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.node.squeak_deletion_worker import SqueakDeletionWorker
from squeaknode.node.squeak_offer_expiry_worker import SqueakOfferExpiryWorker
from squeaknode.node.squeak_peer_sync_worker import SqueakPeerSyncWorker
from squeaknode.node.squeak_rate_limiter import SqueakRateLimiter


logger = logging.getLogger(__name__)


class SqueakNode:

    def __init__(self, config: SqueaknodeConfig):
        self.config = config
        self.stopped = threading.Event()
        self._initialize()

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

    def start_running(self):
        # start admin rpc server
        if self.config.admin.rpc_enabled:
            start_admin_rpc_server(self.admin_rpc_server)

        # start admin web server
        if self.config.webadmin.enabled:
            start_admin_web_server(self.admin_web_server)

        # Start peer socket server and peer client
        self.network_manager.start(self.squeak_controller)

        # Background workers
        self.start_peer_connection_worker()
        self.start_peer_sync_worker()
        self.start_squeak_deletion_worker()
        self.start_offer_expiry_worker()

        self.received_payment_processor_worker.start_running()

    def stop_running(self):
        self.stopped.set()

        # TODO: Use explicit stop to stop all components
        self.network_manager.stop()

    def start_peer_connection_worker(self):
        logger.info("Starting peer connection worker...")
        PeerConnectionWorker(
            self.squeak_controller,
            10,
        ).start()

    def start_peer_sync_worker(self):
        if self.config.sync.enabled:
            logger.info("Starting peer sync worker...")
            SqueakPeerSyncWorker(
                self.squeak_controller,
                10,
            ).start()

    def start_squeak_deletion_worker(self):
        logger.info("Starting squeak deletion worker...")
        SqueakDeletionWorker(
            self.squeak_controller,
            self.config.core.squeak_deletion_interval_s,
        ).start()

    def start_offer_expiry_worker(self):
        logger.info("Starting offer expiry worker...")
        SqueakOfferExpiryWorker(
            self.squeak_controller,
            self.config.core.offer_deletion_interval_s,
        ).start()

    def initialize_network(self):
        # load the network
        self.network = self.config.core.network
        SelectParams(self.network)

    def initialize_db(self):
        # load the db
        self.squeak_db = load_db(self.config, self.network)
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
            self.stopped,
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
            self.stopped,
        )

    def initialize_received_payment_processor_worker(self):
        self.received_payment_processor_worker = ProcessReceivedPaymentsWorker(
            self.payment_processor,
            self.stopped,
        )


def load_db(config, network):
    connection_string = config.db.connection_string
    logger.info("connection string: {}".format(connection_string))
    logger.info("connection string type: {}".format(type(connection_string)))
    if not connection_string:
        sqk_dir = config.core.sqk_dir_path
        logger.info(
            "Getting connection string from sqk dir: {}".format(sqk_dir))
        connection_string = get_sqlite_connection_string(sqk_dir, network)
    logger.info("Getting engine from connection string: {}".format(
        connection_string))
    engine = get_engine(connection_string)
    return SqueakDb(engine)


def start_admin_rpc_server(rpc_server):
    logger.info("Starting admin RPC server...")
    thread = threading.Thread(
        target=rpc_server.serve,
        args=(),
    )
    thread.start()


def start_admin_web_server(admin_web_server):
    logger.info("Starting admin web server...")
    thread = threading.Thread(
        target=admin_web_server.serve,
        args=(),
    )
    thread.start()

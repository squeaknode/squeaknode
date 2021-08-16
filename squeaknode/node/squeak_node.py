import logging
import threading
from pathlib import Path

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

        # load the network
        network = self.config.core.network
        SelectParams(network)

        # load the db
        squeak_db = load_db(self.config, network)
        squeak_db.init()

        # load the lightning client
        lightning_client = load_lightning_client(self.config)

        # load the bitcoin client
        bitcoin_client = load_bitcoin_client(self.config)

        squeak_core = SqueakCore(
            bitcoin_client,
            lightning_client,
        )
        squeak_rate_limiter = SqueakRateLimiter(
            squeak_db,
            self.config.core.max_squeaks_per_address_per_block,
        )
        payment_processor = PaymentProcessor(
            squeak_db,
            squeak_core,
            self.config.core.subscribe_invoices_retry_s,
        )

        self.network_manager = NetworkManager(self.config)

        squeak_controller = SqueakController(
            squeak_db,
            squeak_core,
            squeak_rate_limiter,
            payment_processor,
            self.network_manager,
            self.config,
        )
        self.squeak_controller = squeak_controller

        admin_handler = load_admin_handler(
            lightning_client, squeak_controller)

        self.admin_rpc_server = load_admin_rpc_server(
            self.config, admin_handler, self.stopped)

        self.admin_web_server = load_admin_web_server(
            self.config, admin_handler, self.stopped)

        self.sent_offers_worker = ProcessReceivedPaymentsWorker(
            payment_processor, self.stopped,
        )

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

        self.sent_offers_worker.start_running()

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


def load_lightning_client(config) -> LNDLightningClient:
    return LNDLightningClient(
        config.lnd.host,
        config.lnd.rpc_port,
        config.lnd.tls_cert_path,
        config.lnd.macaroon_path,
    )


def load_admin_rpc_server(config, handler, stopped_event) -> SqueakAdminServerServicer:
    return SqueakAdminServerServicer(
        config.admin.rpc_host,
        config.admin.rpc_port,
        handler,
        stopped_event,
    )


def load_admin_web_server(config, handler, stopped_event) -> SqueakAdminWebServer:
    return SqueakAdminWebServer(
        config.webadmin.host,
        config.webadmin.port,
        config.webadmin.username,
        config.webadmin.password,
        config.webadmin.use_ssl,
        config.webadmin.login_disabled,
        config.webadmin.allow_cors,
        handler,
        stopped_event,
    )


def load_admin_handler(lightning_client, squeak_controller):
    return SqueakAdminServerHandler(
        lightning_client,
        squeak_controller,
    )


def load_sqk_dir_path(config):
    sqk_dir = config.core.sqk_dir_path
    return Path(sqk_dir)


def load_db(config, network):
    connection_string = config.db.connection_string
    logger.info("connection string: {}".format(connection_string))
    logger.info("connection string type: {}".format(type(connection_string)))
    if not connection_string:
        sqk_dir = load_sqk_dir_path(config)
        logger.info(
            "Getting connection string from sqk dir: {}".format(sqk_dir))
        connection_string = get_sqlite_connection_string(sqk_dir, network)
    logger.info("Getting engine from connection string: {}".format(
        connection_string))
    engine = get_engine(connection_string)
    return SqueakDb(engine)


def load_bitcoin_client(config):
    return BitcoinCoreBitcoinClient(
        config.bitcoin.rpc_host,
        config.bitcoin.rpc_port,
        config.bitcoin.rpc_user,
        config.bitcoin.rpc_pass,
        config.bitcoin.rpc_use_ssl,
        config.bitcoin.rpc_ssl_cert,
    )


def start_admin_rpc_server(rpc_server):
    logger.info("Starting admin RPC server...")
    thread = threading.Thread(
        target=rpc_server.serve,
        args=(),
    )
    thread.start()


def load_admin_web_server_enabled(config):
    return config.webadmin.enabled


def start_admin_web_server(admin_web_server):
    logger.info("Starting admin web server...")
    thread = threading.Thread(
        target=admin_web_server.serve,
        args=(),
    )
    thread.start()

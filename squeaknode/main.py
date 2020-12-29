import argparse
import logging
import sys
import threading
from pathlib import Path

from squeak.params import SelectParams

from squeaknode.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeaknode.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeaknode.admin.webapp.app import SqueakAdminWebServer
from squeaknode.bitcoin.bitcoin_blockchain_client import BitcoinBlockchainClient
from squeaknode.config.config import Config
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.db.db_engine import get_engine
from squeaknode.db.db_engine import get_sqlite_connection_string
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.lightning.lnd_lightning_client import LNDLightningClient
from squeaknode.node.squeak_controller import SqueakController
from squeaknode.node.squeak_node import SqueakNode
from squeaknode.server.squeak_server_handler import SqueakServerHandler
from squeaknode.server.squeak_server_servicer import SqueakServerServicer

logger = logging.getLogger(__name__)


def load_lightning_client(config) -> LNDLightningClient:
    return LNDLightningClient(
        config.lnd_host,
        config.lnd_rpc_port,
        config.lnd_tls_cert_path,
        config.lnd_macaroon_path,
    )


def load_lightning_host_port(config) -> LightningAddressHostPort:
    return LightningAddressHostPort(
        config.lnd_external_host,
        config.lnd_port,
    )


def load_rpc_server(config, handler) -> SqueakServerServicer:
    return SqueakServerServicer(
        config.server_rpc_host,
        config.server_rpc_port,
        handler,
    )


def load_admin_rpc_server(config, handler) -> SqueakAdminServerServicer:
    return SqueakAdminServerServicer(
        config.admin_rpc_host,
        config.admin_rpc_port,
        handler,
    )


def load_admin_web_server(config, handler) -> SqueakAdminWebServer:
    return SqueakAdminWebServer(
        config.webadmin_host,
        config.webadmin_port,
        config.webadmin_username,
        config.webadmin_password,
        config.webadmin_use_ssl,
        config.webadmin_login_disabled,
        config.webadmin_allow_cors,
        handler,
    )


def load_network(config):
    return config.squeaknode_network


def load_price_msat(config):
    return config.squeaknode_price_msat


def load_max_squeaks_per_address_per_hour(config):
    return config.squeaknode_max_squeaks_per_address_per_hour


def load_sync_interval_s(config):
    return config.squeaknode_sync_interval_s


def load_handler(squeak_controller):
    return SqueakServerHandler(squeak_controller)


def load_admin_handler(lightning_client, squeak_controller):
    return SqueakAdminServerHandler(
        lightning_client,
        squeak_controller,
    )


def load_sqk_dir_path(config):
    sqk_dir = config.squeaknode_sqk_dir
    return Path(sqk_dir)


def load_db(config, network):
    connection_string = config.db_connection_string
    if not connection_string:
        sqk_dir = load_sqk_dir_path(config)
        connection_string = get_sqlite_connection_string(sqk_dir, network)
    engine = get_engine(connection_string)
    return SqueakDb(engine)


def load_blockchain_client(config):
    return BitcoinBlockchainClient(
        config.bitcoin_rpc_host,
        config.bitcoin_rpc_port,
        config.bitcoin_rpc_user,
        config.bitcoin_rpc_pass,
        config.bitcoin_rpc_use_ssl,
        config.bitcoin_rpc_ssl_cert,
    )


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


def start_admin_rpc_server(rpc_server):
    logger.info("Starting admin RPC server...")
    thread = threading.Thread(
        target=rpc_server.serve,
        args=(),
    )
    thread.daemon = True
    thread.start()


def load_admin_web_server_enabled(config):
    return config.webadmin_enabled


def start_admin_web_server(admin_web_server):
    logger.info("Starting admin web server...")
    thread = threading.Thread(
        target=admin_web_server.serve,
        args=(),
    )
    thread.daemon = True
    thread.start()


def parse_args():
    parser = argparse.ArgumentParser(
        description="squeaknode runs a node using squeak protocol. ",
    )
    parser.add_argument(
        "--config",
        dest="config",
        type=str,
        help="Path to the config file.",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        type=str,
        default="info",
        help="Logging level",
    )
    subparsers = parser.add_subparsers(help="sub-command help")

    # create the parser for the "run-server" command
    parser_run_server = subparsers.add_parser(
        "run-server", help="run-server help")
    parser_run_server.set_defaults(func=run_server)

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()

    # Set the log level
    level = args.log_level.upper()
    logging.getLogger().setLevel(level)

    logger.info("Starting squeaknode...")
    config = Config(args.config)
    logger.info("config: {}".format(config))

    # Set the log level again
    level = config.squeaknode_log_level
    logging.getLogger().setLevel(level)

    args.func(config)


def run_server(config):
    # load the network
    network = load_network(config)
    SelectParams(network)

    # load the db
    squeak_db = load_db(config, network)
    squeak_db.init()

    # load the price
    price_msat = load_price_msat(config)

    # load the max squeaks per block per address
    max_squeaks_per_address_per_hour = load_max_squeaks_per_address_per_hour(
        config)

    # load the lightning client
    lightning_client = load_lightning_client(config)
    lightning_host_port = load_lightning_host_port(config)

    # load the blockchain client
    blockchain_client = load_blockchain_client(config)

    # load enable sync config
    sync_interval_s = load_sync_interval_s(config)

    squeak_controller = SqueakController(
        squeak_db,
        blockchain_client,
        lightning_client,
        lightning_host_port,
        price_msat,
        max_squeaks_per_address_per_hour,
    )

    # Create and start the squeak node
    squeak_node = SqueakNode(squeak_controller, sync_interval_s)
    squeak_node.start_running()

    # start admin rpc server
    admin_handler = load_admin_handler(lightning_client, squeak_controller)
    admin_rpc_server = load_admin_rpc_server(config, admin_handler)
    start_admin_rpc_server(admin_rpc_server)

    # start admin web server
    admin_web_server_enabled = load_admin_web_server_enabled(config)
    if admin_web_server_enabled:
        admin_web_server = load_admin_web_server(config, admin_handler)
        start_admin_web_server(admin_web_server)

    # start rpc server
    handler = load_handler(squeak_controller)
    server = load_rpc_server(config, handler)
    server.serve()


if __name__ == "__main__":
    main()

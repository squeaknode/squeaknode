import argparse
import logging
import sys
import threading
from configparser import ConfigParser
from pathlib import Path
from os import environ

from squeak.params import SelectParams

from squeaknode.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeaknode.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeaknode.admin.webapp.app import SqueakAdminWebServer
from squeaknode.blockchain.bitcoin_blockchain_client import BitcoinBlockchainClient
from squeaknode.common.lnd_lightning_client import LNDLightningClient
from squeaknode.db.db_engine import get_postgres_engine, get_sqlite_engine
from squeaknode.db.squeak_db import SqueakDb
from squeaknode.node.squeak_node import SqueakNode
from squeaknode.server.lightning_address import LightningAddressHostPort
from squeaknode.server.squeak_server_handler import SqueakServerHandler
from squeaknode.server.squeak_server_servicer import SqueakServerServicer

from squeaknode.config.config import Config


logger = logging.getLogger(__name__)

SQK_DIR_NAME = ".sqk"

def load_lightning_client(config) -> LNDLightningClient:
    return LNDLightningClient(
        config.lnd_host,
        config.lnd_rpc_port,
        config.lnd_tls_cert_path,
        config.lnd_macaroon_path,
    )


def load_lightning_host_port(config) -> LNDLightningClient:
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
    return config["squeaknode"]["network"]


def load_price(config):
    return int(config["squeaknode"]["price"])


def load_database(config):
    return config["squeaknode"]["database"]


def load_max_squeaks_per_address_per_hour(config):
    return int(config["squeaknode"]["max_squeaks_per_address_per_hour"])


def load_enable_sync(config):
    return config["squeaknode"].getboolean("enable_sync")


def load_handler(squeak_node):
    return SqueakServerHandler(squeak_node)


def load_admin_handler(lightning_client, squeak_node):
    return SqueakAdminServerHandler(
        lightning_client,
        squeak_node,
    )


def load_sqk_dir_path(config):
    sqk_dir = config.get("squeaknode", "sqk_dir", fallback=None)
    if sqk_dir:
        return Path(sqk_dir)
    else:
        return Path.home().joinpath(SQK_DIR_NAME)


def load_db(config, network):
    database = load_database(config)
    logger.info("database: " + database)
    if database == "postgresql":
        engine = get_postgres_engine(
            config["postgresql"]["user"],
            config["postgresql"]["password"],
            config["postgresql"]["host"],
            config["postgresql"]["database"],
        )
        return SqueakDb(engine, schema=network)
    elif database == "sqlite":
        sqk_dir = load_sqk_dir_path(config)
        logger.info("Loaded sqk_dir: {}".format(sqk_dir))
        data_dir = sqk_dir.joinpath("data").joinpath(network)
        data_dir.mkdir(parents=True, exist_ok=True)
        engine = get_sqlite_engine(data_dir)
        return SqueakDb(engine)


def load_blockchain_client(config):
    return BitcoinBlockchainClient(
        config.bitcoin_rpc_host,
        config.bitcoin_rpc_port,
        config.bitcoin_rpc_user,
        config.bitcoin_rpc_pass,
    )


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


def start_admin_rpc_server(rpc_server):
    logger.info("Calling start_admin_rpc_server...")
    thread = threading.Thread(
        target=rpc_server.serve,
        args=(),
    )
    thread.daemon = True
    thread.start()


def load_admin_web_server_enabled(config):
    return config.webadmin_enabled


def start_admin_web_server(admin_web_server):
    logger.info("Calling start_admin_web_server...")
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
    parser_run_server = subparsers.add_parser("run-server", help="run-server help")
    parser_run_server.set_defaults(func=run_server)

    return parser.parse_args()


def main():
    logger.info("Running main() in server...")
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()

    # Set the log level
    level = args.log_level.upper()
    logger.info("level: " + level)
    logging.getLogger().setLevel(level)

    # Get the config object
    config = ConfigParser()
    config.read(args.config)

    new_config = Config(args.config)
    logger.info("config: {}".format(new_config))
    logger.info("config.configs: {}".format(new_config.configs))
    logger.info("new_config.foobar: {}".format(new_config.foobar))
    logger.info("new_config.bitcoin_rpc_host: {}".format(new_config.bitcoin_rpc_host))

    args.func(config, new_config)


def run_server(config, new_config):
    # load the network
    network = load_network(config)
    logger.info("network: " + network)
    SelectParams(network)

    # load postgres db
    squeak_db = load_db(config, network)
    logger.info("squeak_db: " + str(squeak_db))
    squeak_db.init()

    # load the price
    price = load_price(config)

    # load the max squeaks per block per address
    max_squeaks_per_address_per_hour = load_max_squeaks_per_address_per_hour(config)

    # load the lightning client
    lightning_client = load_lightning_client(new_config)
    lightning_host_port = load_lightning_host_port(new_config)
    logger.info("Loaded lightning_host_port: {}".format(lightning_host_port))

    # load the blockchain client
    blockchain_client = load_blockchain_client(new_config)

    # load enable sync config
    enable_sync = load_enable_sync(config)

    # Create and start the squeak node
    squeak_node = SqueakNode(
        squeak_db,
        blockchain_client,
        lightning_client,
        lightning_host_port,
        price,
        max_squeaks_per_address_per_hour,
        enable_sync,
    )
    squeak_node.start_running()

    # start admin rpc server
    admin_handler = load_admin_handler(lightning_client, squeak_node)
    admin_rpc_server = load_admin_rpc_server(new_config, admin_handler)
    start_admin_rpc_server(admin_rpc_server)

    # start admin web server
    admin_web_server_enabled = load_admin_web_server_enabled(new_config)
    if admin_web_server_enabled:
        admin_web_server = load_admin_web_server(new_config, admin_handler)
        start_admin_web_server(admin_web_server)

    # start rpc server
    handler = load_handler(squeak_node)
    server = load_rpc_server(new_config, handler)
    server.serve()


if __name__ == "__main__":
    main()

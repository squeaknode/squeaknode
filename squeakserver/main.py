import argparse
import logging
import sys
import threading
from configparser import ConfigParser

from squeak.params import SelectParams

import proto.lnd_pb2 as ln
import proto.lnd_pb2_grpc as lnrpc
from squeakserver.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeakserver.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeakserver.blockchain.bitcoin_blockchain_client import BitcoinBlockchainClient
from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.db.db_params import parse_db_params
from squeakserver.db.db_engine import get_postgres_engine
from squeakserver.node.squeak_node import SqueakNode
from squeakserver.server.lightning_address import LightningAddressHostPort
from squeakserver.db.squeak_db import SqueakDb
from squeakserver.server.squeak_server_handler import SqueakServerHandler
from squeakserver.server.squeak_server_servicer import SqueakServerServicer

logger = logging.getLogger(__name__)


def load_lightning_client(config) -> LNDLightningClient:
    return LNDLightningClient(
        config["lnd"]["host"],
        config["lnd"]["rpc_port"],
        config["lnd"]["tls_cert_path"],
        config["lnd"]["macaroon_path"],
        ln,
        lnrpc,
    )


def load_lightning_host_port(config) -> LNDLightningClient:
    lnd_host = config.get("lnd", "external_host", fallback=None)
    lnd_port = int(config["lnd"]["port"])
    return LightningAddressHostPort(lnd_host, lnd_port,)


def load_rpc_server(config, handler) -> SqueakServerServicer:
    return SqueakServerServicer(
        config["server"]["rpc_host"], config["server"]["rpc_port"], handler,
    )


def load_admin_rpc_server(config, handler) -> SqueakAdminServerServicer:
    return SqueakAdminServerServicer(
        config["admin"]["rpc_host"], config["admin"]["rpc_port"], handler,
    )


def load_network(config):
    return config["squeaknode"]["network"]


def load_price(config):
    return int(config["squeaknode"]["price"])


def load_max_squeaks_per_address_per_hour(config):
    return int(config["squeaknode"]["max_squeaks_per_address_per_hour"])


def load_handler(squeak_node):
    return SqueakServerHandler(squeak_node)


def load_admin_handler(lightning_client, squeak_node):
    return SqueakAdminServerHandler(lightning_client, squeak_node,)


def load_db_engine(config):
    # TODO: check if using postgres
    if True:
        return get_postgres_engine(
            config["postgresql"]["user"],
            config["postgresql"]["password"],
            config["postgresql"]["host"],
            config["postgresql"]["database"],
        )


def load_db(config, schema):
    engine = load_db_engine(config)
    return SqueakDb(engine, schema)


def load_blockchain_client(config):
    return BitcoinBlockchainClient(
        config["bitcoin"]["rpc_host"],
        config["bitcoin"]["rpc_port"],
        config["bitcoin"]["rpc_user"],
        config["bitcoin"]["rpc_pass"],
    )


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


def start_admin_rpc_server(rpc_server):
    logger.info("Calling start_admin_rpc_server...")
    thread = threading.Thread(target=rpc_server.serve, args=(),)
    thread.daemon = True
    thread.start()


def parse_args():
    parser = argparse.ArgumentParser(
        description="squeakserver runs a node using squeak protocol. ",
    )
    parser.add_argument(
        "--config", dest="config", type=str, help="Path to the config file.",
    )
    parser.add_argument(
        "--log-level", dest="log_level", type=str, default="info", help="Logging level",
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

    args.func(config)


def run_server(config):
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
    lightning_client = load_lightning_client(config)
    lightning_host_port = load_lightning_host_port(config)

    # load the blockchain client
    blockchain_client = load_blockchain_client(config)

    # Create and start the squeak node
    squeak_node = SqueakNode(
        squeak_db,
        blockchain_client,
        lightning_client,
        lightning_host_port,
        price,
        max_squeaks_per_address_per_hour,
    )
    squeak_node.start_running()

    # start admin rpc server
    admin_handler = load_admin_handler(lightning_client, squeak_node)
    admin_rpc_server = load_admin_rpc_server(config, admin_handler)
    start_admin_rpc_server(admin_rpc_server)

    # start rpc server
    handler = load_handler(squeak_node)
    server = load_rpc_server(config, handler)
    server.serve()


if __name__ == "__main__":
    main()

import argparse
import logging
import threading
import time

from configparser import ConfigParser

from squeak.params import SelectParams

from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.btcd_blockchain_client import BTCDBlockchainClient
from squeaknode.common.lnd_lightning_client import LNDLightningClient
from squeaknode.client.rpc.route_guide_server import RouteGuideServicer
from squeaknode.client.clientsqueaknode import SqueakNodeClient
from squeaknode.client.db import get_db
from squeaknode.client.db import close_db
from squeaknode.client.db import initialize_db


def load_blockchain_client(rpc_host, rpc_port, rpc_user, rpc_pass) -> BlockchainClient:
    return BTCDBlockchainClient(
        host=rpc_host,
        port=rpc_port,
        rpc_user=rpc_user,
        rpc_password=rpc_pass,
    )


def load_lightning_client(rpc_host, rpc_port, network) -> LightningClient:
    return LNDLightningClient(
        host=rpc_host,
        port=rpc_port,
        network=network,
    )


def _load_client(blockchain_client, lightning_client):
    node = SqueakNodeClient(blockchain_client, lightning_client)
    return node


def _start_route_guide_rpc_server(node):
    server = RouteGuideServicer(node)
    thread = threading.Thread(
        target=server.serve,
        args=(),
    )
    thread.daemon = True
    thread.start()
    return server, thread


def parse_args():
    parser = argparse.ArgumentParser(
        description="squeaknode runs a node using squeak protocol. ",
    )
    parser.add_argument(
        '--config',
        dest='config',
        type=str,
        help='Path to the config file.',
    )
    parser.add_argument(
        '--log-level',
        dest='log_level',
        type=str,
        default='info',
        help='Logging level',
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "init-db" command
    parser_init_db = subparsers.add_parser('init-db', help='init-db help')
    parser_init_db.set_defaults(func=init_db)

    # create the parser for the "run-client" command
    parser_run_client = subparsers.add_parser('run-client', help='run-client help')
    parser_run_client.set_defaults(func=run_client)

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()

    # Set the log level
    level = args.log_level.upper()
    print("level: " + level)
    logging.getLogger().setLevel(level)

    # Get the config object
    config = ConfigParser()
    config.read(args.config)

    args.func(config)


def init_db(config):
    db = get_db()
    initialize_db(db)
    print("Initialized the database.")


def run_client(config):
    print('network:', config['DEFAULT']['network'])
    SelectParams(config['DEFAULT']['network'])

    blockchain_client = load_blockchain_client(
        config['btcd']['rpc_host'],
        config['btcd']['rpc_port'],
        config['btcd']['rpc_user'],
        config['btcd']['rpc_pass'],
    )
    lightning_client = load_lightning_client(
        config['lnd']['rpc_host'],
        config['lnd']['rpc_port'],
        config['lnd']['network'],
    )

    db = get_db()

    node = _load_client(blockchain_client, lightning_client)

    # start rpc server
    route_guide_server, route_guide_server_thread = _start_route_guide_rpc_server(node)

    while True:
        time.sleep(10)

    close_db(db)


if __name__ == '__main__':
    main()

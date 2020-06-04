import argparse
import logging
import signal
import sys
import threading
import time

from configparser import ConfigParser

from squeak.params import SelectParams
from squeak.core.signing import CSigningKey


import squeaknode.common.lnd_pb2 as ln
import squeaknode.common.lnd_pb2_grpc as lnrpc

from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lnd_lightning_client import LNDLightningClient
from squeaknode.common.btcd_blockchain_client import BTCDBlockchainClient
from squeaknode.common.lnd_lightning_client import LNDLightningClient
from squeaknode.client.rpc.route_guide_server import RouteGuideServicer
from squeaknode.client.clientsqueaknode import SqueakNodeClient
from squeaknode.client.db import SQLiteDBFactory
from squeaknode.client.db import initialize_db
from squeaknode.client.rpc_client import RPCClient


def load_blockchain_client(config) -> BlockchainClient:
    return BTCDBlockchainClient(
        config['btcd']['rpc_host'],
        config['btcd']['rpc_port'],
        config['btcd']['rpc_user'],
        config['btcd']['rpc_pass'],
    )


def load_lightning_client(config) -> LNDLightningClient:
    return LNDLightningClient(
        config['lnd']['rpc_host'],
        config['lnd']['rpc_port'],
        config['lnd']['network'],
        ln,
        lnrpc,
    )


def load_rpc_client(config) -> RPCClient:
    return RPCClient(
        config['server']['rpc_host'],
        config['server']['rpc_port'],
    )


def load_client(blockchain_client, lightning_client, signing_key, db, rpc_client):
    return SqueakNodeClient(
        blockchain_client,
        lightning_client,
        signing_key,
        db,
        rpc_client,
    )


def load_signing_key(config):
    signing_key_str = config['client']['private_key']
    if signing_key_str:
        return CSigningKey(signing_key_str)


def load_db_factory(config):
    return SQLiteDBFactory('db_file_path')


def start_rpc_server(node):
    server = RouteGuideServicer(node)
    thread = threading.Thread(
        target=server.serve,
        args=(),
    )
    thread.daemon = True
    thread.start()
    return server, thread


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


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
    db_factory = load_db_factory(config)
    with db_factory.make_conn() as conn:
        initialize_db(conn)
    print("Initialized the database.")


def run_client(config):
    print('network:', config['DEFAULT']['network'])
    SelectParams(config['DEFAULT']['network'])

    blockchain_client = load_blockchain_client(config)
    lightning_client = load_lightning_client(config)
    db_factory = load_db_factory(config)
    signing_key = load_signing_key(config)
    rpc_client = load_rpc_client(config)
    node = load_client(blockchain_client, lightning_client, signing_key, db_factory, rpc_client)

    # start rpc server
    rpc_server, rpc_server_thread = start_rpc_server(node)

    signal.signal(signal.SIGTERM, sigterm_handler)

    print("Starting client...")
    node.start()
    try:
        while True:
            time.sleep(1)
    finally:
        print("Shutting down...")
        node.stop()


if __name__ == '__main__':
    main()

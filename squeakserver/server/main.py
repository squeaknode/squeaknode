import socket
import argparse
import logging
import signal
import sys
import threading
import time

from configparser import ConfigParser

from squeak.params import SelectParams
from squeak.core.signing import CSigningKey

import squeakserver.common.rpc.lnd_pb2 as ln
import squeakserver.common.rpc.lnd_pb2_grpc as lnrpc

from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.server.lightning_address import LightningAddressHostPort
from squeakserver.server.squeak_server_servicer import SqueakServerServicer
from squeakserver.server.squeak_server_handler import SqueakServerHandler
from squeakserver.server.db_params import parse_db_params
from squeakserver.server.postgres_db import PostgresDb


def load_lightning_client(config) -> LNDLightningClient:
    return LNDLightningClient(
        config['lnd']['rpc_host'],
        config['lnd']['rpc_port'],
        config['lnd']['network'],
        ln,
        lnrpc,
    )


def load_lightning_host_port(config) -> LNDLightningClient:
    lnd_ip_address = socket.gethostbyname(
        config['lnd']['rpc_host'],
    )
    lnd_port = config['lnd']['port']
    return LightningAddressHostPort(
        lnd_ip_address,
        lnd_port,
    )


def load_rpc_server(config, handler) -> SqueakServerServicer:
    return SqueakServerServicer(
        config['server']['rpc_host'],
        config['server']['rpc_port'],
        handler,
    )


def start_rpc_server(handler):
    print('Calling start_rpc_server...', flush=True)
    server = SqueakServerServicer(handler)
    # thread = threading.Thread(
    #     target=server.serve,
    #     args=(),
    # )
    # thread.daemon = True
    # thread.start()
    # return server, thread
    server.serve()


def load_handler(lightning_host_port, lightning_client, postgres_db):
    return SqueakServerHandler(
        lightning_host_port,
        lightning_client,
        postgres_db
    )


def load_db_params(config):
    return parse_db_params(config)


def load_postgres_db(config):
    db_params = parse_db_params(config)
    return PostgresDb(db_params)


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        description="squeakserver runs a node using squeak protocol. ",
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

    # # create the parser for the "init-db" command
    # parser_init_db = subparsers.add_parser('init-db', help='init-db help')
    # parser_init_db.set_defaults(func=init_db)

    # create the parser for the "run-server" command
    parser_run_server = subparsers.add_parser('run-server', help='run-server help')
    parser_run_server.set_defaults(func=run_server)

    return parser.parse_args()


def main():
    print("Running main() in server...", flush=True)
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


# def init_db(config):
#     db_factory = load_db_factory(config)
#     with db_factory.make_conn() as conn:
#         initialize_db(conn)
#     print("Initialized the database.")


def run_server(config):
    print('network:', config['DEFAULT']['network'], flush=True)
    # SelectParams(config['DEFAULT']['network'])
    SelectParams("mainnet")

    # load the db params
    db_params = load_db_params(config)
    print('db params: ' + str(db_params), flush=True)

    # load postgres db
    postgres_db = load_postgres_db(config)
    print('postgres_db: ' + str(postgres_db), flush=True)
    postgres_db.get_connection()

    print('starting lightning client here...', flush=True)
    lightning_client = load_lightning_client(config)
    lightning_host_port = load_lightning_host_port(config)
    # db_factory = load_db_factory(config)
    handler = load_handler(lightning_host_port, lightning_client, postgres_db)

    # start rpc server
    # start_rpc_server(handler)

    server = load_rpc_server(config, handler)
    server.serve()

    # rpc_server, rpc_server_thread = start_rpc_server(handler)
    # print("rpc server started...", flush=True)

    # signal.signal(signal.SIGTERM, sigterm_handler)

    # print("sleeping....", flush=True)
    # try:
    #     while True:
    #         time.sleep(1)
    # finally:
    #     print("Shutting down...", flush=True)


if __name__ == '__main__':
    main()

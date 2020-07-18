import argparse
import logging
import sys
import threading

from configparser import ConfigParser

from squeak.params import SelectParams

import proto.lnd_pb2 as ln
import proto.lnd_pb2_grpc as lnrpc

from squeakserver.admin.squeak_admin_server_servicer import SqueakAdminServerServicer
from squeakserver.admin.squeak_admin_server_handler import SqueakAdminServerHandler
from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.server.lightning_address import LightningAddressHostPort
from squeakserver.server.squeak_server_servicer import SqueakServerServicer
from squeakserver.server.squeak_server_handler import SqueakServerHandler
from squeakserver.server.db_params import parse_db_params
from squeakserver.server.postgres_db import PostgresDb
from squeakserver.node.squeak_block_verifier import SqueakBlockVerifier
from squeakserver.node.squeak_block_periodic_worker import SqueakBlockPeriodicWorker
from squeakserver.blockchain.bitcoin_blockchain_client import BitcoinBlockchainClient


logger = logging.getLogger(__name__)


def load_lightning_client(config) -> LNDLightningClient:
    if int(config['server']['price']) == 0:
        return None
    return LNDLightningClient(
        config['lnd']['host'],
        config['lnd']['rpc_port'],
        config['lnd']['tls_cert_path'],
        config['lnd']['macaroon_path'],
        ln,
        lnrpc,
    )


def load_lightning_host_port(config) -> LNDLightningClient:
    if int(config['server']['price']) == 0:
        return None
    lnd_host = config['lnd']['host']
    if 'external_host' in config['lnd']:
        lnd_host = config['lnd']['external_host']
    lnd_port = int(config['lnd']['port'])
    return LightningAddressHostPort(
        lnd_host,
        lnd_port,
    )


def load_rpc_server(config, handler) -> SqueakServerServicer:
    return SqueakServerServicer(
        config['server']['rpc_host'],
        config['server']['rpc_port'],
        handler,
    )


def load_admin_rpc_server(config, handler) -> SqueakAdminServerServicer:
    return SqueakAdminServerServicer(
        config['admin']['rpc_host'],
        config['admin']['rpc_port'],
        handler,
    )


def load_price(config):
    return int(config['server']['price'])


def load_handler(lightning_host_port, lightning_client, postgres_db, price):
    return SqueakServerHandler(
        lightning_host_port,
        lightning_client,
        postgres_db,
        price,
    )


def load_admin_handler(lightning_client, postgres_db):
    return SqueakAdminServerHandler(
        lightning_client,
        postgres_db,
    )


def load_db_params(config):
    return parse_db_params(config)


def load_postgres_db(config):
    db_params = parse_db_params(config)
    return PostgresDb(db_params)


def load_blockchain_client(config):
    return BitcoinBlockchainClient(
        config['bitcoin']['rpc_host'],
        config['bitcoin']['rpc_host'],
        config['bitcoin']['rpc_user'],
        config['bitcoin']['rpc_pass'],
    )


def load_squeak_block_verifier(postgres_db, blockchain_client):
    return SqueakBlockVerifier(postgres_db, blockchain_client)


def load_squeak_block_periodic_worker(squeak_block_verifier, postgres_db):
    return SqueakBlockPeriodicWorker(squeak_block_verifier, postgres_db)


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


def start_admin_rpc_server(rpc_server):
    logger.info('Calling start_admin_rpc_server...')
    thread = threading.Thread(
        target=rpc_server.serve,
        args=(),
    )
    thread.daemon = True
    thread.start()


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


# def init_db(config):
#     db_factory = load_db_factory(config)
#     with db_factory.make_conn() as conn:
#         initialize_db(conn)
#     logger.info("Initialized the database.")


def run_server(config):
    logger.info('network: ' + config['DEFAULT']['network'])
    # SelectParams(config['DEFAULT']['network'])
    SelectParams("mainnet")

    # load the db params
    db_params = load_db_params(config)
    logger.info('db params: ' + str(db_params))

    # load postgres db
    postgres_db = load_postgres_db(config)
    logger.info('postgres_db: ' + str(postgres_db))
    postgres_db.get_version()
    postgres_db.init()

    logger.info('starting lightning client here...')
    price = load_price(config)
    lightning_client = load_lightning_client(config)
    lightning_host_port = load_lightning_host_port(config)

    # Start the squeak block verifier
    bitcoin_blockchain_client = load_blockchain_client(config)
    squeak_block_verifier = load_squeak_block_verifier(postgres_db, bitcoin_blockchain_client)
    squeak_block_periodic_worker = load_squeak_block_periodic_worker(squeak_block_verifier, postgres_db)
    squeak_block_periodic_worker.start_running()

    # start admin rpc server
    admin_handler = load_admin_handler(lightning_client, postgres_db)
    admin_rpc_server = load_admin_rpc_server(config, admin_handler)
    start_admin_rpc_server(admin_rpc_server)

    # start rpc server
    handler = load_handler(lightning_host_port, lightning_client, postgres_db, price)
    server = load_rpc_server(config, handler)
    server.serve()


if __name__ == '__main__':
    main()

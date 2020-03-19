import argparse
import logging
import threading
import time

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


def _start_node(blockchain_client, lightning_client):
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

    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "init-db" command
    parser_init_db = subparsers.add_parser('init-db', help='init-db help')
    parser_init_db.set_defaults(func=init_db)

    # create the parser for the "run-client" command
    parser_run_client = subparsers.add_parser('run-client', help='run-client help')
    parser_run_client.add_argument(
        '--network',
        dest='network',
        type=str,
        default='mainnet',
        choices=['mainnet', 'testnet', 'regtest', 'simnet'],
        help='The bitcoin network to use',
    )
    parser_run_client.add_argument(
        '--rpcport',
        dest='rpcport',
        type=int,
        default=None,
        help='RPC server port number',
    )
    parser_run_client.add_argument(
        '--rpcuser',
        dest='rpcuser',
        type=str,
        default='',
        help='RPC username',
    )
    parser_run_client.add_argument(
        '--rpcpass',
        dest='rpcpass',
        type=str,
        default='',
        help='RPC password',
    )
    parser_run_client.add_argument(
        '--btcd.rpchost',
        dest='btcd_rpchost',
        type=str,
        default='localhost',
        help='Blockchain (bitcoin) backend hostname',
    )
    parser_run_client.add_argument(
        '--btcd.rpcport',
        dest='btcd_rpcport',
        type=int,
        default=18332,
        help='Blockchain (bitcoin) backend port',
    )
    parser_run_client.add_argument(
        '--btcd.rpcuser',
        dest='btcd_rpcuser',
        type=str,
        default='',
        help='Blockchain (bitcoin) backend username',
    )
    parser_run_client.add_argument(
        '--btcd.rpcpass',
        dest='btcd_rpcpass',
        type=str,
        default='',
        help='Blockchain (bitcoin) backend password',
    )
    parser_run_client.add_argument(
        '--lnd.rpchost',
        dest='lnd_rpchost',
        type=str,
        default='localhost',
        help='Lightning network backend hostname',
    )
    parser_run_client.add_argument(
        '--lnd.rpcport',
        dest='lnd_rpcport',
        type=int,
        default=10009,
        help='Lightning network backend port',
    )
    parser_run_client.add_argument(
        '--log-level',
        dest='log_level',
        type=str,
        default='info',
        help='Logging level',
    )
    parser_run_client.set_defaults(func=run_client)

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()
    args.func(args)


def init_db(args):
    db = get_db()
    initialize_db(db)
    print("Initialized the database.")


def run_client(args):
    level = args.log_level.upper()
    print("level: " + level, flush=True)
    logging.getLogger().setLevel(level)

    print('network:', args.network, flush=True)
    SelectParams(args.network)

    blockchain_client = load_blockchain_client(
        args.btcd_rpchost,
        args.btcd_rpcport,
        args.btcd_rpcuser,
        args.btcd_rpcpass,
    )
    lightning_client = load_lightning_client(
        args.lnd_rpchost,
        args.lnd_rpcport,
        args.network,
    )

    db = get_db()

    node = _start_node(blockchain_client, lightning_client)

    # start rpc server
    route_guide_server, route_guide_server_thread = _start_route_guide_rpc_server(node)

    while True:
        time.sleep(10)

    close_db(db)


if __name__ == '__main__':
    main()

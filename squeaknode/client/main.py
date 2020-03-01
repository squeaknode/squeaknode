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


# def _start_node(blockchain, lightning_client):
#     node = ClientSqueakNode(blockchain, lightning_client)
#     peer_handler = PeerHandler(node)
#     thread = threading.Thread(
#         target=node.start,
#         args=(peer_handler,),
#     )
#     thread.daemon = True
#     thread.start()
#     return node, thread


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
        '--network',
        dest='network',
        type=str,
        default='mainnet',
        choices=['mainnet', 'testnet', 'regtest', 'simnet'],
        help='The bitcoin network to use',
    )
    parser.add_argument(
        '--rpcport',
        dest='rpcport',
        type=int,
        default=None,
        help='RPC server port number',
    )
    parser.add_argument(
        '--rpcuser',
        dest='rpcuser',
        type=str,
        default='',
        help='RPC username',
    )
    parser.add_argument(
        '--rpcpass',
        dest='rpcpass',
        type=str,
        default='',
        help='RPC password',
    )
    parser.add_argument(
        '--btcd.rpchost',
        dest='btcd_rpchost',
        type=str,
        default='localhost',
        help='Blockchain (bitcoin) backend hostname',
    )
    parser.add_argument(
        '--btcd.rpcport',
        dest='btcd_rpcport',
        type=int,
        default=18332,
        help='Blockchain (bitcoin) backend port',
    )
    parser.add_argument(
        '--btcd.rpcuser',
        dest='btcd_rpcuser',
        type=str,
        default='',
        help='Blockchain (bitcoin) backend username',
    )
    parser.add_argument(
        '--btcd.rpcpass',
        dest='btcd_rpcpass',
        type=str,
        default='',
        help='Blockchain (bitcoin) backend password',
    )
    parser.add_argument(
        '--lnd.rpchost',
        dest='lnd_rpchost',
        type=str,
        default='localhost',
        help='Lightning network backend hostname',
    )
    parser.add_argument(
        '--lnd.rpcport',
        dest='lnd_rpcport',
        type=int,
        default=10009,
        help='Lightning network backend port',
    )
    parser.add_argument(
        '--log-level',
        dest='log_level',
        type=str,
        default='info',
        help='Logging level',
    )
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()
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

    # node, thread = _start_node(blockchain, lightning_client)

    # start rpc server
    route_guide_server, route_guide_server_thread = _start_route_guide_rpc_server(node)

    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()

import argparse
import logging
from signal import SIGHUP
from signal import SIGINT
from signal import signal
from signal import SIGTERM
from threading import Event

from squeaknode.config.config import SqueaknodeConfig
from squeaknode.node.squeak_node import SqueakNode


logger = logging.getLogger(__name__)


stop_event = Event()


def handler(signum, frame):
    stop_event.set()


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
    # subparsers = parser.add_subparsers(help="sub-command help")

    # # create the parser for the "run-server" command
    # parser_run_server = subparsers.add_parser(
    #     "run-server", help="run-server help")
    # parser_run_server.set_defaults(func=run_server)

    # return parser.parse_args()

    parser.set_defaults(func=run_node)
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.ERROR)
    args = parse_args()

    # Set the log level
    level = args.log_level.upper()
    logging.getLogger().setLevel(level)

    logger.info("Starting squeaknode...")
    config = SqueaknodeConfig(args.config)
    config.read()
    logger.info("config: {}".format(config))
    logger.info("bitcoin rpc host: {}, rpc port: {}, rpc user: {}, rpc pass: {}, rpc use_ssl: {}, rpc ssl cert: {}".format(
        config.bitcoin.rpc_host,
        config.bitcoin.rpc_port,
        config.bitcoin.rpc_user,
        config.bitcoin.rpc_pass,
        config.bitcoin.rpc_use_ssl,
        config.bitcoin.rpc_ssl_cert,
    ))

    # Set the log level again
    level = config.core.log_level
    logging.getLogger().setLevel(level)

    args.func(config)


def run_node(config):
    signal(SIGTERM, handler)
    signal(SIGINT, handler)
    signal(SIGHUP, handler)
    squeak_node = SqueakNode(config)
    print('Starting Squeaknode...')
    squeak_node.start_running()
    stop_event.wait()
    print('Shutting down Squeaknode...')
    squeak_node.stop_running()


if __name__ == "__main__":
    main()

import argparse
import logging
import sys

from squeaknode.config.config import SqueaknodeConfig
from squeaknode.node.received_payments_subscription_client import (
    OpenReceivedPaymentsSubscriptionClient,
)
from squeaknode.node.squeak_node import SqueakNode


logger = logging.getLogger(__name__)


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


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
    squeak_node = SqueakNode(config)
    squeak_node.start_running()


if __name__ == "__main__":
    main()

import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.client.squeak_store import SqueakStore
from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.squeak_maker import SqueakMaker
from squeaknode.client.db import SQLiteDBFactory
from squeaknode.client.uploader import Uploader
from squeaknode.client.rpc_client import RPCClient


logger = logging.getLogger(__name__)


class SqueakServerHandler(object):
    """Handles server commands.
    """

    def __init__(
            self,
            lightning_client: LightningClient,
    ) -> None:
        self.lightning_client = lightning_client

    def say_hello(self):
        return 'hello from the handler'

    def handle_posted_squeak(self, squeak):
        logger.info("Handler got posted squeak: " + str(squeak))
        return squeak.GetHash()


# class ClientNodeError(Exception):
#     pass


# class MissingSigningKeyError(ClientNodeError):
#     def __str__(self):
#         return 'Missing signing key.'

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
from squeaknode.server.postgres_db import PostgresDb


logger = logging.getLogger(__name__)


class SqueakServerHandler(object):
    """Handles server commands.
    """

    def __init__(
            self,
            lightning_client: LightningClient,
            postgres_db: PostgresDb,
    ) -> None:
        self.lightning_client = lightning_client
        self.postgres_db = postgres_db

    def say_hello(self):
        return 'hello from the handler'

    def handle_posted_squeak(self, squeak):
        logger.info("Handler got posted squeak: " + str(squeak))

        # Insert the squeak in the database
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        logger.info("Inserted squeak and got back hash: " + str(inserted_squeak_hash))

        return squeak.GetHash()


# class ClientNodeError(Exception):
#     pass


# class MissingSigningKeyError(ClientNodeError):
#     def __str__(self):
#         return 'Missing signing key.'

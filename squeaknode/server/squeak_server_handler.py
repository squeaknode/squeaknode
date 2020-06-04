import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lnd_lightning_client import LNDLightningClient
from squeaknode.common.squeak_maker import SqueakMaker
from squeaknode.server.postgres_db import PostgresDb


logger = logging.getLogger(__name__)


class SqueakServerHandler(object):
    """Handles server commands.
    """

    def __init__(
            self,
            lightning_client: LNDLightningClient,
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
        ## Todo: return the squeak from the db.
        return squeak.GetHash()

    def handle_get_squeak(self, squeak_hash):
        logger.info("Handler get squeak by hash: " + str(squeak_hash))

        squeak = self.postgres_db.get_squeak(squeak_hash)
        logger.info("Got squeak from db: " + str(squeak))
        return squeak


# class ClientNodeError(Exception):
#     pass


# class MissingSigningKeyError(ClientNodeError):
#     def __str__(self):
#         return 'Missing signing key.'

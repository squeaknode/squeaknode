import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.server.postgres_db import PostgresDb


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

    def handle_posted_squeak(self, squeak):
        logger.info("Handler got posted squeak: " + str(squeak))
        # Insert the squeak in the database
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        logger.info("Inserted squeak and got back hash: " + str(inserted_squeak_hash))
        ## Todo: return the squeak from the db.
        return inserted_squeak_hash

    def handle_get_squeak(self, squeak_hash):
        logger.info("Handler get squeak by hash: " + str(squeak_hash))
        squeak = self.postgres_db.get_squeak(squeak_hash)
        logger.info("Got squeak from db: " + str(squeak))
        return squeak

    def handle_lookup_squeaks(self, addresses, min_block, max_block):
        logger.info("Handler lookup squeaks with addresses: " + str(addresses))
        hashes = self.postgres_db.lookup_squeaks(addresses, min_block, max_block)
        logger.info("Got hashes from db: " + str(hashes))
        return hashes

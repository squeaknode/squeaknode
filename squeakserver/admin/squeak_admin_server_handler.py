import logging
import threading

from squeak.core.encryption import generate_initialization_vector
from squeak.core.encryption import CEncryptedDecryptionKey
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeakserver.server.buy_offer import BuyOffer
from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.server.lightning_address import LightningAddressHostPort
from squeakserver.server.postgres_db import PostgresDb
from squeakserver.server.util import generate_offer_preimage
from squeakserver.server.util import bxor
from squeakserver.server.util import get_hash


logger = logging.getLogger(__name__)


class SqueakAdminServerHandler(object):
    """Handles admin server commands.
    """

    def __init__(
            self,
            lightning_client: LNDLightningClient,
            postgres_db: PostgresDb,
    ) -> None:
        self.lightning_client = lightning_client
        self.postgres_db = postgres_db

    def handle_get_balance(self):
        logger.info("Handle get balance: {}")
        wallet_balance = self.lightning_client.get_wallet_balance()
        return wallet_balance

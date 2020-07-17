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

from squeakserver.server.squeak_profile import SqueakProfile


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
        logger.info("Handle get balance")
        wallet_balance = self.lightning_client.get_wallet_balance()
        logger.info("Wallet balance: {}".format(wallet_balance))
        return wallet_balance.total_balance

    def handle_create_signing_profile(self, profile_name):
        logger.info("Handle create signing profile with name: {}".format(profile_name))
        signing_key = CSigningKey.generate()
        verifying_key = signing_key.get_verifying_key()
        address = CSqueakAddress.from_verifying_key(verifying_key)
        squeak_profile = SqueakProfile(
            profile_id=None,
            profile_name=profile_name,
            private_key=bytes(signing_key),
            address=str(address),
            sharing=False,
            following=False,
        )
        profile_id = self.postgres_db.insert_profile(squeak_profile)
        logger.info("New profile_id: {}".format(profile_id))
        return profile_id

    def handle_get_squeak_profile(self, profile_id):
        logger.info("Handle get squeak profile with id: {}".format(profile_id))
        squeak_profile = self.postgres_db.get_profile(profile_id)
        return squeak_profile

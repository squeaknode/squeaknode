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

from squeakserver.node.squeak_maker import SqueakMaker


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
        logger.info("Created new signing key: {}".format(signing_key))
        verifying_key = signing_key.get_verifying_key()
        address = CSqueakAddress.from_verifying_key(verifying_key)
        signing_key_str = str(signing_key)
        signing_key_bytes = signing_key_str.encode()
        squeak_profile = SqueakProfile(
            profile_id=None,
            profile_name=profile_name,
            private_key=signing_key_bytes,
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

    def handle_make_squeak(self, profile_id, content_str, replyto_hash):
        logger.info("Handle make squeak profile with id: {}".format(profile_id))
        squeak_profile = self.postgres_db.get_profile(profile_id)
        squeak_maker = SqueakMaker(self.lightning_client)
        squeak = squeak_maker.make_squeak(squeak_profile, content_str, replyto_hash)
        inserted_squeak_hash = self.postgres_db.insert_squeak(squeak)
        return inserted_squeak_hash

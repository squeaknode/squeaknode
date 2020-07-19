import logging

from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.node.squeak_node import SqueakNode

logger = logging.getLogger(__name__)


class SqueakAdminServerHandler(object):
    """Handles admin server commands.
    """

    def __init__(
        self, lightning_client: LNDLightningClient, squeak_node: SqueakNode,
    ):
        self.lightning_client = lightning_client
        self.squeak_node = squeak_node

    def handle_get_balance(self):
        logger.info("Handle get balance")
        wallet_balance = self.lightning_client.get_wallet_balance()
        return wallet_balance

    def handle_create_signing_profile(self, profile_name):
        logger.info("Handle create signing profile with name: {}".format(profile_name))
        profile_id = self.squeak_node.create_signing_profile(profile_name)
        logger.info("New profile_id: {}".format(profile_id))
        return profile_id

    def handle_get_squeak_profile(self, profile_id):
        logger.info("Handle get squeak profile with id: {}".format(profile_id))
        squeak_profile = self.squeak_node.get_squeak_profile(profile_id)
        return squeak_profile

    def handle_make_squeak(self, profile_id, content_str, replyto_hash):
        logger.info("Handle make squeak profile with id: {}".format(profile_id))
        inserted_squeak_hash = self.squeak_node.make_squeak(
            profile_id, content_str, replyto_hash
        )
        return inserted_squeak_hash

    def handle_get_squeak_display_entry(self, squeak_hash):
        logger.info("Handle get squeak display entry for hash: {}".format(squeak_hash))
        squeak_entry_with_profile = self.squeak_node.get_squeak_entry_with_profile(
            squeak_hash
        )
        logger.info("Got squeak entry with profile for hash: {}".format(squeak_entry_with_profile))
        return squeak_entry_with_profile

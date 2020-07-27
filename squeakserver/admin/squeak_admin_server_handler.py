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

    def handle_lnd_get_info(self):
        logger.info("Handle lnd get info")
        return self.lightning_client.get_info()

    def handle_lnd_wallet_balance(self):
        logger.info("Handle lnd wallet balance")
        return self.lightning_client.get_wallet_balance()

    def handle_create_signing_profile(self, profile_name):
        logger.info("Handle create signing profile with name: {}".format(profile_name))
        profile_id = self.squeak_node.create_signing_profile(profile_name)
        logger.info("New profile_id: {}".format(profile_id))
        return profile_id

    def handle_create_contact_profile(self, profile_name, squeak_address):
        logger.info("Handle create contact profile with name: {}, address: {}".format(profile_name, squeak_address))
        profile_id = self.squeak_node.create_contact_profile(profile_name, squeak_address)
        logger.info("New profile_id: {}".format(profile_id))
        return profile_id

    def handle_get_signing_profiles(self):
        logger.info("Handle get signing profiles.")
        profiles = self.squeak_node.get_signing_profiles()
        logger.info("Got number of profiles: {}".format(len(profiles)))
        return profiles

    def handle_get_contact_profiles(self):
        logger.info("Handle get contact profiles.")
        profiles = self.squeak_node.get_contact_profiles()
        logger.info("Got number of profiles: {}".format(len(profiles)))
        return profiles

    def handle_get_squeak_profile(self, profile_id):
        logger.info("Handle get squeak profile with id: {}".format(profile_id))
        squeak_profile = self.squeak_node.get_squeak_profile(profile_id)
        return squeak_profile

    def handle_get_squeak_profile_by_address(self, address):
        logger.info("Handle get squeak profile with address: {}".format(address))
        squeak_profile = self.squeak_node.get_squeak_profile_by_address(address)
        logger.info("Got squeak profile by address: {}".format(squeak_profile))
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
        logger.info(
            "Got squeak entry with profile for hash: {}".format(
                squeak_entry_with_profile
            )
        )
        return squeak_entry_with_profile

    def handle_get_followed_squeak_display_entries(self):
        logger.info("Handle get followed squeak display entries.")
        squeak_entries_with_profile = self.squeak_node.get_followed_squeak_entries_with_profile()
        logger.info(
            "Got squeak entries with profile: {}".format(
                squeak_entries_with_profile
            )
        )
        return squeak_entries_with_profile

    def handle_get_squeak_display_entries_for_address(self, address, min_block, max_block):
        logger.info("Handle get squeak display entries for address: {}".format(address))
        squeak_entries_with_profile = self.squeak_node.get_squeak_entries_with_profile_for_address(
            address,
            min_block,
            max_block,
        )
        return squeak_entries_with_profile

    def handle_get_ancestor_squeak_display_entries(self, squeak_hash_str):
        logger.info("Handle get ancestor squeak display entries for squeak hash: {}".format(squeak_hash_str))
        squeak_entries_with_profile = self.squeak_node.get_ancestor_squeak_entries_with_profile(
            squeak_hash_str,
        )
        logger.info("Got number of ancestor squeak entries: {}".format(len(squeak_entries_with_profile)))
        logger.info("Got ancestor squeak display entries:")
        for entry in squeak_entries_with_profile:
            logger.info("Entry: {}".format(entry))
        return squeak_entries_with_profile

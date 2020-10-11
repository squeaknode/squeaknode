import logging

from squeakserver.common.lnd_lightning_client import LNDLightningClient
from squeakserver.node.squeak_node import SqueakNode

logger = logging.getLogger(__name__)


class SqueakAdminServerHandler(object):
    """Handles admin server commands."""

    def __init__(
        self,
        lightning_client: LNDLightningClient,
        squeak_node: SqueakNode,
    ):
        self.lightning_client = lightning_client
        self.squeak_node = squeak_node

    def handle_lnd_get_info(self):
        logger.info("Handle lnd get info")
        return self.lightning_client.get_info()

    def handle_lnd_wallet_balance(self):
        logger.info("Handle lnd wallet balance")
        return self.lightning_client.get_wallet_balance()

    def handle_lnd_new_address(self, address_type):
        logger.info("Handle lnd new address with type: {}".format(address_type))
        return self.lightning_client.new_address(address_type)

    def handle_lnd_list_channels(self):
        logger.info("Handle lnd list channels")
        return self.lightning_client.list_channels()

    def handle_lnd_pending_channels(self):
        logger.info("Handle lnd pending channels")
        return self.lightning_client.pending_channels()

    def handle_lnd_get_transactions(self):
        logger.info("Handle lnd get transactions")
        return self.lightning_client.get_transactions()

    def handle_lnd_list_peers(self):
        logger.info("Handle list peers")
        return self.lightning_client.list_peers()

    def handle_lnd_connect_peer(self, lightning_address):
        logger.info("Handle connect peer with address: {}".format(lightning_address))
        pubkey = lightning_address.pubkey
        host = lightning_address.host
        return self.lightning_client.connect_peer(pubkey, host)

    def handle_lnd_disconnect_peer(self, pubkey):
        logger.info("Handle disconnect peer with pubkey: {}".format(pubkey))
        return self.lightning_client.disconnect_peer(pubkey)

    def handle_lnd_open_channel_sync(self, node_pubkey_string, local_funding_amount, sat_per_byte):
        logger.info("Handle open channel to peer with pubkey: {}, amount: {}".format(
            node_pubkey_string,
            local_funding_amount,
        ))
        return self.lightning_client.open_channel_sync(
            node_pubkey_string,
            local_funding_amount,
        )

    def handle_lnd_close_channel(self, channel_point, sat_per_byte):
        logger.info("Handle close channel with channel_point: {}".format(
            channel_point,
            sat_per_byte,
        ))
        return self.lightning_client.close_channel(
            channel_point,
        )

    def handle_create_signing_profile(self, profile_name):
        logger.info("Handle create signing profile with name: {}".format(profile_name))
        profile_id = self.squeak_node.create_signing_profile(profile_name)
        logger.info("New profile_id: {}".format(profile_id))
        return profile_id

    def handle_create_contact_profile(self, profile_name, squeak_address):
        logger.info(
            "Handle create contact profile with name: {}, address: {}".format(
                profile_name, squeak_address
            )
        )
        profile_id = self.squeak_node.create_contact_profile(
            profile_name, squeak_address
        )
        logger.info("New profile_id: {}".format(profile_id))
        return profile_id

    def handle_get_signing_profiles(self):
        logger.info("Handle get signing profiles.")
        profiles = self.squeak_node.get_signing_profiles()
        logger.info("Got number of signing profiles: {}".format(len(profiles)))
        return profiles

    def handle_get_contact_profiles(self):
        logger.info("Handle get contact profiles.")
        profiles = self.squeak_node.get_contact_profiles()
        logger.info("Got number of contact profiles: {}".format(len(profiles)))
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

    def handle_set_squeak_profile_whitelisted(self, profile_id, whitelisted):
        logger.info(
            "Handle set squeak profile whitelisted with profile id: {}, whitelisted: {}".format(
                profile_id,
                whitelisted,
            )
        )
        self.squeak_node.set_squeak_profile_whitelisted(profile_id, whitelisted)

    def handle_set_squeak_profile_following(self, profile_id, following):
        logger.info(
            "Handle set squeak profile following with profile id: {}, following: {}".format(
                profile_id,
                following,
            )
        )
        self.squeak_node.set_squeak_profile_following(profile_id, following)

    def handle_set_squeak_profile_sharing(self, profile_id, sharing):
        logger.info(
            "Handle set squeak profile sharing with profile id: {}, sharing: {}".format(
                profile_id,
                sharing,
            )
        )
        self.squeak_node.set_squeak_profile_sharing(profile_id, sharing)

    def handle_delete_squeak_profile(self, profile_id):
        logger.info("Handle delete squeak profile with id: {}".format(profile_id))
        self.squeak_node.delete_squeak_profile(profile_id)

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
        squeak_entries_with_profile = (
            self.squeak_node.get_followed_squeak_entries_with_profile()
        )
        logger.info(
            "Got number of followed squeak entries: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        return squeak_entries_with_profile

    def handle_get_squeak_display_entries_for_address(
        self, address, min_block, max_block
    ):
        logger.info("Handle get squeak display entries for address: {}".format(address))
        squeak_entries_with_profile = (
            self.squeak_node.get_squeak_entries_with_profile_for_address(
                address,
                min_block,
                max_block,
            )
        )
        logger.info(
            "Got number of squeak entries for address: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        return squeak_entries_with_profile

    def handle_get_ancestor_squeak_display_entries(self, squeak_hash_str):
        logger.info(
            "Handle get ancestor squeak display entries for squeak hash: {}".format(
                squeak_hash_str
            )
        )
        squeak_entries_with_profile = (
            self.squeak_node.get_ancestor_squeak_entries_with_profile(
                squeak_hash_str,
            )
        )
        logger.info(
            "Got number of ancestor squeak entries: {}".format(
                len(squeak_entries_with_profile)
            )
        )
        return squeak_entries_with_profile

    def handle_delete_squeak(self, squeak_hash):
        logger.info("Handle delete squeak with hash: {}".format(squeak_hash))
        self.squeak_node.delete_squeak(squeak_hash)
        logger.info("Deleted squeak entry with hash: {}".format(squeak_hash))

    def handle_create_peer(self, peer_name, host, port):
        logger.info(
            "Handle create peer with name: {}, host: {}, port: {}".format(
                peer_name,
                host,
                port,
            )
        )
        peer_id = self.squeak_node.create_peer(
            peer_name,
            host,
            port,
        )
        return peer_id

    def handle_get_squeak_peer(self, peer_id):
        logger.info("Handle get squeak peer with id: {}".format(peer_id))
        squeak_peer = self.squeak_node.get_peer(peer_id)
        return squeak_peer

    def handle_get_squeak_peers(self):
        logger.info("Handle get squeak peers")
        squeak_peers = self.squeak_node.get_peers()
        return squeak_peers

    def handle_set_squeak_peer_downloading(self, peer_id, downloading):
        logger.info(
            "Handle set peer downloading with peer id: {}, downloading: {}".format(
                peer_id,
                downloading,
            )
        )
        self.squeak_node.set_peer_downloading(peer_id, downloading)

    def handle_set_squeak_peer_uploading(self, peer_id, uploading):
        logger.info(
            "Handle set peer uploading with peer id: {}, uploading: {}".format(
                peer_id,
                uploading,
            )
        )
        self.squeak_node.set_peer_uploading(peer_id, uploading)

    def handle_delete_squeak_peer(self, peer_id):
        logger.info("Handle delete squeak peer with id: {}".format(peer_id))
        self.squeak_node.delete_peer(peer_id)

    def handle_get_buy_offers(self, squeak_hash_str):
        logger.info("Handle get buy offers for hash: {}".format(squeak_hash_str))
        return self.squeak_node.get_buy_offers_with_peer(squeak_hash_str)

    def handle_get_buy_offer(self, offer_id):
        logger.info("Handle get buy offer for hash: {}".format(offer_id))
        return self.squeak_node.get_buy_offer_with_peer(offer_id)

import logging
from contextlib import contextmanager
from typing import Optional

from squeaknode.core.block_range import BlockRange
from squeaknode.core.received_offer_with_peer import ReceivedOfferWithPeer
from squeaknode.network.peer_client import PeerClient
from squeaknode.node.squeak_controller import SqueakController

logger = logging.getLogger(__name__)


class PeerConnection:

    def __init__(
        self,
        squeak_controller: SqueakController,
        peer,
        timeout_s,
    ):
        self.squeak_controller = squeak_controller
        self.peer = peer
        self.timeout_s = timeout_s
        self.peer_client = PeerClient(
            self.peer.host,
            self.peer.port,
            self.timeout_s,
        )

    @contextmanager
    def open_connection(self):
        with self.peer_client.open_stub():
            yield self

    def download(
        self,
        block_range: BlockRange = None,
    ):
        # Get the network
        network = self.squeak_controller.get_network()
        # Get the block range
        if block_range is None:
            block_range = self.squeak_controller.get_block_range()
        # Get list of followed addresses
        followed_addresses = self.squeak_controller.get_followed_addresses()
        # Get remote hashes
        lookup_result = self.peer_client.lookup_squeaks_to_download(
            network,
            followed_addresses,
            block_range.min_block,
            block_range.max_block,
        )
        remote_hashes = lookup_result.hashes
        # Get local hashes of saved squeaks
        local_hashes = self.squeak_controller.lookup_squeaks_include_locked(
            followed_addresses,
            block_range.min_block,
            block_range.max_block,
        )
        # Get hashes to download
        hashes_to_download = set(remote_hashes) - set(local_hashes)
        # Download squeaks for the hashes
        for hash in hashes_to_download:
            self._download_squeak(hash)

        # Get local hashes of locked squeaks that don't have an offer from this peer.
        locked_hashes = self.squeak_controller.lookup_squeaks_needing_offer(
            followed_addresses,
            block_range.min_block,
            block_range.max_block,
            self.peer.peer_id,
        )
        # Get hashes to get offer
        hashes_to_get_offer = set(remote_hashes) & set(locked_hashes)
        # Download offers for the hashes
        # TODO: catch exception downloading individual squeak
        for hash in hashes_to_get_offer:
            self._download_offer(hash)

    def upload(self):
        # Get the network
        network = self.squeak_controller.get_network()
        # Get list of sharing addresses.
        sharing_addresses = self.squeak_controller.get_sharing_addresses()
        # Get remote hashes
        lookup_result = self.peer_client.lookup_squeaks_to_upload(
            network,
            sharing_addresses,
        )
        remote_hashes = lookup_result.hashes
        remote_addresses = lookup_result.addresses
        min_block = lookup_result.min_block
        max_block = lookup_result.max_block
        # Get local hashes
        local_hashes = self.squeak_controller.lookup_squeaks(
            remote_addresses,
            min_block,
            max_block,
        )
        # Get hashes to upload
        hashes_to_upload = set(local_hashes) - set(remote_hashes)
        # Upload squeaks for the hashes
        # TODO: catch exception uploading individual squeak
        for hash in hashes_to_upload:
            self._upload_squeak(hash)

    def download_single_squeak(self, squeak_hash: bytes):
        """Downloads a single squeak and the corresponding offer. """
        saved_squeak = self.squeak_controller.get_squeak(squeak_hash)
        if not saved_squeak:
            self._force_download_squeak(squeak_hash)
        saved_offer = self._get_saved_offer(squeak_hash)
        if not saved_offer:
            self._download_offer(squeak_hash)

    def upload_single_squeak(self, squeak_hash: bytes):
        """Uploads a single squeak. """
        local_squeak = self.squeak_controller.get_squeak(squeak_hash)
        if local_squeak and local_squeak.HasDecryptionKey():
            self._upload_squeak(squeak_hash)

    def _get_saved_offer(self, squeak_hash: bytes) -> Optional[ReceivedOfferWithPeer]:
        offers = self.squeak_controller.get_buy_offers_with_peer(squeak_hash)
        for offer_with_peer in offers:
            if offer_with_peer.received_offer.peer_id == self.peer.peer_id:
                return offer_with_peer
        return None

    def _download_squeak(self, squeak_hash: bytes):
        squeak = self.peer_client.download_squeak(squeak_hash)
        self.squeak_controller.save_downloaded_squeak(
            squeak,
        )

    def _force_download_squeak(self, squeak_hash: bytes):
        squeak = self.peer_client.download_squeak(squeak_hash)
        self.squeak_controller.save_downloaded_squeak(
            squeak,
            skip_interested_check=True,
        )

    def _download_offer(self, squeak_hash: bytes):
        squeak = self.squeak_controller.get_squeak(squeak_hash)
        offer = self.peer_client.download_offer(squeak_hash)
        # buy_offer = parse_buy_offer(offer_msg)
        decoded_offer = self.squeak_controller.get_offer(
            squeak, offer, self.peer)
        self.squeak_controller.save_offer(decoded_offer)
        logger.info("Downloaded offer for squeak {} from peer {}".format(
            squeak_hash.hex(), self.peer
        ))

    def _upload_squeak(self, squeak_hash: bytes):
        squeak = self.squeak_controller.get_squeak(squeak_hash)
        self.peer_client.upload_squeak(squeak)
        logger.info("Uploaded squeak {} to peer {}".format(
            squeak_hash.hex(), self.peer
        ))

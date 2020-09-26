import logging

from squeakserver.node.squeak_node import SqueakNode
from squeakserver.server.util import get_hash

logger = logging.getLogger(__name__)


class SqueakServerHandler(object):
    """Handles server commands."""

    def __init__(self, squeak_node: SqueakNode):
        self.squeak_node = squeak_node

    def handle_posted_squeak(self, squeak):
        logger.info("Handle posted squeak with hash: {}".format(get_hash(squeak).hex()))
        # Save the squeak
        self.squeak_node.save_uploaded_squeak(squeak)

    def handle_get_squeak(self, squeak_hash):
        logger.info("Handle get squeak by hash: {}".format(squeak_hash.hex()))
        return self.squeak_node.get_public_squeak(squeak_hash)

    def handle_lookup_squeaks(self, addresses, min_block, max_block):
        logger.info(
            "Handle lookup squeaks with addresses: {}, min_block: {}, max_block: {}".format(
                str(addresses), min_block, max_block
            )
        )
        hashes = self.squeak_node.lookup_squeaks(addresses, min_block, max_block)
        logger.info("Got number of hashes from db: {}".format(len(hashes)))
        return hashes

    def handle_buy_squeak(self, squeak_hash, challenge):
        logger.info("Handle buy squeak by hash: {}".format(squeak_hash.hex()))
        buy_offer = self.squeak_node.get_buy_offer(squeak_hash, challenge)
        return buy_offer

import logging

from squeaknode.node.squeak_node import SqueakNode
from squeaknode.server.util import get_hash

from proto import squeak_server_pb2, squeak_server_pb2_grpc

logger = logging.getLogger(__name__)


class SqueakServerHandler(object):
    """Handles server commands."""

    def __init__(self, squeak_node: SqueakNode):
        self.squeak_node = squeak_node

    def handle_posted_squeak(self, squeak):
        logger.info("Handle posted squeak with hash: {}".format(get_hash(squeak)))
        # Save the squeak
        self.squeak_node.save_uploaded_squeak(squeak)

    def handle_get_squeak(self, squeak_hash):
        logger.info("Handle get squeak by hash: {}".format(squeak_hash))
        return self.squeak_node.get_public_squeak(squeak_hash)

    def handle_lookup_squeaks(self, request):
        addresses = request.addresses
        min_block = request.min_block
        max_block = request.max_block
        logger.info(
            "Handle lookup squeaks with addresses: {}, min_block: {}, max_block: {}".format(
                str(addresses), min_block, max_block
            )
        )
        hashes = self.squeak_node.lookup_squeaks(addresses, min_block, max_block)
        logger.info("Got number of hashes from db: {}".format(len(hashes)))
        allowed_addresses = self.squeak_node.lookup_allowed_addresses(addresses)
        logger.info("Got number of allowed addresses from db: {}".format(len(allowed_addresses)))
        return squeak_server_pb2.LookupSqueaksReply(
            hashes=hashes,
            allowed_addresses=allowed_addresses,
        )

    def handle_buy_squeak(self, squeak_hash, challenge, client_addr):
        logger.info("Handle buy squeak by hash: {} from client_addr: {}".format(squeak_hash, client_addr))
        buy_offer = self.squeak_node.get_buy_offer(squeak_hash, challenge, client_addr)
        return buy_offer

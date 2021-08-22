import logging
import threading

from squeak.core import CSqueak
from squeak.messages import msg_inv
from squeak.net import CInterested
from squeak.net import CInv

from squeaknode.core.util import get_hash
from squeaknode.network.network_manager import NetworkManager
from squeaknode.network.peer import Peer
from squeaknode.node.squeak_controller import SqueakController


logger = logging.getLogger(__name__)

DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_UPDATE_INTERVAL_S = 1

HASH_LENGTH = 32
EMPTY_HASH = b'\x00' * HASH_LENGTH


class NewSqueakWorker:

    def __init__(self,
                 squeak_controller: SqueakController,
                 network_manager: NetworkManager,
                 ):
        self.squeak_controller = squeak_controller
        self.network_manager = network_manager
        self.stopped = threading.Event()

    def start_running(self):
        threading.Thread(
            target=self.handle_new_squeaks,
            name="new_squeaks_worker_thread",
        ).start()

    def stop_running(self):
        self.stopped.set()

    def handle_new_squeaks(self):
        logger.info("Starting NewSqueakWorker...")
        for squeak in self.squeak_controller.subscribe_new_squeaks(
                self.stopped,
        ):
            logger.info("Handling new squeak: {!r}".format(
                get_hash(squeak).hex(),
            ))
            self.forward_squeak(squeak)

    def forward_squeak(self, squeak):
        logger.info("Forward new squeak: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if self.should_forward(squeak, peer):
                logger.info("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=1, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.info("Finished checking peers to forward.")

    def should_forward(self, squeak: CSqueak, peer: Peer) -> bool:
        logger.info("""
        Checking if should forward for peer: {}
        with subscription: {}
        and squeak: {}
        with squeak address: {}
        """.format(
            peer,
            peer.subscription,
            squeak,
            str(squeak.GetAddress()),
        ))
        if peer.subscription is None:
            return False
        locator = peer.subscription.locator
        for interest in locator.vInterested:
            if self.squeak_matches_interest(squeak, interest):
                logger.debug("Found a match!")
                return True
        return False

    def squeak_matches_interest(self, squeak: CSqueak, interest: CInterested) -> bool:
        if len(interest.addresses) > 0 \
           and squeak.GetAddress() not in interest.addresses:
            return False
        # if interest.nMinBlockHeight != -1 \
        #    and squeak.nBlockHeight < interest.nMinBlockHeight:
        #     return False
        # if interest.nMaxBlockHeight != -1 \
        #    and squeak.nBlockHeight > interest.nMaxBlockHeight:
        #     return False
        if interest.hashReplySqk != EMPTY_HASH \
           and squeak.hashReplySqk != interest.hashReplySqk:
            return False
        return True

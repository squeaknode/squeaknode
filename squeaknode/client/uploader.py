import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.client.squeak_store import SqueakStore
from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.squeak_maker import SqueakMaker
from squeaknode.client.db import SQLiteDBFactory
from squeaknode.client.hub_store import HubStore


logger = logging.getLogger(__name__)


class Uploader(object):
    """Uploads squeaks to the hubs.
    """

    def __init__(
            self,
            hub_store: HubStore,
            squeak_store: SqueakStore,
            address: CSqueakAddress,
            stopped: threading.Event,
    ) -> None:
        self.hub_store = hub_store
        self.squeak_store = squeak_store
        self.address = address
        self.stopped = stopped

    def upload_squeak(self, squeak):
        squeak_hash = squeak.GetHash()
        if self.squeak_store.is_squeak_uploaded(squeak_hash):
            # TODO: Upload squeak here.
            ##
            logger.info("Upload the squeak here.")
            self.squeak_store.mark_squeak_uploaded(squeak_hash)

    def upload_squeaks(self):
        for squeak in self.squeak_store.get_squeaks_to_upload(self.address):
            self.upload_squeak(squeak)

    def start(self):
        while True:
            try:
                self.upload_squeaks()
            except:
                self.stopped.set()

            # Check if client is stopped.
            is_stopped = self.stopped.wait(10)
            if is_stopped:
                break

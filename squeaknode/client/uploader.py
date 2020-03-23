import logging

from squeak.core.signing import CSigningKey

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
    ) -> None:
        self.hub_store = hub_store
        self.squeak_store = squeak_store

    def upload_squeak(self, squeak_hash):
        squeak = self.squeak_store.get_squeak(squeak_hash)
        # TODO: Upload squeak here.
        ##
        self.squeak_store.mark_squeak_uploaded(squeak_hash)

    def upload_squeaks(self):
        for squeak_hash in self.squeak_store.get_squeaks_to_upload():
            self.upload_squeak(squeak_hash)

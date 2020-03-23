import logging

from squeak.core.signing import CSigningKey

from squeaknode.client.squeak_store import SqueakStore
from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.squeak_maker import SqueakMaker
from squeaknode.client.db import SQLiteDBFactory
from squeaknode.client.uploader import Uploader


logger = logging.getLogger(__name__)


class SqueakNodeClient(object):
    """Network node that handles client commands.
    """

    def __init__(
            self,
            blockchain_client: BlockchainClient,
            lightning_client: LightningClient,
            signing_key: CSigningKey,
            db_factory: SQLiteDBFactory,
    ) -> None:
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client
        self.signing_key = signing_key
        self.squeak_store = SqueakStore(db_factory)
        self.hub_store = None
        self.uploader = Uploader(self.hub_store, self.squeak_store)

    def get_address(self):
        pass

    def make_squeak(self, content):
        if self.signing_key is None:
            logger.error('Missing signing key.')
            raise MissingSigningKeyError()
        squeak_maker = SqueakMaker(self.signing_key, self.blockchain_client)
        squeak = squeak_maker.make_squeak(content)
        logger.info('Made squeak: {}'.format(squeak))
        self.squeak_store.save_squeak(squeak)
        return squeak

    def get_squeak(self, squeak_hash):
        return self.squeak_store.get_squeak(squeak_hash)

    def listen_squeaks_changed(self, callback):
        self.squeaks_access.listen_squeaks_changed(callback)

    def add_follow(self, follow):
        pass

    def listen_follows_changed(self, callback):
        pass

    def get_wallet_balance(self):
        return self.lightning_client.get_wallet_balance()


class ClientNodeError(Exception):
    pass


class MissingSigningKeyError(ClientNodeError):
    def __str__(self):
        return 'Missing signing key.'

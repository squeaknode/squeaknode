import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress

from squeaknode.client.squeak_store import SqueakStore
from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.squeak_maker import SqueakMaker
from squeaknode.client.db import SQLiteDBFactory
from squeaknode.client.uploader import Uploader
from squeaknode.client.rpc_client import RPCClient


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
        self.address = CSqueakAddress.from_verifying_key(signing_key.get_verifying_key())
        self.squeak_store = SqueakStore(db_factory)
        self.hub_store = None

        # Event is set when the client stops
        self.stopped = threading.Event()
        self.uploader = Uploader(self.hub_store, self.squeak_store, self.address)
        self.rpc_client = RPCClient('sqkserver', 50051)

    def start(self):
        # TODO: start the uploader and the downloader.
        pass

    def stop(self):
        self.stopped.set()

    def get_address(self):
        return self.address

    def make_squeak(self, content):
        if self.signing_key is None:
            logger.error('Missing signing key.')
            raise MissingSigningKeyError()
        squeak_maker = SqueakMaker(self.signing_key, self.blockchain_client)
        squeak = squeak_maker.make_squeak(content)
        logger.info('Made squeak: {}'.format(squeak))
        self.squeak_store.save_squeak(squeak)
        self.rpc_client.upload_squeak(squeak)
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

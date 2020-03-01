import logging

from squeaknode.common.blockchain_client import BlockchainClient
from squeaknode.common.lightning_client import LightningClient
from squeaknode.common.squeak_maker import SqueakMaker


logger = logging.getLogger(__name__)


class SqueakNodeClient(object):
    """Network node that handles client commands.
    """

    def __init__(self, blockchain_client: BlockchainClient, lightning_client: LightningClient) -> None:
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client

    @property
    def address(self):
        return (self.peer_server.ip, self.peer_server.port)

    @property
    def signing_key(self):
        pass

    def get_address(self):
        pass

    def generate_signing_key(self):
        pass

    def make_squeak(self, content):
        key = self.get_signing_key()
        if key is None:
            logger.error('Missing signing key.')
            raise MissingSigningKeyError()
        else:
            squeak_maker = SqueakMaker(key, self.blockchain)
            squeak = squeak_maker.make_squeak(content)
            logger.info('Made squeak: {}'.format(squeak))
            self.add_squeak(squeak)
            return squeak

    def add_squeak(self, squeak):
        self.squeaks_access.add_squeak(squeak)

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

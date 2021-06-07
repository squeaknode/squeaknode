import logging
import threading

from squeak.core.signing import CSigningKey
from squeak.core.signing import CSqueakAddress
from squeak.net import CInterested
from squeak.net import CSqueakLocator
from squeakclient.squeaknode.core.stores.storage import Storage


logger = logging.getLogger(__name__)


class SigningKeyAccess(object):

    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.key_lock = threading.Lock()
        self.key_changed_callback = None

    def get_signing_key(self):
        return self.storage.get_key_store().get_signing_key()

    def get_address(self):
        key = self.get_signing_key()
        return self.address_from_signing_key(key)

    def set_signing_key(self, signing_key):
        with self.key_lock:
            self.storage.get_key_store().set_signing_key(signing_key)
            self.on_key_changed()

    def generate_signing_key(self):
        signing_key = CSigningKey.generate()
        self.set_signing_key(signing_key)
        verifying_key = signing_key.get_verifying_key()
        address = CSqueakAddress.from_verifying_key(verifying_key)
        logger.info('Returning generated address: {}'.format(str(address)))
        return address

    def on_key_changed(self):
        if self.key_changed_callback:
            address = self.get_address()
            logger.info('New address: {}'.format(address))
            self.key_changed_callback(address)

    def listen_key_changed(self, callback):
        self.key_changed_callback = callback

    def address_from_signing_key(self, key):
        verifying_key = key.get_verifying_key()
        return CSqueakAddress.from_verifying_key(verifying_key)


class FollowsAccess(object):

    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.follows_changed_callback = None

    def add_follow(self, follow):
        self.storage.get_follow_store().add_follow(follow)
        self.on_follows_changed()

    def on_follows_changed(self):
        logger.info('Number of follows {}'.format(
            len(self.storage.get_follow_store().get_follows())))
        if self.follows_changed_callback:
            follows = self.storage.get_follow_store().get_follows()
            self.follows_changed_callback(follows)

    def listen_follows_changed(self, callback):
        self.follows_changed_callback = callback

    def get_follows(self):
        """Get the squeak locator message to locate squeaks from other peers."""
        return self.storage.get_follow_store().get_follows()

    def get_follow_locator(self):
        follows = self.storage.get_follow_store().get_follows()
        interesteds = [CInterested(address=follow)
                       for follow in follows]
        return CSqueakLocator(vInterested=interesteds)


class SqueaksAccess(object):

    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.squeaks_lock = threading.Lock()
        self.squeaks_changed_callback = None

    def get_squeak(self, squeak_hash):
        return self.storage.get_squeak_store().get_squeak(squeak_hash)

    def add_squeak(self, squeak):
        with self.squeaks_lock:
            self.storage.get_squeak_store().add_squeak(squeak)
            self.on_squeaks_changed()

    def on_squeaks_changed(self):
        if self.squeaks_changed_callback:
            squeaks = self.storage.get_squeak_store().get_squeaks()
            self.squeaks_changed_callback(squeaks)

    def listen_squeaks_changed(self, callback):
        self.squeaks_changed_callback = callback

    def get_squeaks_by_locator(self, locator):
        with self.squeaks_lock:
            return self.storage.get_squeak_store().get_squeaks_by_locator(locator)

    def get_squeak_hashes(self):
        return self.storage.get_squeak_store().get_hashes()

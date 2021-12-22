# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
from typing import List
from typing import Optional

from squeak.core import CSqueak
from squeak.core.signing import SqueakPublicKey
from squeak.messages import msg_getdata
from squeak.messages import msg_inv
from squeak.messages import MSG_SECRET_KEY
from squeak.messages import MSG_SQUEAK
from squeak.messages import MsgSerializable
from squeak.net import CInterested
from squeak.net import CInv
from squeak.net import CSqueakLocator

from squeaknode.core.block_range import BlockRange
from squeaknode.core.connected_peer import ConnectedPeer
from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.offer import Offer
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.squeaks import get_hash
from squeaknode.node.active_download_manager import ActiveDownload
from squeaknode.node.downloaded_object import DownloadedOffer
from squeaknode.node.downloaded_object import DownloadedSqueak
from squeaknode.node.node_settings import NodeSettings
from squeaknode.node.secret_key_reply import OfferReply
from squeaknode.node.secret_key_reply import SecretKeyReply
from squeaknode.node.squeak_store import SqueakStore


logger = logging.getLogger(__name__)


class NetworkHandler:

    def __init__(
        self,
        squeak_store: SqueakStore,
        node_settings: NodeSettings,
        network_manager,
        download_manager,
        config,
    ):
        self.squeak_store = squeak_store
        self.node_settings = node_settings
        self.network_manager = network_manager
        self.active_download_manager = download_manager
        self.config = config

    def save_squeak(self, squeak: CSqueak) -> Optional[bytes]:
        return self.squeak_store.save_squeak(squeak)

    def unlock_squeak(self, squeak_hash: bytes, secret_key: bytes):
        self.squeak_store.unlock_squeak(squeak_hash, secret_key)

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        return self.squeak_store.get_squeak(squeak_hash)

    def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
        return self.squeak_store.get_squeak_secret_key(squeak_hash)

    def squeak_in_limit_of_interest(self, squeak: CSqueak, interest: CInterested) -> bool:
        # return self.squeak_db.number_of_squeaks_with_public_key_in_block_range(
        #     squeak.GetPubKey(),
        #     interest.nMinBlockHeight,
        #     interest.nMaxBlockHeight,
        # ) < self.config.node.max_squeaks_per_address_in_block_range
        return self.squeak_store.squeak_in_limit_of_interest(squeak, interest)

    def get_download_squeak_counter(self, squeak: CSqueak) -> Optional[ActiveDownload]:
        downloaded_squeak = DownloadedSqueak(squeak)
        return self.active_download_manager.lookup_counter(downloaded_squeak)

    def get_download_offer_counter(self, offer: Offer) -> Optional[ActiveDownload]:
        downloaded_offer = DownloadedOffer(offer)
        return self.active_download_manager.lookup_counter(downloaded_offer)

    def get_secret_key_reply(
            self,
            squeak_hash: bytes,
            peer_address: PeerAddress,
            price_msat: int,
            lnd_external_address: Optional[LightningAddressHostPort],
    ) -> Optional[SecretKeyReply]:
        # squeak = self.get_squeak(squeak_hash)
        # if squeak is None:
        #     return None
        # price = self.get_price_for_squeak(squeak, peer_address)
        # if price == 0:
        #     return self.get_free_squeak_secret_key_reply(squeak_hash)
        # else:
        #     return self.get_offer_reply(
        #         squeak=squeak,
        #         peer_address=peer_address,
        #         price_msat=price,
        #     )
        return self.squeak_store.get_secret_key_reply(
            squeak_hash,
            peer_address,
            price_msat,
            lnd_external_address,
        )

    def get_offer_reply(
            self,
            squeak: CSqueak,
            peer_address: PeerAddress,
            price_msat: int,
            lnd_external_address: Optional[LightningAddressHostPort],
    ) -> Optional[OfferReply]:
        # sent_offer = self.get_sent_offer_for_peer(
        #     squeak,
        #     peer_address,
        #     price_msat,
        # )
        # if sent_offer is None:
        #     return None
        # lnd_external_address: Optional[LightningAddressHostPort] = None
        # if self.config.lnd.external_host:
        #     lnd_external_address = LightningAddressHostPort(
        #         host=self.config.lnd.external_host,
        #         port=self.config.lnd.port,
        #     )
        # try:
        #     offer = self.squeak_core.package_offer(
        #         sent_offer,
        #         lnd_external_address,
        #     )
        #     return OfferReply(
        #         squeak_hash=get_hash(squeak),
        #         offer=offer,
        #     )
        # except Exception:
        #     return None
        return self.squeak_store.get_offer_reply(
            squeak,
            peer_address,
            price_msat,
            lnd_external_address,
        )

    # def get_sent_offer_for_peer(self, squeak: CSqueak, peer_address: PeerAddress, price_msat: int) -> Optional[SentOffer]:
    #     squeak_hash = get_hash(squeak)
    #     # Check if there is an existing offer for the hash/peer_address combination
    #     sent_offer = self.squeak_db.get_sent_offer_by_squeak_hash_and_peer(
    #         squeak_hash,
    #         peer_address,
    #     )
    #     if sent_offer:
    #         return sent_offer
    #     secret_key = self.get_squeak_secret_key(squeak_hash)
    #     if squeak is None or secret_key is None:
    #         return None
    #     try:
    #         sent_offer = self.squeak_core.create_offer(
    #             squeak,
    #             secret_key,
    #             peer_address,
    #             price_msat,
    #         )
    #     except Exception:
    #         logger.exception("Failed to create offer.")
    #         return None
    #     self.squeak_db.insert_sent_offer(sent_offer)
    #     return sent_offer

    # def get_price_for_squeak(self, squeak: CSqueak, peer_address: PeerAddress) -> int:
    #     price_policy = PricePolicy(self.squeak_db, self.config)
    #     return price_policy.get_price(squeak, peer_address)

    def get_block_range(self) -> BlockRange:
        # max_block = self.squeak_core.get_best_block_height()
        # block_interval = self.config.node.interest_block_interval
        # min_block = max(0, max_block - block_interval)
        # return BlockRange(min_block, max_block)
        return self.squeak_store.get_block_range()

    def save_received_offer(self, offer: Offer, peer_address: PeerAddress) -> Optional[int]:
        # squeak = self.get_squeak(offer.squeak_hash)
        # secret_key = self.get_squeak_secret_key(offer.squeak_hash)
        # if squeak is None or secret_key is not None:
        #     return None
        # try:
        #     # TODO: Call unpack_offer with check_payment_point=True.
        #     received_offer = self.squeak_core.unpack_offer(
        #         squeak,
        #         offer,
        #         peer_address,
        #     )
        # except Exception:
        #     logger.exception("Failed to save received offer.")
        #     return None
        # received_offer_id = self.squeak_db.insert_received_offer(
        #     received_offer)
        # if received_offer_id is None:
        #     return None
        # logger.info("Saved received offer: {}".format(received_offer))
        # received_offer = received_offer._replace(
        #     received_offer_id=received_offer_id)
        # self.new_received_offer_listener.handle_new_item(received_offer)
        # return received_offer_id
        return self.squeak_store.save_received_offer(offer, peer_address)

    def get_followed_public_keys(self) -> List[SqueakPublicKey]:
        # followed_profiles = self.squeak_db.get_following_profiles()
        # return [profile.public_key for profile in followed_profiles]
        return self.squeak_store.get_followed_public_keys()

    def connect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Connect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.connect_peer_sync(peer_address)

    def get_connected_peer(self, peer_address: PeerAddress) -> Optional[ConnectedPeer]:
        peer = self.network_manager.get_connected_peer(peer_address)
        if peer is None:
            return None
        return ConnectedPeer(
            peer=peer,
            # saved_peer=self.squeak_db.get_peer_by_address(
            #     peer_address,
            # ),
            saved_peer=self.squeak_store.get_peer_by_address(
                peer_address,
            ),
        )

    def get_connected_peers(self) -> List[ConnectedPeer]:
        peers = self.network_manager.get_connected_peers()
        return [
            ConnectedPeer(
                peer=peer,
                # saved_peer=self.squeak_db.get_peer_by_address(
                #     peer.remote_address,
                # ),
                saved_peer=self.squeak_store.get_peer_by_address(
                    peer.remote_address,
                ),
            ) for peer in peers
        ]

    def lookup_squeaks(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: Optional[int],
            max_block: Optional[int],
            reply_to_hash: Optional[bytes],
    ) -> List[bytes]:
        # return self.squeak_db.lookup_squeaks(
        #     public_keys,
        #     min_block,
        #     max_block,
        #     reply_to_hash,
        #     include_locked=True,
        # )
        return self.squeak_store.lookup_squeaks(
            public_keys,
            min_block,
            max_block,
            reply_to_hash,
        )

    def lookup_secret_keys(
            self,
            public_keys: List[SqueakPublicKey],
            min_block: Optional[int],
            max_block: Optional[int],
            reply_to_hash: Optional[bytes],
    ) -> List[bytes]:
        # return self.squeak_db.lookup_squeaks(
        #     public_keys,
        #     min_block,
        #     max_block,
        #     reply_to_hash,
        # )
        return self.squeak_store.lookup_secret_keys(
            public_keys,
            min_block,
            max_block,
            reply_to_hash,
        )

    def get_interested_locator(self) -> CSqueakLocator:
        block_range = self.get_block_range()
        followed_public_keys = self.get_followed_public_keys()
        if len(followed_public_keys) == 0:
            return CSqueakLocator(
                vInterested=[],
            )
        interests = [
            CInterested(
                pubkeys=followed_public_keys,
                nMinBlockHeight=block_range.min_block,
                nMaxBlockHeight=block_range.max_block,
            )
        ]
        return CSqueakLocator(
            vInterested=interests,
        )

    def request_offers(self, squeak_hash: bytes):
        logger.info("Requesting offers for squeak: {}".format(
            squeak_hash.hex(),
        ))
        invs = [
            CInv(type=2, hash=squeak_hash)
        ]
        getdata_msg = msg_getdata(inv=invs)
        self.broadcast_msg(getdata_msg)

    def broadcast_msg(self, msg: MsgSerializable) -> int:
        return self.network_manager.broadcast_msg(msg)

    def disconnect_peer(self, peer_address: PeerAddress) -> None:
        logger.info("Disconnect to peer: {}".format(
            peer_address,
        ))
        self.network_manager.disconnect_peer(peer_address)

    def forward_squeak(self, squeak):
        logger.debug("Forward new squeak: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if peer.is_remote_subscribed(squeak):
                logger.debug("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=MSG_SQUEAK, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.debug("Finished checking peers to forward.")

    def forward_secret_key(self, squeak):
        logger.debug("Forward new secret key for hash: {!r}".format(
            get_hash(squeak).hex(),
        ))
        for peer in self.network_manager.get_connected_peers():
            if peer.is_remote_subscribed(squeak):
                logger.debug("Forwarding to peer: {}".format(
                    peer,
                ))
                squeak_hash = get_hash(squeak)
                inv = CInv(type=MSG_SECRET_KEY, hash=squeak_hash)
                inv_msg = msg_inv(inv=[inv])
                peer.send_msg(inv_msg)
        logger.debug("Finished checking peers to forward.")

    def get_default_sell_price_msat(self) -> int:
        return self.config.node.price_msat

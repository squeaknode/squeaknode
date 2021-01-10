import logging
import time
from typing import Optional

from squeak.core import CSqueak
from squeak.core import MakeSqueakFromStr
from squeak.core.signing import CSigningKey

from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.node.received_payments_subscription_client import (
    OpenReceivedPaymentsSubscriptionClient,
)

logger = logging.getLogger(__name__)


class SqueakCore:
    def __init__(
        self,
        blockchain_client,
        lightning_client,
    ):
        self.blockchain_client = blockchain_client
        self.lightning_client = lightning_client

    def make_squeak(self, signing_profile: SqueakProfile, content_str: str, replyto_hash: Optional[bytes] = None) -> SqueakEntry:
        if signing_profile.private_key is None:
            raise Exception("Can't make squeak with a contact profile.")
        signing_key_str = signing_profile.private_key.decode()
        signing_key = CSigningKey(signing_key_str)
        block_info = self.blockchain_client.get_best_block_info()
        block_height = block_info.block_height
        block_hash = block_info.block_hash
        timestamp = int(time.time())
        if replyto_hash is None or len(replyto_hash) == 0:
            squeak = MakeSqueakFromStr(
                signing_key,
                content_str,
                block_height,
                block_hash,
                timestamp,
            )
        else:
            squeak = MakeSqueakFromStr(
                signing_key,
                content_str,
                block_height,
                block_hash,
                timestamp,
                replyto_hash,
            )
        return SqueakEntry(
            squeak=squeak,
            block_header=block_info.block_header,
        )

    def validate_squeak(self, squeak: CSqueak) -> SqueakEntry:
        block_info = self.blockchain_client.get_block_info_by_height(
            squeak.nBlockHeight)
        if squeak.hashBlock != block_info.block_hash:
            raise Exception("Block hash incorrect.")
        return SqueakEntry(
            squeak=squeak,
            block_header=block_info.block_header,
        )

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
            address: CSqueakAddress,
    ) -> None:
        self.hub_store = hub_store
        self.signing_key = signing_key

    def get_squeaks_to_upload(self):
        if self.address is None:
            return None

        with self.db_factory.make_conn() as conn:
            squeak_rows = (
                conn
                .execute(
                    "SELECT s.hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, scriptPubKey, hashDataKey, vchIv, nTime, nNonce, encContent, scriptSig, vchDataKey"
                    " FROM squeak s"
                    " WHERE s. = ?",
                    (squeak_hash,),
                )
                .fetchall()
            )
            squeaks = []
            for squeak_row in squeak_rows:
                squeak = CSqueak(
                    nVersion=squeak_row['nVersion'],
                    hashEncContent=squeak_row['hashEncContent'],
                    hashReplySqk=squeak_row['hashReplySqk'],
                    hashBlock=squeak_row['hashBlock'],
                    nBlockHeight=squeak_row['nBlockHeight'],
                    scriptPubKey=CScript(squeak_row['scriptPubKey']),
                    hashDataKey=squeak_row['hashDataKey'],
                    vchIv=squeak_row['vchIv'],
                    nTime=squeak_row['nTime'],
                    nNonce=squeak_row['nNonce'],
                    encContent=CSqueakEncContent(squeak_row['encContent']),
                    scriptSig=CScript(squeak_row['scriptSig']),
                    vchDataKey=squeak_row['vchDataKey'],
                )
                CheckSqueak(squeak)
            return squeaks

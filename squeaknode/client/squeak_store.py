import logging

from squeak.core import CSqueak
from squeak.core import CheckSqueak
from squeak.core import HASH_LENGTH
from squeak.core import MakeSqueakFromStr
from squeak.core import CSqueakEncContent
from squeak.core.signing import CSigningKey
from squeak.core.signing import CSigningKey
from squeak.core.script import CScript

from squeaknode.client.db import get_db
from squeaknode.client.db import close_db
from squeaknode.client.db import initialize_db
from squeaknode.client.db import SQLiteDBFactory


logger = logging.getLogger(__name__)


class SqueakStore(object):
    """Network node that handles client commands.
    """

    def __init__(
            self,
            db_factory: SQLiteDBFactory,
    ) -> None:
        self.db_factory = db_factory

    def save_squeak(self, squeak):
        CheckSqueak(squeak)
        with self.db_factory.make_conn() as conn:
            conn.execute(
                "INSERT INTO squeak (hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, scriptPubKey, hashDataKey, vchIv, nTime, nNonce, encContent, scriptSig, address, vchDataKey, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    squeak.GetHash(),
                    squeak.nVersion,
                    squeak.hashEncContent,
                    squeak.hashReplySqk,
                    squeak.hashBlock,
                    squeak.nBlockHeight,
                    bytes(squeak.scriptPubKey),
                    squeak.hashDataKey,
                    squeak.vchIv,
                    squeak.nTime,
                    squeak.nNonce,
                    bytes(squeak.encContent.vchEncContent),
                    bytes(squeak.scriptSig),
                    str(squeak.GetAddress()),
                    squeak.vchDataKey,
                    "",
                ),
            )

    def get_squeak(self, squeak_hash):
        with self.db_factory.make_conn() as conn:
            squeak_row = (
                conn
                .execute(
                    "SELECT s.hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, scriptPubKey, hashDataKey, vchIv, nTime, nNonce, encContent, scriptSig, vchDataKey"
                    " FROM squeak s"
                    " WHERE s.hash = ?",
                    (squeak_hash,),
                )
                .fetchone()
            )
            if squeak_row is None:
                return None
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
            return squeak

    def delete_squeak(self):
        pass

    def unlock_squeak(self):
        pass

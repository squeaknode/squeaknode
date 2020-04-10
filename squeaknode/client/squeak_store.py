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

    def _row_to_squeak(self, squeak_row):
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
        try:
            CheckSqueak(squeak)
            return squeak
        except:
            return None

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
            return self._row_to_squeak(squeak_row)

    def delete_squeak(self):
        pass

    def unlock_squeak(self):
        pass

    def get_squeaks_to_upload(self, address, min_block=0):
        """Get all squeaks that need to be uploaded.
        """
        with self.db_factory.make_conn() as conn:
            squeak_row = (
                conn
                .execute(
                    "SELECT s.hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, scriptPubKey, hashDataKey, vchIv, nTime, nNonce, encContent, scriptSig, vchDataKey"
                    " FROM squeak s"
                    " WHERE s.address = ?",
                    (address,),
                )
                .fetchone()
            )
            if squeak_rows is None:
                return None
            squeaks = []
            for squeak_row in squeak_rows:
                squeak = self._row_to_squeak(squeak_row)
                squeaks.append(squeak)
            return squeaks

    def mark_squeak_uploaded(self, squeak_hash):
        """Mark the given squeak as one that needs to be uploaded.
        """
        with self.db_factory.make_conn() as conn:
            conn.execute(
                "INSERT INTO upload (squeakHash, complete) VALUES (?, ?)",
                (squeak_hash, 1),
            )

    def is_squeak_uploaded(self, squeak_hash):
        """True if the squeak has already been uploaded.
        """
        with self.db_factory.make_conn() as conn:
            upload_row = (
                conn
                .execute(
                    "SELECT u.squeakHash, complete"
                    " FROM upload u"
                    " WHERE u.squeakHash = ?",
                    (squeak_hash,),
                )
                .fetchone()
            )
            complete = upload_row['complete']
            return complete == 1

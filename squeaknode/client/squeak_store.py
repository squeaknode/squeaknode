import logging

from squeak.core.signing import CSigningKey

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
        title = squeak.GetHash()
        body = squeak.GetDecryptedContentStr()
        with self.db_factory.make_conn() as conn:
            conn.execute(
                "INSERT INTO post (title, body) VALUES (?, ?)",
                (title, body),
            )

    def get_squeak(self, squeak_hash):
        with self.db_factory.make_conn() as conn:
            post = (
                conn
                .execute(
                    "SELECT p.id, title, body, created"
                    " FROM post p"
                    " WHERE p.id = ?",
                    (squeak_hash,),
                )
                .fetchone()
            )
            return post

    def delete_squeak(self):
        pass

    def unlock_squeak(self):
        pass

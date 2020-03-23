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


class HubStore(object):
    """Network node that handles client commands.
    """

    def __init__(
            self,
            db_factory: SQLiteDBFactory,
    ) -> None:
        self.db_factory = db_factory

    def save_hub(self, hub):
        host, port = hub
        with self.db_factory.make_conn() as conn:
            conn.execute(
                "INSERT INTO hub (host, port) VALUES (?, ?)",
                (host, port),
            )

    def get_hubs(self):
        with self.db_factory.make_conn() as conn:
            hub_rows = (
                conn
                .execute(
                    "SELECT host, port"
                    " FROM hub h",
                )
                .fetchall()
            )
            hubs = []
            for hub_row in hub_rows:
                hubs.append(
                    hub_row['host'],
                    hub_row['port'],
                )
            return hubs

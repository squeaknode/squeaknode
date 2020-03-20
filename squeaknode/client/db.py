import sqlite3

from importlib_resources import files, as_file

def get_db():
    """Connect to the application's configured database.
    """
    db = sqlite3.connect(
        ":memory:",
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.row_factory = sqlite3.Row
    return db


def close_db(db):
    """Close the connection.
    """
    if db is not None:
        db.close()


def initialize_db(db):
    """Clear existing data and create new tables."""
    schema = files('squeaknode.client').joinpath('schema.sql').read_text()
    db.executescript(schema)


class SQLiteDB():

    def __init__(self, _file):
        self._file=_file

    def __enter__(self):
        self.conn = sqlite3.connect(
            self._file,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def initialize(self):
        initialize_db(self.conn)


class SQLiteDBFactory():

    def __init__(self, _file=":memory:"):
        self._file=_file

    def make_conn(self):
        return SQLiteDB(_file=self._file)

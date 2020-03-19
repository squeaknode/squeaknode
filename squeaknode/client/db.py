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
    print('schema:')
    print(schema)
    db.executescript(schema)

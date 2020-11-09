from alembic.config import Config
from alembic import command


def run_migrations(engine):
    """ Run migrations. """
    alembic_cfg = Config("alembic.ini")
    with engine.begin() as connection:
        alembic_cfg.attributes['connection'] = connection
        command.upgrade(alembic_cfg, "head")

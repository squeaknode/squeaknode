from alembic import command
from alembic.config import Config


def run_migrations(engine):
    """ Run migrations. """
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes["configure_logger"] = False
    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")

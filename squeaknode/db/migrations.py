import logging

from pkg_resources import resource_filename

from alembic import command
from alembic.config import Config


logger = logging.getLogger(__name__)


def run_migrations(engine):
    """ Run migrations. """
    alembic_conf_path = resource_filename(__name__, 'alembic.ini')
    alembic_cfg = Config(alembic_conf_path)
    alembic_cfg.attributes["configure_logger"] = False
    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")

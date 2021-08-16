from pathlib import Path

from sqlalchemy import create_engine


def get_engine(connection_string):
    return create_engine(connection_string)


def get_sqlite_connection_string(sqk_dir, network):
    data_dir = Path(sqk_dir).joinpath("data").joinpath(network)
    data_dir.mkdir(parents=True, exist_ok=True)
    return "sqlite:////{}/data.db".format(
        data_dir,
    )


def get_connection_string(config, network):
    if config.db.connection_string:
        return config.db.connection_string
    return get_sqlite_connection_string(
        config.core.sqk_dir_path,
        network,
    )

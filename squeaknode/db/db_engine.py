from sqlalchemy import create_engine


def get_engine(connection_string):
    return create_engine(connection_string)


def get_sqlite_connection_string(sqk_dir, network):
    data_dir = sqk_dir.joinpath("data").joinpath(network)
    data_dir.mkdir(parents=True, exist_ok=True)
    return "sqlite:////{}/data.db".format(
        data_dir,
    )

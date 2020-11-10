from sqlalchemy import create_engine


def get_engine(connection_string):
    return create_engine(connection_string)


# def get_postgres_engine(user, password, host, database):
#     return create_engine(get_postgres_connection_string(user, password, host, database))


# def get_postgres_connection_string(user, password, host, database):
#     return "postgresql://{}:{}@{}/{}".format(
#         user,
#         password,
#         host,
#         database,
#     )


# def get_sqlite_engine(data_dir):
#     return create_engine(get_sqlite_connection_string(data_dir))


# def get_data_dir(sqk_dir):
#     data_dir = sqk_dir.joinpath("data").joinpath(network)
#     data_dir.mkdir(parents=True, exist_ok=True)
#     return data_dir


def get_sqlite_connection_string(sqk_dir, network):
    data_dir = sqk_dir.joinpath("data").joinpath(network)
    data_dir.mkdir(parents=True, exist_ok=True)
    return "sqlite:////{}/data.db".format(
        data_dir,
    )

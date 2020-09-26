from sqlalchemy import create_engine


def get_postgres_engine(user, password, host, database):
    return create_engine(get_postgres_connection_string(user, password, host, database))


def get_postgres_connection_string(user, password, host, database):
    return "postgresql://{}:{}@{}/{}".format(
        user,
        password,
        host,
        database,
    )


def get_sqlite_engine(squeak_dir, network):
    return create_engine(get_sqlite_connection_string(squeak_dir, network))


def get_sqlite_connection_string(squeak_dir, network):
    return "sqlite:////{}/{}.db".format(
        squeak_dir,
        network,
    )

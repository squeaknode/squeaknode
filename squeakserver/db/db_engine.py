from sqlalchemy import create_engine


def get_postgres_engine(user, password, host, database):
    return create_engine(
        get_postgres_connection_string(
            user, password, host, database
        )
    )

def get_postgres_connection_string(user, password, host, database):
    return "postgresql://{}:{}@{}/{}".format(
        user,
        password,
        host,
        database,
    )

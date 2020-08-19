import logging

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy import func


logger = logging.getLogger(__name__)


def create_tables(engine, schema):
    logger.info("Calling create_tables")

    metadata = MetaData(schema=schema)

    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String),
                  Column('fullname', String),
    )

    addresses = Table('addresses', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', None, ForeignKey('users.id')),
                      Column('email_address', String, nullable=False)
    )

    peers = Table('peer', metadata,
                  Column('peer_id', Integer, primary_key=True),
                  Column('created', DateTime, server_default=func.now(), nullable=False),
                  Column('peer_name', String),
                  Column('server_host', String, nullable=False),
                  Column('server_port', Integer, nullable=False),
                  Column('uploading', Boolean, nullable=False),
                  Column('downloading', Boolean, nullable=False),
    )

    metadata.create_all(engine)
    logger.info("Called create_tables")

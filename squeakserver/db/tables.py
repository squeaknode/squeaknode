import logging

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, Binary, BigInteger, MetaData, ForeignKey
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

    squeaks = Table('squeak', metadata,
                  Column('hash', String(64), primary_key=True),
                  Column('created', DateTime, server_default=func.now(), nullable=False),
                  Column('n_version', Integer, nullable=False),
                  Column('hash_enc_content', String(64), nullable=False),
                  Column('hash_reply_sqk', String(64), nullable=False),
                  Column('hash_block', String(64), nullable=False),
                  Column('n_block_height', Integer, nullable=False),
                  Column('vch_script_pub_key', Binary, nullable=False),
                  Column('vch_encryption_key', Binary, nullable=False),
                  Column('enc_data_key', String, nullable=False),
                  Column('iv', String(64), nullable=False),
                  Column('n_time', Integer, nullable=False),
                  Column('n_nonce', BigInteger, nullable=False),
                  Column('enc_content', String(2272), nullable=False),
                  Column('vch_script_sig', Binary, nullable=False),
                  Column('author_address', String(35), index=True, nullable=False),
                  Column('vch_decryption_key', Binary, nullable=True),
                  Column('block_header', Binary, nullable=True),
    )

    profiles = Table('profile', metadata,
                  Column('profile_id', Integer, primary_key=True),
                  Column('created', DateTime, server_default=func.now(), nullable=False),
                  Column('profile_name', String, nullable=False),
                  Column('private_key', Binary),
                  Column('address', String(35), nullable=False),
                  Column('sharing', Boolean, nullable=False),
                  Column('following', Boolean, nullable=False),
                  Column('whitelisted', Boolean, nullable=False),
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

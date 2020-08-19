import logging
from contextlib import contextmanager

from psycopg2 import pool
from psycopg2 import sql
from psycopg2.extras import DictCursor
from squeak.core import CSqueak

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, Binary, BigInteger, MetaData, ForeignKey
from sqlalchemy import func
from sqlalchemy.sql import select

from squeakserver.blockchain.util import parse_block_header
from squeakserver.core.squeak_entry import SqueakEntry
from squeakserver.core.squeak_entry_with_profile import SqueakEntryWithProfile
from squeakserver.core.offer_with_peer import OfferWithPeer
from squeakserver.core.offer import Offer
from squeakserver.server.squeak_profile import SqueakProfile
from squeakserver.server.squeak_peer import SqueakPeer
from squeakserver.server.util import get_hash


logger = logging.getLogger(__name__)


class PostgresDb:
    def __init__(self, params, schema):
        logger.info("Starting connection pool with params: {}".format(params))
        self.schema = schema
        self.connection_pool = pool.ThreadedConnectionPool(5, 20, **params)
        self.db_string = self.get_connection_string(params)
        self.engine = create_engine(self.db_string)

        self.metadata = MetaData(schema=schema)

        self.users = Table('users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String),
                      Column('fullname', String),
        )

        self.addresses = Table('addresses', self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('user_id', None, ForeignKey('users.id')),
                          Column('email_address', String, nullable=False)
        )

        self.squeaks = Table('squeak', self.metadata,
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

        self.profiles = Table('profile', self.metadata,
                         Column('profile_id', Integer, primary_key=True),
                         Column('created', DateTime, server_default=func.now(), nullable=False),
                         Column('profile_name', String, nullable=False),
                         Column('private_key', Binary),
                         Column('address', String(35), nullable=False),
                         Column('sharing', Boolean, nullable=False),
                         Column('following', Boolean, nullable=False),
                         Column('whitelisted', Boolean, nullable=False),
        )

        self.peers = Table('peer', self.metadata,
                      Column('peer_id', Integer, primary_key=True),
                      Column('created', DateTime, server_default=func.now(), nullable=False),
                      Column('peer_name', String),
                      Column('server_host', String, nullable=False),
                      Column('server_port', Integer, nullable=False),
                      Column('uploading', Boolean, nullable=False),
                      Column('downloading', Boolean, nullable=False),
        )

        self.offers = Table('offer', self.metadata,
                       Column('offer_id', Integer, primary_key=True),
                       Column('created', DateTime, server_default=func.now(), nullable=False),
                       Column('squeak_hash', String(64), nullable=False),
                       Column('key_cipher', Binary, nullable=False),
                       Column('iv', Binary, nullable=False),
                       Column('payment_hash', String(64), nullable=False),
                       Column('invoice_timestamp', Integer, nullable=False),
                       Column('invoice_expiry', Integer, nullable=False),
                       Column('price_msat', Integer, nullable=False),
                       Column('payment_request', String, nullable=False),
                       Column('destination', String(66), nullable=False),
                       Column('node_host', String, nullable=False),
                       Column('node_port', Integer, nullable=False),
                       Column('peer_id', Integer, nullable=False),
        )

        self.sent_payments = Table('sent_payment', self.metadata,
                              Column('sent_payment_id', Integer, primary_key=True),
                              Column('created', DateTime, server_default=func.now(), nullable=False),
                              Column('offer_id', Integer, nullable=False),
                              Column('peer_id', Integer, nullable=False),
                              Column('squeak_hash', String(64), nullable=False),
                              Column('preimage_hash', String(64), nullable=False),
                              Column('preimage', String(64), nullable=False),
                              Column('amount', Integer, nullable=False),
                              Column('node_pubkey', String(66), nullable=False),
                              Column('preimage_is_valid', Boolean, nullable=False),
        )

    def create_tables(self):
        logger.info("Calling create_tables")
        self.metadata.create_all(self.engine)
        logger.info("Called create_tables")

    # Get Cursor
    @contextmanager
    def get_cursor(self):
        con = self.connection_pool.getconn()
        try:
            yield con.cursor(cursor_factory=DictCursor)
            con.commit()
        finally:
            self.connection_pool.putconn(con)

    def get_version(self):
        """ Connect to the PostgreSQL database server """
        with self.get_cursor() as curs:
            # execute a statement
            logger.info("PostgreSQL database version:")
            curs.execute("SELECT version()")

            # display the PostgreSQL database server version
            db_version = curs.fetchone()
            logger.info(db_version)

    def get_connection_string(self, params):
        return "postgresql://{}:{}@{}/{}".format(
            params['user'],
            params['password'],
            params['host'],
            params['database'],
        )

    def init(self):
        """ Create the tables and indices in the database. """

        logger.info("SqlAlchemy version: {}".format(sqlalchemy.__version__))

        logger.info("Creating tables...")
        # create_tables(self.engine, self.schema)
        self.create_tables()
        logger.info("Created tables.")

        # with self.get_cursor() as curs:
        #     # execute a statement
        #     logger.info("Setting up database tables...")
        #     curs.execute(open("init.sql", "r").read())

    def insert_squeak(self, squeak):
        """ Insert a new squeak. """
        sql = """
        INSERT INTO squeak(hash, n_version, hash_enc_content, hash_reply_sqk, hash_block, n_block_height, vch_script_pub_key, vch_encryption_key, enc_data_key, iv, n_time, n_nonce, enc_content, vch_script_sig, author_address, vch_decryption_key)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING hash;"""

        with self.get_cursor() as curs:
            # execute the INSERT statement
            curs.execute(
                sql,
                (
                    get_hash(squeak).hex(),
                    squeak.nVersion,
                    squeak.hashEncContent.hex(),
                    squeak.hashReplySqk.hex(),
                    squeak.hashBlock.hex(),
                    squeak.nBlockHeight,
                    squeak.vchScriptPubKey,
                    squeak.vchEncryptionKey,
                    squeak.encDatakey.hex(),
                    squeak.iv.hex(),
                    squeak.nTime,
                    squeak.nNonce,
                    squeak.encContent.hex(),
                    squeak.vchScriptSig,
                    str(squeak.GetAddress()),
                    squeak.GetDecryptionKey().get_bytes() if squeak.HasDecryptionKey() else None,
                ),
            )
            # get the generated hash back
            row = curs.fetchone()
            return bytes.fromhex(row["hash"])

    def get_squeak_entry(self, squeak_hash):
        """ Get a squeak. """
        sql = """
        SELECT * FROM squeak WHERE hash=%s"""

        squeak_hash_str = squeak_hash.hex()

        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash_str,))
            row = curs.fetchone()
            return self._parse_squeak_entry(row)

    def get_squeak_entry_with_profile(self, squeak_hash):
        """ Get a squeak. """
        sql = """
        SELECT * FROM squeak
        LEFT JOIN profile
        ON squeak.author_address=profile.address
        WHERE squeak.hash=%s
        """

        squeak_hash_str = squeak_hash.hex()

        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash_str,))
            row = curs.fetchone()
            return self._parse_squeak_entry_with_profile(row)

    def get_followed_squeak_entries_with_profile(self):
        """ Get all followed squeaks. """
        sql = """
        SELECT * FROM squeak
        JOIN profile
        ON squeak.author_address=profile.address
        WHERE squeak.block_header IS NOT NULL
        AND profile.following
        ORDER BY n_block_height DESC, n_time DESC;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            return [self._parse_squeak_entry_with_profile(row) for row in rows]

    def get_squeak_entries_with_profile_for_address(
        self, address, min_block, max_block
    ):
        """ Get a squeak. """
        sql = """
        SELECT * FROM squeak
        LEFT JOIN profile
        ON squeak.author_address=profile.address
        WHERE squeak.block_header IS NOT NULL
        AND squeak.author_address=%s
        AND n_block_height >= %s
        AND n_block_height <= %s
        ORDER BY n_block_height DESC, n_time DESC;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (address, min_block, max_block))
            rows = curs.fetchall()
            return [self._parse_squeak_entry_with_profile(row) for row in rows]

    def get_thread_ancestor_squeak_entries_with_profile(self, squeak_hash_str):
        """ Get all reply ancestors of squeak hash. """
        sql = """
        WITH RECURSIVE is_thread_ancestor(hash, depth) AS (
            VALUES(%s, 1)
          UNION\n
            SELECT squeak.hash_reply_sqk AS hash, is_thread_ancestor.depth + 1 AS depth FROM squeak, is_thread_ancestor
            WHERE squeak.hash=is_thread_ancestor.hash
          )
          SELECT * FROM squeak
          JOIN is_thread_ancestor
            ON squeak.hash=is_thread_ancestor.hash
          LEFT JOIN profile
            ON squeak.author_address=profile.address
          WHERE squeak.block_header IS NOT NULL
          ORDER BY is_thread_ancestor.depth DESC;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash_str,))
            rows = curs.fetchall()
            return [self._parse_squeak_entry_with_profile(row) for row in rows]

    def lookup_squeaks(self, addresses, min_block, max_block, include_unverified=False, include_locked=False):
        """ Lookup squeaks. """
        sql = """
        SELECT hash FROM squeak
        WHERE author_address IN %s
        AND n_block_height >= %s
        AND n_block_height <= %s
        AND (vch_decryption_key IS NOT NULL) OR %s
        AND ((block_header IS NOT NULL) OR %s);
        """
        addresses_tuple = tuple(addresses)

        if not addresses:
            return []

        with self.get_cursor() as curs:
            # mogrify to debug.
            # logger.info(curs.mogrify(sql, (addresses_tuple, min_block, max_block)))
            curs.execute(
                sql, (addresses_tuple, min_block, max_block, include_locked, include_unverified)
            )
            rows = curs.fetchall()
            hashes = [bytes.fromhex(row["hash"]) for row in rows]
            return hashes

    def lookup_squeaks_by_time(
        self, addresses, interval_seconds, include_unverified=False
    ):
        """ Lookup squeaks. """
        sql = """
        SELECT hash FROM squeak
        WHERE author_address IN %s
        AND created > now() - interval '%s seconds'
        AND vch_decryption_key IS NOT NULL
        AND ((block_header IS NOT NULL) OR %s);
        """
        addresses_tuple = tuple(addresses)

        if not addresses:
            return []

        with self.get_cursor() as curs:
            # mogrify to debug.
            # logger.info(curs.mogrify(sql, (addresses_tuple, min_block, max_block)))
            curs.execute(sql, (addresses_tuple, interval_seconds, include_unverified))
            rows = curs.fetchall()
            hashes = [bytes.fromhex(row["hash"]) for row in rows]
            return hashes

    def lookup_squeaks_needing_offer(self, addresses, min_block, max_block, peer_id, include_unverified=False):
        """ Lookup squeaks that are locked and don't have an offer. """
        sql = """
        SELECT hash FROM squeak
        LEFT JOIN offer
        ON squeak.hash=offer.squeak_hash
        AND offer.peer_id=%s
        WHERE author_address IN %s
        AND n_block_height >= %s
        AND n_block_height <= %s
        AND vch_decryption_key IS NULL
        AND ((block_header IS NOT NULL) OR %s)
        AND offer.squeak_hash IS NULL
        """
        addresses_tuple = tuple(addresses)

        if not addresses:
            return []

        with self.get_cursor() as curs:
            # mogrify to debug.
            # logger.info(curs.mogrify(sql, (addresses_tuple, min_block, max_block)))
            curs.execute(
                sql, (peer_id, addresses_tuple, min_block, max_block, include_unverified)
            )
            rows = curs.fetchall()
            hashes = [bytes.fromhex(row["hash"]) for row in rows]
            return hashes

    def insert_profile(self, squeak_profile):
        """ Insert a new squeak profile. """
        sql = """
        INSERT INTO profile(profile_name, private_key, address, sharing, following, whitelisted)
        VALUES(%s, %s, %s, %s, %s, %s)
        RETURNING profile_id;
        """
        with self.get_cursor() as curs:
            # execute the INSERT statement
            curs.execute(
                sql,
                (
                    squeak_profile.profile_name,
                    squeak_profile.private_key,
                    squeak_profile.address,
                    squeak_profile.sharing,
                    squeak_profile.following,
                    squeak_profile.whitelisted,
                ),
            )
            # get the new profile id back
            row = curs.fetchone()
            return row["profile_id"]

    def get_signing_profiles(self):
        """ Get all signing profiles. """
        sql = """
        SELECT * FROM profile
        WHERE private_key IS NOT NULL;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_contact_profiles(self):
        """ Get all contact profiles. """
        sql = """
        SELECT * FROM profile
        WHERE private_key IS NULL;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_whitelisted_profiles(self):
        """ Get all whitelisted profiles. """
        sql = """
        SELECT * FROM profile
        WHERE whitelisted;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_following_profiles(self):
        """ Get all following profiles. """
        sql = """
        SELECT * FROM profile
        WHERE following;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_sharing_profiles(self):
        """ Get all sharing profiles. """
        sql = """
        SELECT * FROM profile
        WHERE sharing;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_profile(self, profile_id):
        """ Get a profile. """
        sql = """
        SELECT * FROM profile WHERE profile_id=%s"""
        with self.get_cursor() as curs:
            curs.execute(sql, (profile_id,))
            row = curs.fetchone()
            return self._parse_squeak_profile(row)

    def get_profile_by_address(self, address):
        """ Get a profile by address. """
        sql = """
        SELECT * FROM profile
        WHERE address=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (address,))
            row = curs.fetchone()
            return self._parse_squeak_profile(row)

    def set_profile_whitelisted(self, profile_id, whitelisted):
        """ Set a profile is whitelisted. """
        sql = """
        UPDATE profile
        SET whitelisted=%s
        WHERE profile_id=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (whitelisted, profile_id,))

    def set_profile_following(self, profile_id, following):
        """ Set a profile is following. """
        sql = """
        UPDATE profile
        SET following=%s
        WHERE profile_id=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (following, profile_id,))

    def set_profile_sharing(self, profile_id, sharing):
        """ Set a profile is sharing. """
        sql = """
        UPDATE profile
        SET sharing=%s
        WHERE profile_id=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (sharing, profile_id,))

    def delete_profile(self, profile_id):
        """ Delete a profile. """
        sql = """
        DELETE FROM profile
        WHERE profile_id=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (profile_id,))

    def get_unverified_block_squeaks(self):
        """ Get all squeaks without block header. """
        sql = """
        SELECT hash FROM squeak
        WHERE block_header IS NULL;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            hashes = [bytes.fromhex(row["hash"]) for row in rows]
            return hashes

    def delete_squeak(self, squeak_hash):
        """ Delete a squeak. """
        sql = """
        DELETE FROM squeak WHERE hash=%s;
        """
        squeak_hash_str = squeak_hash.hex()
        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash_str,))

    def mark_squeak_block_valid(self, squeak_hash, block_header):
        """ Add the block header to a squeak. """
        sql = """
        UPDATE squeak
        SET block_header=%s
        WHERE hash=%s;
        """
        squeak_hash_str = squeak_hash.hex()
        with self.get_cursor() as curs:
            # execute the UPDATE statement
            curs.execute(sql, (block_header, squeak_hash_str,))

    def delete_squeak(self, squeak_hash):
        """ Delete a squeak. """
        sql = """
        DELETE FROM squeak
        WHERE squeak.hash=%s
        """
        squeak_hash_str = squeak_hash.hex()
        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash_str,))

    def insert_peer(self, squeak_peer):
        """ Insert a new squeak peer. """
        logger.info("Inserting peer: {}".format(squeak_peer))
        ins = self.peers.insert().values(
            peer_name=squeak_peer.peer_name,
            server_host=squeak_peer.host,
            server_port=squeak_peer.port,
            uploading=squeak_peer.uploading,
            downloading=squeak_peer.downloading,
        )
        logger.info("Insert peer params: {}".format(ins.compile().params))
        with self.engine.connect() as connection:
            res = connection.execute(ins)
            peer_id = res.inserted_primary_key[0]
            logger.info("Inserted peer and got id: {}".format(peer_id))
            return peer_id

    def get_peer(self, peer_id):
        """ Get a peer. """
        s = select([self.peers]).where(self.peers.c.peer_id == peer_id)
        with self.engine.connect() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            return self._parse_squeak_peer(row)

    def get_peers(self):
        """ Get all peers. """
        s = select([self.peers])
        with self.engine.connect() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            peers = [self._parse_squeak_peer(row) for row in rows]
            return peers

    def set_peer_downloading(self, peer_id, downloading):
        """ Set a peer is downloading. """
        stmt = self.peers.update().\
            where(self.peers.c.peer_id == peer_id).\
            values(downloading=downloading)
        with self.engine.connect() as connection:
            connection.execute(stmt)

    def set_peer_uploading(self, peer_id, uploading):
        """ Set a peer is uploading. """
        sql = """
        UPDATE peer
        SET uploading=%s
        WHERE peer_id=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (uploading, peer_id,))

    def delete_peer(self, peer_id):
        """ Delete a peer. """
        sql = """
        DELETE FROM peer WHERE peer_id=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (peer_id,))

    def insert_offer(self, offer):
        """ Insert a new offer. """
        sql = """
        INSERT INTO offer(squeak_hash, key_cipher, iv, price_msat, payment_hash, invoice_timestamp, invoice_expiry, payment_request, destination, node_host, node_port, peer_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING offer_id;
        """
        with self.get_cursor() as curs:
            # execute the INSERT statement
            curs.execute(
                sql,
                (
                    offer.squeak_hash.hex(),
                    offer.key_cipher,
                    offer.iv,
                    offer.price_msat,
                    offer.payment_hash.hex(),
                    offer.invoice_timestamp,
                    offer.invoice_expiry,
                    offer.payment_request,
                    offer.destination,
                    offer.node_host,
                    offer.node_port,
                    offer.peer_id,
                ),
            )
            # get the new offer id back
            row = curs.fetchone()
            return row["offer_id"]

    def get_offers(self, squeak_hash):
        """ Get offers for a squeak hash. """
        sql = """
        SELECT * FROM offer
        WHERE squeak_hash=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash,))
            rows = curs.fetchall()
            offers = [self._parse_offer(row) for row in rows]
            return offers

    def get_offers_with_peer(self, squeak_hash):
        """ Get offers with peer for a squeak hash. """
        sql = """
        SELECT * FROM offer
        LEFT JOIN peer
        ON offer.peer_id=peer.peer_id
        WHERE squeak_hash=%s;
        """
        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash,))
            rows = curs.fetchall()
            offers_with_peer = [self._parse_offer_with_peer(row) for row in rows]
            return offers_with_peer

    def delete_expired_offers(self):
        """ Delete all expired offers. """
        sql = """
        DELETE FROM offer
        WHERE now() > to_timestamp(invoice_timestamp + invoice_expiry)
        RETURNING *;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            return len(rows)

    def _parse_squeak_entry(self, row):
        if row is None:
            return None
        vch_decryption_key_column = row["vch_decryption_key"]
        vch_decryption_key = (
            bytes(vch_decryption_key_column) if vch_decryption_key_column else b''
        )
        squeak = CSqueak(
            nVersion=row["n_version"],
            hashEncContent=bytes.fromhex(row["hash_enc_content"]),
            hashReplySqk=bytes.fromhex(row["hash_reply_sqk"]),
            hashBlock=bytes.fromhex(row["hash_block"]),
            nBlockHeight=row["n_block_height"],
            vchScriptPubKey=bytes(row["vch_script_pub_key"]),
            vchEncryptionKey=bytes(row["vch_encryption_key"]),
            encDatakey=bytes.fromhex(row["enc_data_key"]),
            iv=bytes.fromhex((row["iv"])),
            nTime=row["n_time"],
            nNonce=row["n_nonce"],
            encContent=bytes.fromhex((row["enc_content"])),
            vchScriptSig=bytes(row["vch_script_sig"]),
            vchDecryptionKey=vch_decryption_key,
        )
        block_header_column = row["block_header"]
        block_header_bytes = bytes(block_header_column) if block_header_column else None
        block_header = (
            parse_block_header(block_header_bytes) if block_header_bytes else None
        )
        return SqueakEntry(squeak=squeak, block_header=block_header)

    def _parse_squeak_profile(self, row):
        if row is None:
            return None
        if row["profile_id"] is None:
            return None
        private_key_column = row["private_key"]
        private_key = bytes(private_key_column) if private_key_column else None
        return SqueakProfile(
            profile_id=row["profile_id"],
            profile_name=row["profile_name"],
            private_key=private_key,
            address=row["address"],
            sharing=row["sharing"],
            following=row["following"],
            whitelisted=row["whitelisted"],
        )

    def _parse_squeak_entry_with_profile(self, row):
        if row is None:
            return None
        squeak_entry = self._parse_squeak_entry(row)
        squeak_profile = self._parse_squeak_profile(row)
        return SqueakEntryWithProfile(
            squeak_entry=squeak_entry, squeak_profile=squeak_profile,
        )

    def _parse_squeak_peer(self, row):
        if row is None:
            return None
        return SqueakPeer(
            peer_id=row["peer_id"],
            peer_name=row["peer_name"],
            host=row["server_host"],
            port=row["server_port"],
            uploading=row["uploading"],
            downloading=row["downloading"],
        )

    def _parse_offer(self, row):
        if row is None:
            return None
        return Offer(
            offer_id=row["offer_id"],
            squeak_hash=row["squeak_hash"],
            key_cipher=row["key_cipher"],
            iv=row["iv"],
            price_msat=row["price_msat"],
            payment_hash=row["payment_hash"],
            invoice_timestamp=row["invoice_timestamp"],
            invoice_expiry=row["invoice_expiry"],
            payment_request=row["payment_request"],
            destination=row["destination"],
            node_host=row["node_host"],
            node_port=row["node_port"],
            proof=None,
            peer_id=row["peer_id"],
        )

    def _parse_offer_with_peer(self, row):
        if row is None:
            return None
        offer = self._parse_offer(row)
        peer = self._parse_squeak_peer(row)
        return OfferWithPeer(
            offer=offer,
            peer=peer,
        )

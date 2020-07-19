import logging
from contextlib import contextmanager

from psycopg2 import pool
from squeak.core import CSqueak

from squeakserver.server.squeak_profile import SqueakProfile
from squeakserver.server.util import get_hash

logger = logging.getLogger(__name__)


class PostgresDb():

    def __init__(self, params):
        self.connection_pool = pool.ThreadedConnectionPool(5, 20, **params)

    # Get Cursor
    @contextmanager
    def get_cursor(self):
        con = self.connection_pool.getconn()
        try:
            yield con.cursor()
            con.commit()
        finally:
            self.connection_pool.putconn(con)

    def get_version(self):
        """ Connect to the PostgreSQL database server """
        with self.get_cursor() as curs:
            # execute a statement
            logger.info('PostgreSQL database version:')
            curs.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = curs.fetchone()
            logger.info(db_version)

    def init(self):
        """ Create the tables and indices in the database. """
        with self.get_cursor() as curs:
            # execute a statement
            logger.info('Setting up database tables...')
            curs.execute(open("init.sql", "r").read())

    def insert_squeak(self, squeak):
        """ Insert a new squeak. """
        sql = """
        INSERT INTO squeak(hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, vchScriptPubKey, vchEncryptionKey, encDatakey, iv, nTime, nNonce, encContent, vchScriptSig, address, vchDecryptionKey)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING hash;"""

        with self.get_cursor() as curs:
            # execute the INSERT statement
            curs.execute(sql, (
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
                squeak.vchDecryptionKey,
            ))
            # get the generated hash back
            row = curs.fetchone()
            return bytes.fromhex(row[0])

    def get_squeak(self, squeak_hash):
        """ Get a squeak. """
        sql = """
        SELECT * FROM squeak WHERE hash=%s"""

        squeak_hash_str = squeak_hash.hex()

        with self.get_cursor() as curs:
            curs.execute(sql, (squeak_hash_str,))
            row = curs.fetchone()

            squeak = CSqueak(
                nVersion=row[2],
                hashEncContent=bytes.fromhex(row[3]),
                hashReplySqk=bytes.fromhex(row[4]),
                hashBlock=bytes.fromhex(row[5]),
                nBlockHeight=row[6],
                vchScriptPubKey=row[7],
                vchEncryptionKey=row[8],
                encDatakey=bytes.fromhex(row[9]),
                iv=bytes.fromhex((row[10])),
                nTime=row[11],
                nNonce=row[12],
                encContent=bytes.fromhex((row[13])),
                vchScriptSig=row[14],
                vchDecryptionKey=row[16],
            )
            return squeak

    def lookup_squeaks(self, addresses, min_block, max_block):
        """ Lookup squeaks. """
        sql = """
        SELECT hash FROM squeak
        WHERE address IN %s
        AND nBlockHeight >= %s
        AND nBlockHeight <= %s"""
        addresses_tuple = tuple(addresses)

        if not addresses:
            return []

        with self.get_cursor() as curs:
            # mogrify to debug.
            # logger.info(curs.mogrify(sql, (addresses_tuple, min_block, max_block)))
            curs.execute(sql, (addresses_tuple, min_block, max_block))
            rows = curs.fetchall()
            hashes = [
                bytes.fromhex(row[0])
                for row in rows
            ]
            return hashes

    def insert_profile(self, squeak_profile):
        """ Insert a new squeak profile. """
        sql = """
        INSERT INTO profile(profile_name, private_key, address, sharing, following)
        VALUES(%s, %s, %s, %s, %s)
        RETURNING profile_id;
        """
        with self.get_cursor() as curs:
            # execute the INSERT statement
            curs.execute(sql, (
                squeak_profile.profile_name,
                squeak_profile.private_key,
                squeak_profile.address,
                squeak_profile.sharing,
                squeak_profile.following,
            ))
            logger.info('Inserted new profile')
            # get the new profile id back
            row = curs.fetchone()
            logger.info('New profile id: {}'.format(row[0]))
            return row[0]

    def get_profile(self, profile_id):
        """ Get a profile. """
        sql = """
        SELECT * FROM profile WHERE profile_id=%s"""

        with self.get_cursor() as curs:
            curs.execute(sql, (profile_id,))
            row = curs.fetchone()

            squeak_profile = SqueakProfile(
                profile_id=row[0],
                profile_name=row[2],
                private_key=bytes(row[3]),
                address=row[4],
                sharing=row[5],
                following=row[6],
            )
            return squeak_profile

    def get_unverified_block_squeaks(self):
        """ Get all squeaks without block header. """
        sql = """
        SELECT hash FROM squeak
        WHERE block_header IS NULL;
        """
        with self.get_cursor() as curs:
            curs.execute(sql)
            rows = curs.fetchall()
            hashes = [
                bytes.fromhex(row[0])
                for row in rows
            ]
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
            curs.execute(sql, (
                block_header,
                squeak_hash,
            ))
            logger.info('Updated squeak with block header')

import logging

from contextlib import contextmanager

import psycopg2
from psycopg2 import pool

from squeak.core import CSqueak
from squeak.core import CSqueakEncContent
from squeak.core.script import CScript

from squeakserver.server.util import get_hash


logger = logging.getLogger(__name__)


class PostgresDb():

    def __init__(self, params):
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(5, 20, **params)

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
        INSERT INTO squeak(hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, scriptPubKey, hashDataKey, vchIv, nTime, nNonce, encContent, scriptSig, address, vchDataKey, content)
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
                bytes(squeak.scriptPubKey).hex(),
                squeak.hashDataKey.hex(),
                squeak.vchIv.hex(),
                squeak.nTime,
                squeak.nNonce,
                bytes(squeak.encContent.vchEncContent).hex(),
                bytes(squeak.scriptSig).hex(),
                str(squeak.GetAddress()),
                squeak.vchDataKey.hex(),
                squeak.GetDecryptedContentStr(),
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
                scriptPubKey=CScript(bytes.fromhex(row[7])),
                hashDataKey=bytes.fromhex(row[8]),
                vchIv=bytes.fromhex((row[9])),
                nTime=row[10],
                nNonce=row[11],
                encContent=CSqueakEncContent(bytes.fromhex((row[12]))),
                scriptSig=CScript(bytes.fromhex((row[13]))),
                vchDataKey=bytes.fromhex((row[15])),
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

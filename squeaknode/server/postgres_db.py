import psycopg2

from squeak.core import CSqueak
from squeak.core import CSqueakEncContent
from squeak.core.script import CScript


class PostgresDb():

    def __init__(self, params):
        self.params = params

    def get_connection(self):
        """ Connect to the PostgreSQL database server """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as curs:
	        # execute a statement
                print('PostgreSQL database version:')
                curs.execute('SELECT version()')

                # display the PostgreSQL database server version
                db_version = curs.fetchone()
                print(db_version)

    def insert_squeak(self, squeak):
        """ Insert a new squeak. """
        sql = """
        INSERT INTO squeak(hash, nVersion, hashEncContent, hashReplySqk, hashBlock, nBlockHeight, scriptPubKey, hashDataKey, vchIv, nTime, nNonce, encContent, scriptSig, address, vchDataKey, content)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING hash;"""

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as curs:
                # execute the INSERT statement
                curs.execute(sql, (
                    squeak.GetHash().hex(),
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
                squeak_hash = curs.fetchone()[0]
                return squeak_hash

    def get_squeak(self, squeak_hash):
        """ Get a squeak. """
        sql = """
        SELECT * FROM squeak WHERE hash=%s"""

        squeak_hash_str = squeak_hash.hex()

        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as curs:
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

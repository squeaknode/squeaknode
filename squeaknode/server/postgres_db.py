import psycopg2


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

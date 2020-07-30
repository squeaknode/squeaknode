import logging
from contextlib import contextmanager

from psycopg2 import pool
from psycopg2.extras import DictCursor
from squeak.core import CSqueak

from squeakserver.core.squeak_entry import SqueakEntry
from squeakserver.core.squeak_entry_with_profile import SqueakEntryWithProfile
from squeakserver.server.squeak_profile import SqueakProfile
from squeakserver.server.util import get_hash
from squeakserver.blockchain.util import parse_block_header


logger = logging.getLogger(__name__)


class PostgresDb:
    def __init__(self, params):
        self.connection_pool = pool.ThreadedConnectionPool(5, 20, **params)

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

    def init(self):
        """ Create the tables and indices in the database. """
        with self.get_cursor() as curs:
            # execute a statement
            logger.info("Setting up database tables...")
            curs.execute(open("init.sql", "r").read())

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
                    squeak.vchDecryptionKey,
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

    def get_squeak_entries_with_profile_for_address(self, address, min_block, max_block):
        """ Get a squeak. """
        sql = """
        SELECT * FROM squeak
        JOIN profile
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

    def lookup_squeaks(self, addresses, min_block, max_block, include_unverified=False):
        """ Lookup squeaks. """
        sql = """
        SELECT hash FROM squeak
        WHERE author_address IN %s
        AND n_block_height >= %s
        AND n_block_height <= %s
        AND vch_decryption_key IS NOT NULL
        AND ((block_header IS NOT NULL) OR %s);
        """
        addresses_tuple = tuple(addresses)

        if not addresses:
            return []

        with self.get_cursor() as curs:
            # mogrify to debug.
            # logger.info(curs.mogrify(sql, (addresses_tuple, min_block, max_block)))
            curs.execute(sql, (addresses_tuple, min_block, max_block, include_unverified))
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

    def _parse_squeak_entry(self, row):
        vch_decryption_key_column = row["vch_decryption_key"]
        vch_decryption_key = (
            bytes(vch_decryption_key_column) if vch_decryption_key_column else None
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
        block_header = parse_block_header(block_header_bytes) if block_header_bytes else None
        return SqueakEntry(squeak=squeak, block_header=block_header)

    def _parse_squeak_profile(self, row):
        if row is None:
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

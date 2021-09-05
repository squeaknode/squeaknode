# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
from contextlib import contextmanager
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Iterator
from typing import List
from typing import Optional

import sqlalchemy
from bitcoin.core import CBlockHeader
from sqlalchemy import func
from sqlalchemy import literal
from sqlalchemy.sql import select
from sqlalchemy.sql import tuple_
from squeak.core import CSqueak

from squeaknode.core.lightning_address import LightningAddressHostPort
from squeaknode.core.peer_address import PeerAddress
from squeaknode.core.received_offer import ReceivedOffer
from squeaknode.core.received_payment import ReceivedPayment
from squeaknode.core.received_payment_summary import ReceivedPaymentSummary
from squeaknode.core.sent_offer import SentOffer
from squeaknode.core.sent_payment import SentPayment
from squeaknode.core.sent_payment_summary import SentPaymentSummary
from squeaknode.core.squeak_entry import SqueakEntry
from squeaknode.core.squeak_peer import SqueakPeer
from squeaknode.core.squeak_profile import SqueakProfile
from squeaknode.core.util import get_hash
from squeaknode.db.exception import DuplicateReceivedPaymentError
from squeaknode.db.migrations import run_migrations
from squeaknode.db.models import Models


MAX_INT = 999999999999
MAX_HASH = b'\xff' * 32


logger = logging.getLogger(__name__)


class SqueakDb:
    def __init__(self, engine, schema=None):
        self.engine = engine
        self.schema = schema
        self.models = Models(schema=schema)

    @contextmanager
    def get_connection(self):
        with self.engine.connect() as connection:
            yield connection

    def init(self):
        """ Create the tables and indices in the database. """
        logger.debug("SqlAlchemy version: {}".format(sqlalchemy.__version__))
        run_migrations(self.engine)

    @property
    def squeaks(self):
        return self.models.squeaks

    @property
    def profiles(self):
        return self.models.profiles

    @property
    def peers(self):
        return self.models.peers

    @property
    def received_offers(self):
        return self.models.received_offers

    @property
    def sent_payments(self):
        return self.models.sent_payments

    @property
    def received_payments(self):
        return self.models.received_payments

    @property
    def sent_offers(self):
        return self.models.sent_offers

    @property
    def squeak_has_secret_key(self):
        return self.squeaks.c.secret_key != None  # noqa: E711

    @property
    def squeak_is_liked(self):
        return self.squeaks.c.liked_time != None  # noqa: E711

    @property
    def squeak_is_not_liked(self):
        return self.squeaks.c.liked_time == None  # noqa: E711

    @property
    def squeak_has_no_secret_key(self):
        return self.squeaks.c.secret_key == None  # noqa: E711

    def squeak_is_older_than_retention(self, interval_s):
        return self.datetime_now - timedelta(seconds=interval_s) > \
            self.squeaks.c.created

    @property
    def profile_has_private_key(self):
        return self.profiles.c.private_key != None  # noqa: E711

    @property
    def profile_has_no_private_key(self):
        return self.profiles.c.private_key == None  # noqa: E711

    @property
    def profile_is_following(self):
        return self.profiles.c.following == True  # noqa: E711

    @property
    def received_offer_does_not_exist(self):
        return self.received_offers.c.squeak_hash == None  # noqa: E711

    @property
    def datetime_now(self):
        return datetime.now(timezone.utc)

    def datetime_from_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp, timezone.utc)

    def received_offer_should_be_deleted(self):
        expire_time = (
            self.received_offers.c.invoice_timestamp
            + self.received_offers.c.invoice_expiry
        )
        return self.datetime_now.timestamp() >= expire_time

    @property
    def received_offer_is_not_paid(self):
        return self.received_offers.c.paid == False  # noqa: E711

    @property
    def received_offer_is_not_expired(self):
        expire_time = (
            self.received_offers.c.invoice_timestamp
            + self.received_offers.c.invoice_expiry
        )
        return self.datetime_now.timestamp() < expire_time

    def sent_offer_should_be_deleted(self, interval_s):
        expire_time = (
            self.sent_offers.c.invoice_timestamp
            + self.sent_offers.c.invoice_expiry
        )
        return self.datetime_now.timestamp() >= expire_time + interval_s

    @property
    def sent_offer_is_not_paid(self):
        return self.sent_offers.c.paid == False  # noqa: E711

    @property
    def sent_offer_is_not_expired(self):
        expire_time = (
            self.sent_offers.c.invoice_timestamp
            + self.sent_offers.c.invoice_expiry
        )
        return self.datetime_now.timestamp() < expire_time

    def insert_squeak(self, squeak: CSqueak, block_header: CBlockHeader) -> bytes:
        """ Insert a new squeak.

        Return the hash (bytes) of the inserted squeak.
        """
        ins = self.squeaks.insert().values(
            hash=get_hash(squeak),
            squeak=squeak.serialize(),
            hash_reply_sqk=squeak.hashReplySqk if squeak.is_reply else None,
            hash_block=squeak.hashBlock,
            n_block_height=squeak.nBlockHeight,
            n_time=squeak.nTime,
            author_address=str(squeak.GetAddress()),
            secret_key=None,
            block_time=block_header.nTime,
        )
        with self.get_connection() as connection:
            try:
                connection.execute(ins)
                # inserted_squeak_hash = res.inserted_primary_key[0]
            except sqlalchemy.exc.IntegrityError:
                pass
            return get_hash(squeak)

    def get_squeak(self, squeak_hash: bytes) -> Optional[CSqueak]:
        """ Get a squeak. """
        s = select([self.squeaks]).where(
            self.squeaks.c.hash == squeak_hash)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_squeak(row)

    def get_squeak_secret_key(self, squeak_hash: bytes) -> Optional[bytes]:
        """ Get a squeak secret key. """
        s = select([self.squeaks]).where(
            self.squeaks.c.hash == squeak_hash)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return row["secret_key"]

    def get_squeak_entry(self, squeak_hash: bytes) -> Optional[SqueakEntry]:
        """ Get a squeak with the author profile. """
        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .where(self.squeaks.c.hash == squeak_hash)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_squeak_entry(row)

    def get_timeline_squeak_entries(
            self,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        """ Get all followed squeaks. """
        last_block_height = last_entry.block_height if last_entry else MAX_INT
        last_squeak_time = last_entry.squeak_time if last_entry else MAX_INT
        last_squeak_hash = last_entry.squeak_hash if last_entry else MAX_HASH
        logger.info("""Timeline db query with
        limit: {}
        block_height: {}
        squeak_time: {}
        squeak_hash: {}
        """.format(
            limit,
            last_block_height,
            last_squeak_time,
            last_squeak_hash.hex(),
        ))
        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .where(self.profile_is_following)
            .where(
                tuple_(
                    self.squeaks.c.n_block_height,
                    self.squeaks.c.n_time,
                    self.squeaks.c.hash,
                ) < tuple_(
                    last_block_height,
                    last_squeak_time,
                    last_squeak_hash,
                )
            )
            .order_by(
                self.squeaks.c.n_block_height.desc(),
                self.squeaks.c.n_time.desc(),
                self.squeaks.c.hash.desc(),
            )
            .limit(limit)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            return [self._parse_squeak_entry(row) for row in rows]

    def get_liked_squeak_entries(
            self,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        """ Get liked squeaks. """
        last_liked_time = self.datetime_from_timestamp(
            last_entry.liked_time) if last_entry else self.datetime_now
        last_squeak_hash = last_entry.squeak_hash if last_entry else MAX_HASH
        logger.info("""Liked squeaks db query with
        limit: {}
        last_liked_time: {}
        last_squeak_hash: {}
        """.format(
            limit,
            last_liked_time,
            last_squeak_hash.hex(),
        ))
        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .where(
                self.squeak_is_liked,
            )
            .where(
                tuple_(
                    self.squeaks.c.liked_time,
                    self.squeaks.c.hash,
                ) < tuple_(
                    last_liked_time,
                    last_squeak_hash,
                )
            )
            .order_by(
                self.squeaks.c.liked_time.desc(),
                self.squeaks.c.hash.desc(),
            )
            .limit(limit)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            return [self._parse_squeak_entry(row) for row in rows]

    def get_squeak_entries_for_address(
            self,
            address: str,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        """ Get a squeak. """
        last_block_height = last_entry.block_height if last_entry else MAX_INT
        last_squeak_time = last_entry.squeak_time if last_entry else MAX_INT
        last_squeak_hash = last_entry.squeak_hash if last_entry else MAX_HASH
        logger.info("""Timeline db query with
        limit: {}
        block_height: {}
        squeak_time: {}
        squeak_hash: {}
        """.format(
            limit,
            last_block_height,
            last_squeak_time,
            last_squeak_hash.hex(),
        ))
        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .where(self.squeaks.c.author_address == address)
            .where(
                tuple_(
                    self.squeaks.c.n_block_height,
                    self.squeaks.c.n_time,
                    self.squeaks.c.hash,
                ) < tuple_(
                    last_block_height,
                    last_squeak_time,
                    last_squeak_hash,
                )
            )
            .order_by(
                self.squeaks.c.n_block_height.desc(),
                self.squeaks.c.n_time.desc(),
                self.squeaks.c.hash.desc(),
            )
            .limit(limit)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            return [self._parse_squeak_entry(row) for row in rows]

    def get_thread_ancestor_squeak_entries(self, squeak_hash: bytes) -> List[SqueakEntry]:
        """ Get all reply ancestors of squeak hash. """
        ancestors = (
            select(
                [
                    self.squeaks.c.hash.label("hash"),
                    literal(0).label("depth"),
                ]
            )
            .where(self.squeaks.c.hash == squeak_hash)
            .cte(recursive=True)
        )

        ancestors_alias = ancestors.alias()
        squeaks_alias = self.squeaks.alias()

        ancestors = ancestors.union_all(
            select(
                [
                    squeaks_alias.c.hash_reply_sqk.label("hash"),
                    (ancestors_alias.c.depth + 1).label("depth"),
                ]
            ).where(squeaks_alias.c.hash == ancestors_alias.c.hash)
        )

        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.join(
                    ancestors,
                    ancestors.c.hash == self.squeaks.c.hash,
                ).outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .order_by(
                ancestors.c.depth.desc(),
            )
        )

        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            return [self._parse_squeak_entry(row) for row in rows]

        # sql = """
        # WITH RECURSIVE is_thread_ancestor(hash, depth) AS (
        #     VALUES(%s, 1)
        #   UNION\n
        #     SELECT squeak.hash_reply_sqk AS hash, is_thread_ancestor.depth + 1 AS depth FROM squeak, is_thread_ancestor
        #     WHERE squeak.hash=is_thread_ancestor.hash
        #   )
        #   SELECT * FROM squeak
        #   JOIN is_thread_ancestor
        #     ON squeak.hash=is_thread_ancestor.hash
        #   LEFT JOIN profile
        #     ON squeak.author_address=profile.address
        #   WHERE squeak.block_header IS NOT NULL
        #   ORDER BY is_thread_ancestor.depth DESC;
        # """
        # with self.get_cursor() as curs:
        #     curs.execute(sql, (squeak_hash_str,))
        #     rows = curs.fetchall()
        #     return [self._parse_squeak_entry_with_profile(row) for row in rows]

    def get_thread_reply_squeak_entries(
            self,
            squeak_hash: bytes,
            limit: int,
            last_entry: Optional[SqueakEntry],
    ) -> List[SqueakEntry]:
        """ Get all replies for a squeak hash. """
        last_block_height = last_entry.block_height if last_entry else MAX_INT
        last_squeak_time = last_entry.squeak_time if last_entry else MAX_INT
        last_squeak_hash = last_entry.squeak_hash if last_entry else MAX_HASH
        logger.info("""Timeline db query with
        limit: {}
        block_height: {}
        squeak_time: {}
        squeak_hash: {}
        """.format(
            limit,
            last_block_height,
            last_squeak_time,
            last_squeak_hash.hex(),
        ))
        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .where(self.squeaks.c.hash_reply_sqk == squeak_hash)
            .where(
                tuple_(
                    self.squeaks.c.n_block_height,
                    self.squeaks.c.n_time,
                    self.squeaks.c.hash,
                ) < tuple_(
                    last_block_height,
                    last_squeak_time,
                    last_squeak_hash,
                )
            )
            .order_by(
                self.squeaks.c.n_block_height.desc(),
                self.squeaks.c.n_time.desc(),
                self.squeaks.c.hash.desc(),
            )
            .limit(limit)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            return [self._parse_squeak_entry(row) for row in rows]

    def lookup_squeaks(
        self,
        addresses: List[str],
        min_block: int,
        max_block: int,
        reply_to_hash: bytes,
        include_locked: bool = False,
    ) -> List[bytes]:
        """ Lookup squeaks. """
        logger.debug("""Running lookup query with
        addresses: {},
        min_block: {}
        max_block: {}
        reply_to_hash: {!r}
        include_locked: {}""".format(
            addresses,
            min_block,
            max_block,
            reply_to_hash,
            include_locked,
        ))

        s = select([self.squeaks.c.hash])
        if addresses:
            s = s.where(self.squeaks.c.author_address.in_(addresses))
        if min_block:
            s = s.where(self.squeaks.c.n_block_height >= min_block)
        if max_block:
            s = s.where(self.squeaks.c.n_block_height <= max_block)
        if reply_to_hash:
            s = s.where(self.squeaks.c.hash_reply_sqk == reply_to_hash)
        if not include_locked:
            s = s.where(self.squeak_has_secret_key)
        s = s.order_by(
            self.squeaks.c.n_block_height.desc(),
            self.squeaks.c.n_time.desc(),
            self.squeaks.c.hash.desc(),
        )

        logger.debug("Query s: {}".format(s))

        with self.get_connection() as connection:
            # logger.debug("Mogrify lookup_squeaks: {}.".format(
            #     connection.connection.cursor().mogrify(s),
            # ))
            result = connection.execute(s)
            rows = result.fetchall()
            hashes = [(row["hash"]) for row in rows]
            return hashes

    def get_number_of_squeaks(self) -> int:
        """ Get total number of squeaks. """
        s = (
            select([
                func.count().label("num_squeaks"),
            ])
            .select_from(self.squeaks)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            num_squeaks = row["num_squeaks"]
            return num_squeaks

    def number_of_squeaks_with_address_with_block(
        self,
        address: str,
        block_height: int,
    ) -> int:
        """ Get number of squeaks with address with block height. """
        s = (
            select([
                func.count().label("num_squeaks"),
            ])
            .select_from(self.squeaks)
            .where(self.squeaks.c.author_address == address)
            .where(self.squeaks.c.n_block_height == block_height)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            num_squeaks = row["num_squeaks"]
            return num_squeaks

    def number_of_squeaks_with_address_in_block_range(
        self,
        address: str,
        min_block: int,
        max_block: int,
    ) -> int:
        """ Get number of squeaks with address in block range. """
        s = (
            select([
                func.count().label("num_squeaks"),
            ])
            .select_from(self.squeaks)
            .where(self.squeaks.c.author_address == address)
            .where(self.squeaks.c.n_block_height >= min_block)
            .where(self.squeaks.c.n_block_height <= max_block)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            num_squeaks = row["num_squeaks"]
            return num_squeaks

    def get_old_squeaks_to_delete(
            self,
            interval_s: int,
    ) -> List[bytes]:
        """ Get squeaks older than retention that meet the
        criteria for deletion.
        """
        s = (
            select([self.squeaks, self.profiles])
            .select_from(
                self.squeaks.outerjoin(
                    self.profiles,
                    self.profiles.c.address == self.squeaks.c.author_address,
                )
            )
            .where(self.squeak_is_older_than_retention(interval_s))
            .where(self.profile_has_no_private_key)
            .where(self.squeak_is_not_liked)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            hashes = [(row["hash"]) for row in rows]
            return hashes

    def insert_profile(self, squeak_profile: SqueakProfile) -> int:
        """ Insert a new squeak profile. """
        ins = self.profiles.insert().values(
            profile_name=squeak_profile.profile_name,
            private_key=squeak_profile.private_key,
            address=squeak_profile.address,
            following=squeak_profile.following,
        )
        with self.get_connection() as connection:
            res = connection.execute(ins)
            profile_id = res.inserted_primary_key[0]
            return profile_id

    def get_profiles(self) -> List[SqueakProfile]:
        """ Get all profiles. """
        s = select([self.profiles])
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_signing_profiles(self) -> List[SqueakProfile]:
        """ Get all signing profiles. """
        s = select([self.profiles]).where(self.profile_has_private_key)
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_contact_profiles(self) -> List[SqueakProfile]:
        """ Get all contact profiles. """
        s = select([self.profiles]).where(self.profile_has_no_private_key)
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_following_profiles(self) -> List[SqueakProfile]:
        """ Get all following profiles. """
        s = select([self.profiles]).where(self.profiles.c.following)
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_following_profiles_from_addreses(self, addresses: List[str]) -> List[SqueakProfile]:
        """ Get all following profiles. """
        s = (
            select([self.profiles])
            .where(self.profiles.c.following)
            .where(self.profiles.c.address.in_(addresses))
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            profiles = [self._parse_squeak_profile(row) for row in rows]
            return profiles

    def get_profile(self, profile_id: int) -> Optional[SqueakProfile]:
        """ Get a profile. """
        s = select([self.profiles]).where(
            self.profiles.c.profile_id == profile_id)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_squeak_profile(row)

    def get_profile_by_address(self, address: str) -> Optional[SqueakProfile]:
        """ Get a profile by address. """
        s = select([self.profiles]).where(self.profiles.c.address == address)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_squeak_profile(row)

    def get_profile_by_name(self, name: str) -> Optional[SqueakProfile]:
        """ Get a profile by name. """
        s = select([self.profiles]).where(self.profiles.c.profile_name == name)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_squeak_profile(row)

    def set_profile_following(self, profile_id: int, following: bool) -> None:
        """ Set a profile is following. """
        stmt = (
            self.profiles.update()
            .where(self.profiles.c.profile_id == profile_id)
            .values(following=following)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def set_profile_name(self, profile_id: int, profile_name: str) -> None:
        """ Set a profile name. """
        stmt = (
            self.profiles.update()
            .where(self.profiles.c.profile_id == profile_id)
            .values(profile_name=profile_name)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def delete_profile(self, profile_id: int) -> None:
        """ Delete a profile. """
        delete_profile_stmt = self.profiles.delete().where(
            self.profiles.c.profile_id == profile_id
        )
        with self.get_connection() as connection:
            connection.execute(delete_profile_stmt)

    def set_profile_image(self, profile_id: int, profile_image: bytes) -> None:
        """ Set a profile image. """
        stmt = (
            self.profiles.update()
            .where(self.profiles.c.profile_id == profile_id)
            .values(profile_image=profile_image)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def set_squeak_decryption_key(self, squeak_hash: bytes, secret_key: bytes, content: str) -> None:
        """ Set the decryption key and decrypted content of a squeak. """
        stmt = (
            self.squeaks.update()
            .where(self.squeaks.c.hash == squeak_hash)
            .values(
                secret_key=secret_key,
                content=content,
            )
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def set_squeak_liked(self, squeak_hash: bytes) -> None:
        """ Set the squeak to be liked. """
        stmt = (
            self.squeaks.update()
            .where(self.squeaks.c.hash == squeak_hash)
            .values(liked_time=self.datetime_now)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def set_squeak_unliked(self, squeak_hash: bytes) -> None:
        """ Set the squeak to be unliked. """
        stmt = (
            self.squeaks.update()
            .where(self.squeaks.c.hash == squeak_hash)
            .values(liked_time=None)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def delete_squeak(self, squeak_hash: bytes) -> None:
        """ Delete a squeak. """
        delete_squeak_stmt = self.squeaks.delete().where(
            self.squeaks.c.hash == squeak_hash
        )
        with self.get_connection() as connection:
            connection.execute(delete_squeak_stmt)

    def insert_peer(self, squeak_peer: SqueakPeer) -> int:
        """ Insert a new squeak peer. """
        ins = self.peers.insert().values(
            peer_name=squeak_peer.peer_name,
            host=squeak_peer.address.host,
            port=squeak_peer.address.port,
            autoconnect=squeak_peer.autoconnect,
        )
        with self.get_connection() as connection:
            res = connection.execute(ins)
            id = res.inserted_primary_key[0]
            return id

    def get_peer(self, peer_id: int) -> Optional[SqueakPeer]:
        """ Get a peer. """
        s = select([self.peers]).where(self.peers.c.peer_id == peer_id)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_squeak_peer(row)

    def get_peers(self) -> List[SqueakPeer]:
        """ Get all peers. """
        s = select([self.peers])
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            peers = [self._parse_squeak_peer(row) for row in rows]
            return peers

    def get_autoconnect_peers(self) -> List[SqueakPeer]:
        """ Get peers that are set to be autoconnect. """
        s = select([self.peers]).where(self.peers.c.autoconnect)
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            peers = [self._parse_squeak_peer(row) for row in rows]
            return peers

    def set_peer_autoconnect(self, peer_id: int, autoconnect: bool):
        """ Set a peer is autoconnect. """
        stmt = (
            self.peers.update()
            .where(self.peers.c.peer_id == peer_id)
            .values(autoconnect=autoconnect)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def set_peer_name(self, peer_id: int, peer_name: str):
        """ Set a peer name. """
        stmt = (
            self.peers.update()
            .where(self.peers.c.peer_id == peer_id)
            .values(peer_name=peer_name)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def delete_peer(self, peer_id: int):
        """ Delete a peer. """
        delete_peer_stmt = self.peers.delete().where(self.peers.c.peer_id == peer_id)
        with self.get_connection() as connection:
            connection.execute(delete_peer_stmt)

    def insert_received_offer(self, received_offer: ReceivedOffer):
        """ Insert a new received offer. """
        ins = self.received_offers.insert().values(
            squeak_hash=received_offer.squeak_hash,
            payment_hash=received_offer.payment_hash,
            nonce=received_offer.nonce,
            payment_point=received_offer.payment_point,
            invoice_timestamp=received_offer.invoice_timestamp,
            invoice_expiry=received_offer.invoice_expiry,
            price_msat=received_offer.price_msat,
            payment_request=received_offer.payment_request,
            destination=received_offer.destination,
            lightning_host=received_offer.lightning_address.host,
            lightning_port=received_offer.lightning_address.port,
            peer_host=received_offer.peer_address.host,
            peer_port=received_offer.peer_address.port,
        )
        with self.get_connection() as connection:
            res = connection.execute(ins)
            received_offer_id = res.inserted_primary_key[0]
            return received_offer_id

    def get_received_offers(self, squeak_hash: bytes) -> List[ReceivedOffer]:
        """ Get offers with peer for a squeak hash. """
        s = (
            select([self.received_offers])
            .where(self.received_offers.c.squeak_hash == squeak_hash)
            .where(self.received_offer_is_not_paid)
            .where(self.received_offer_is_not_expired)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            offers = [
                self._parse_received_offer(row)
                for row in rows
            ]
            return offers

    def get_received_offer(self, received_offer_id: int) -> Optional[ReceivedOffer]:
        """ Get offer with peer for an offer id. """
        s = (
            select([self.received_offers])
            .where(self.received_offers.c.received_offer_id == received_offer_id)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            offer = self._parse_received_offer(row)
            return offer

    def get_received_offer_for_squeak_and_peer(
            self,
            squeak_hash: bytes,
            peer_address: PeerAddress,
    ) -> Optional[ReceivedOffer]:
        """ Get offer with peer for a given peer address and squeak hash . """
        s = (
            select([self.received_offers])
            .where(self.received_offers.c.squeak_hash == squeak_hash)
            .where(self.received_offers.c.peer_host == peer_address.host)
            .where(self.received_offers.c.peer_port == peer_address.port)
            .where(self.received_offer_is_not_paid)
            .where(self.received_offer_is_not_expired)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            offer = self._parse_received_offer(row)
            return offer

    def delete_expired_received_offers(self):
        """ Delete all expired offers. """
        s = self.received_offers.delete().where(
            self.received_offer_should_be_deleted()
        )
        with self.get_connection() as connection:
            res = connection.execute(s)
            deleted_offers = res.rowcount
            return deleted_offers

    def delete_offers_for_squeak(self, squeak_hash: bytes):
        """ Delete all offers for a squeak hash. """
        s = self.received_offers.delete().where(
            self.received_offers.c.squeak_hash == squeak_hash)
        with self.get_connection() as connection:
            res = connection.execute(s)
            deleted_offers = res.rowcount
            return deleted_offers

    def delete_offer(self, payment_hash: bytes):
        """ Delete a received offer by payment hash. """
        s = self.received_offers.delete().where(
            self.received_offers.c.payment_hash == payment_hash
        )
        with self.get_connection() as connection:
            connection.execute(s)

    def set_received_offer_paid(self, payment_hash: bytes, paid: bool) -> None:
        """ Set a received offer is paid. """
        stmt = (
            self.received_offers.update()
            .where(self.received_offers.c.payment_hash == payment_hash)
            .values(paid=paid)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def insert_sent_payment(self, sent_payment: SentPayment):
        """ Insert a new sent payment. """
        ins = self.sent_payments.insert().values(
            peer_host=sent_payment.peer_address.host,
            peer_port=sent_payment.peer_address.port,
            squeak_hash=sent_payment.squeak_hash,
            payment_hash=sent_payment.payment_hash,
            secret_key=sent_payment.secret_key,
            price_msat=sent_payment.price_msat,
            node_pubkey=sent_payment.node_pubkey,
            valid=sent_payment.valid,
        )
        with self.get_connection() as connection:
            res = connection.execute(ins)
            sent_payment_id = res.inserted_primary_key[0]
            return sent_payment_id

    def get_sent_payments(self) -> List[SentPayment]:
        """ Get all sent payments. """
        s = (
            select([self.sent_payments])
            .order_by(
                self.sent_payments.c.created.desc(),
            )
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            sent_payments = [
                self._parse_sent_payment(row) for row in rows]
            return sent_payments

    def get_sent_payment(self, sent_payment_id: int) -> Optional[SentPayment]:
        """ Get sent payment by id. """
        s = (
            select([self.sent_payments])
            .where(self.sent_payments.c.sent_payment_id == sent_payment_id)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            return self._parse_sent_payment(row)

    def insert_sent_offer(self, sent_offer: SentOffer):
        """ Insert a new sent offer. """
        ins = self.sent_offers.insert().values(
            squeak_hash=sent_offer.squeak_hash,
            payment_hash=sent_offer.payment_hash,
            secret_key=sent_offer.secret_key,
            nonce=sent_offer.nonce,
            price_msat=sent_offer.price_msat,
            payment_request=sent_offer.payment_request,
            invoice_timestamp=sent_offer.invoice_time,
            invoice_expiry=sent_offer.invoice_expiry,
            peer_host=sent_offer.peer_address.host,
            peer_port=sent_offer.peer_address.port,
        )
        with self.get_connection() as connection:
            res = connection.execute(ins)
            sent_offer_id = res.inserted_primary_key[0]
            return sent_offer_id

    def get_sent_offers(self) -> List[SentOffer]:
        """ Get all received payments. """
        s = select([self.sent_offers]).order_by(
            self.sent_offers.c.created.desc(),
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            sent_offers = [self._parse_sent_offer(row) for row in rows]
            return sent_offers

    def get_sent_offer_by_payment_hash(self, payment_hash: bytes) -> Optional[SentOffer]:
        """ Get a sent offer by preimage hash. """
        s = select([self.sent_offers]).where(
            self.sent_offers.c.payment_hash == payment_hash
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            sent_offer = self._parse_sent_offer(row)
            return sent_offer

    def get_sent_offer_by_squeak_hash_and_peer(self, squeak_hash: bytes, peer_address: PeerAddress) -> Optional[SentOffer]:
        """
        Get a sent offer by squeak hash and peer address host. Only
        return sent offer if it's not expired and not paid.
        """
        s = (
            select([self.sent_offers])
            .where(self.sent_offers.c.squeak_hash == squeak_hash)
            .where(self.sent_offers.c.peer_host == peer_address.host)
            .where(self.sent_offer_is_not_paid)
            .where(self.sent_offer_is_not_expired)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            if row is None:
                return None
            sent_offer = self._parse_sent_offer(row)
            return sent_offer

    def delete_sent_offer(self, payment_hash: bytes):
        """ Delete a sent offer by payment hash. """
        s = self.sent_offers.delete().where(
            self.sent_offers.c.payment_hash == payment_hash
        )
        with self.get_connection() as connection:
            connection.execute(s)

    def delete_expired_sent_offers(self, interval_s):
        """
        Delete all expired sent offers. Only delete sent
        offers that have been expired for more than interval_s seconds.
        """
        s = self.sent_offers.delete().where(
            self.sent_offer_should_be_deleted(interval_s)
        )
        with self.get_connection() as connection:
            res = connection.execute(s)
            deleted_sent_offers = res.rowcount
            return deleted_sent_offers

    def set_sent_offer_paid(self, payment_hash: bytes, paid: bool) -> None:
        """ Set a sent offer is paid. """
        stmt = (
            self.sent_offers.update()
            .where(self.sent_offers.c.payment_hash == payment_hash)
            .values(paid=paid)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def get_latest_settle_index(self):
        """ Get the lnd settled index of the most recent received payment. """
        s = select(
            [func.max(self.received_payments.c.settle_index)],
        ).select_from(self.received_payments)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            latest_index = row[0]
            return latest_index

    def insert_received_payment(self, received_payment: ReceivedPayment):
        """ Insert a new received payment. """
        ins = self.received_payments.insert().values(
            squeak_hash=received_payment.squeak_hash,
            payment_hash=received_payment.payment_hash,
            price_msat=received_payment.price_msat,
            settle_index=received_payment.settle_index,
            peer_host=received_payment.peer_address.host,
            peer_port=received_payment.peer_address.port,
        )
        with self.get_connection() as connection:
            try:
                res = connection.execute(ins)
                received_payment_id = res.inserted_primary_key[0]
                return received_payment_id
            except sqlalchemy.exc.IntegrityError:
                raise DuplicateReceivedPaymentError()

    def get_received_payments(self) -> List[ReceivedPayment]:
        """ Get all received payments. """
        s = select([self.received_payments]).order_by(
            self.received_payments.c.created.desc(),
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            rows = result.fetchall()
            received_payments = [
                self._parse_received_payment(row) for row in rows]
            return received_payments

    def clear_received_payment_settle_indices(self) -> None:
        """ Set settle_index to zero for all received payments. """
        stmt = (
            self.received_payments.update()
            .values(settle_index=0)
        )
        with self.get_connection() as connection:
            connection.execute(stmt)

    def yield_received_payments_from_index(self, start_index: int = 0) -> Iterator[ReceivedPayment]:
        """ Get all received payments. """
        s = (
            select([self.received_payments])
            .order_by(
                self.received_payments.c.received_payment_id.asc(),
            )
            .where(self.received_payments.c.received_payment_id > start_index)
        )
        with self.get_connection() as connection:
            result = connection.execute(s)
            for row in result:
                received_payment = self._parse_received_payment(row)
                yield received_payment

    def get_received_payment_summary(self) -> ReceivedPaymentSummary:
        """ Get received payment summary. """
        s = select([
            func.count().label("num_payments_received"),
            func.sum(self.received_payments.c.price_msat).label(
                "total_amount_received_msat"),
        ]).select_from(self.received_payments)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            received_payment_summary = self._parse_received_payment_summary(
                row)
            return received_payment_summary

    def get_sent_payment_summary(self) -> SentPaymentSummary:
        """ Get sent payment summary. """
        s = select([
            func.count().label("num_payments_sent"),
            func.sum(self.sent_payments.c.price_msat).label(
                "total_amount_sent_msat"),
        ]).select_from(self.sent_payments)
        with self.get_connection() as connection:
            result = connection.execute(s)
            row = result.fetchone()
            sent_payment_summary = self._parse_sent_payment_summary(row)
            return sent_payment_summary

    def _parse_squeak(self, row) -> CSqueak:
        return CSqueak.deserialize(row["squeak"])

    def _parse_squeak_entry(self, row) -> SqueakEntry:
        secret_key_column = row["secret_key"]
        is_locked = bool(secret_key_column)
        reply_to = (
            row["hash_reply_sqk"]) if row["hash_reply_sqk"] else None
        liked_time = row["liked_time"]
        liked_time_s = int(liked_time.timestamp()) if liked_time else None
        profile = self._try_parse_squeak_profile(row)
        return SqueakEntry(
            squeak_hash=(row["hash"]),
            address=row["author_address"],
            block_height=row["n_block_height"],
            block_hash=(row["hash_block"]),
            block_time=row["block_time"],
            squeak_time=row["n_time"],
            reply_to=reply_to,
            is_unlocked=is_locked,
            liked_time=liked_time_s,
            content=row["content"],
            squeak_profile=profile,
        )

    def _parse_squeak_profile(self, row) -> SqueakProfile:
        private_key_column = row["private_key"]
        private_key = bytes(private_key_column) if private_key_column else None
        return SqueakProfile(
            profile_id=row["profile_id"],
            profile_name=row["profile_name"],
            private_key=private_key,
            address=row["address"],
            following=row["following"],
            use_custom_price=row["use_custom_price"],
            custom_price_msat=row["custom_price_msat"],
            profile_image=row["profile_image"],
        )

    def _try_parse_squeak_profile(self, row) -> Optional[SqueakProfile]:
        if row["profile_id"] is None:
            return None
        return self._parse_squeak_profile(row)

    def _parse_squeak_peer(self, row) -> SqueakPeer:
        return SqueakPeer(
            peer_id=row[self.peers.c.peer_id],
            peer_name=row["peer_name"],
            address=PeerAddress(
                host=row["host"],
                port=row["port"],
            ),
            autoconnect=row["autoconnect"],
        )

    def _parse_received_offer(self, row) -> ReceivedOffer:
        return ReceivedOffer(
            received_offer_id=row["received_offer_id"],
            squeak_hash=(row["squeak_hash"]),
            payment_hash=(row["payment_hash"]),
            nonce=(row["nonce"]),
            payment_point=(row["payment_point"]),
            invoice_timestamp=row["invoice_timestamp"],
            invoice_expiry=row["invoice_expiry"],
            price_msat=row["price_msat"],
            payment_request=row["payment_request"],
            destination=row["destination"],
            lightning_address=LightningAddressHostPort(
                host=row["lightning_host"],
                port=row["lightning_port"],
            ),
            peer_address=PeerAddress(
                host=row["peer_host"],
                port=row["peer_port"],
            ),
        )

    def _parse_sent_payment(self, row) -> SentPayment:
        return SentPayment(
            sent_payment_id=row["sent_payment_id"],
            created=row[self.sent_payments.c.created],
            peer_address=PeerAddress(
                host=row["peer_host"],
                port=row["peer_port"],
            ),
            squeak_hash=(row["squeak_hash"]),
            payment_hash=(row["payment_hash"]),
            secret_key=(row["secret_key"]),
            price_msat=row["price_msat"],
            node_pubkey=row["node_pubkey"],
            valid=row["valid"],
        )

    def _parse_sent_offer(self, row) -> SentOffer:
        return SentOffer(
            sent_offer_id=row["sent_offer_id"],
            squeak_hash=(row["squeak_hash"]),
            payment_hash=(row["payment_hash"]),
            secret_key=(row["secret_key"]),
            nonce=(row["nonce"]),
            price_msat=row["price_msat"],
            payment_request=row["payment_request"],
            invoice_time=row["invoice_timestamp"],
            invoice_expiry=row["invoice_expiry"],
            peer_address=PeerAddress(
                host=row["peer_host"],
                port=row["peer_port"],
            ),
        )

    def _parse_received_payment(self, row) -> ReceivedPayment:
        return ReceivedPayment(
            received_payment_id=row["received_payment_id"],
            created=row["created"],
            squeak_hash=(row["squeak_hash"]),
            payment_hash=(row["payment_hash"]),
            price_msat=row["price_msat"],
            settle_index=row["settle_index"],
            peer_address=PeerAddress(
                host=row["peer_host"],
                port=row["peer_port"],
            ),
        )

    def _parse_received_payment_summary(self, row) -> ReceivedPaymentSummary:
        return ReceivedPaymentSummary(
            num_received_payments=row["num_payments_received"],
            total_amount_received_msat=row["total_amount_received_msat"],
        )

    def _parse_sent_payment_summary(self, row) -> SentPaymentSummary:
        return SentPaymentSummary(
            num_sent_payments=row["num_payments_sent"],
            total_amount_sent_msat=row["total_amount_sent_msat"],
        )

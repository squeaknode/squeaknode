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
import datetime
import logging

from sqlalchemy import BigInteger
from sqlalchemy import Binary
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import TypeDecorator


logger = logging.getLogger(__name__)


class TZDateTime(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.timezone.utc).replace(
                tzinfo=None
            )
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value


class SLBigInteger(BigInteger):
    pass


@compiles(SLBigInteger, 'sqlite')
def bi_c_sqlite(element, compiler, **kw):
    return "INTEGER"


@compiles(SLBigInteger)
def bi_c(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)


class Models:
    def __init__(self, schema=None):
        self.schema = schema
        self.metadata = MetaData(schema=schema)

        self.squeaks = Table(
            "squeak",
            self.metadata,
            Column("hash", Binary(32), primary_key=True),
            Column("created", TZDateTime,
                   server_default=func.now(), nullable=False),
            Column("squeak", Binary, nullable=False),
            Column("hash_reply_sqk", Binary(32), nullable=True),
            Column("hash_block", Binary(32), nullable=False),
            Column("n_block_height", Integer, nullable=False),
            Column("n_time", Integer, nullable=False),
            Column("author_address", String(35), index=True, nullable=False),
            Column("secret_key", Binary(32), nullable=True),
            Column("block_time", Integer, nullable=False),
            Column("liked_time", TZDateTime,
                   default=None, nullable=True),
            Column("content", String(280), nullable=True),
        )

        self.profiles = Table(
            "profile",
            self.metadata,
            Column("profile_id", Integer, primary_key=True),
            Column("created", TZDateTime,
                   server_default=func.now(), nullable=False),
            Column("profile_name", String, unique=True, nullable=False),
            Column("private_key", Binary, nullable=True),
            Column("address", String(35), unique=True, nullable=False),
            Column("following", Boolean, nullable=False),
            Column("use_custom_price", Boolean, nullable=False, default=False),
            Column("custom_price_msat", Integer, nullable=False, default=0),
            Column("profile_image", Binary, nullable=True),
            sqlite_autoincrement=True,
        )

        self.peers = Table(
            "peer",
            self.metadata,
            Column("peer_id", Integer, primary_key=True),
            Column("created", TZDateTime,
                   server_default=func.now(), nullable=False),
            Column("peer_name", String, nullable=False),
            Column("host", String, nullable=False),
            Column("port", Integer, nullable=False),
            Column("autoconnect", Boolean, nullable=False),
            UniqueConstraint('host', 'port',
                             name='uq_peer_host_port'),
            sqlite_autoincrement=True,
        )

        self.received_offers = Table(
            "received_offer",
            self.metadata,
            Column("received_offer_id", SLBigInteger, primary_key=True),
            Column("created_time_ms", SLBigInteger, nullable=False),
            Column("squeak_hash", Binary(32), nullable=False),
            Column("payment_hash", Binary(32), unique=True, nullable=False),
            Column("nonce", Binary(32), nullable=False),
            Column("payment_point", Binary(33), nullable=False),
            Column("invoice_timestamp", Integer, nullable=False),
            Column("invoice_expiry", Integer, nullable=False),
            Column("price_msat", Integer, nullable=False),
            Column("payment_request", String, nullable=False),
            Column("destination", String(66), nullable=False),
            Column("lightning_host", String, nullable=False),
            Column("lightning_port", Integer, nullable=False),
            Column("peer_host", String, nullable=False),
            Column("peer_port", Integer, nullable=False),
            Column("paid", Boolean, nullable=False, default=False),
            sqlite_autoincrement=True,
        )

        self.sent_payments = Table(
            "sent_payment",
            self.metadata,
            Column("sent_payment_id", SLBigInteger, primary_key=True),
            Column("created_time_ms", SLBigInteger, nullable=False),
            Column("peer_host", String, nullable=False),
            Column("peer_port", Integer, nullable=False),
            Column("squeak_hash", Binary(32), nullable=False),
            Column("payment_hash", Binary(32), unique=True, nullable=False),
            Column("secret_key", Binary(32), nullable=False),
            Column("price_msat", Integer, nullable=False, default=0),
            Column("node_pubkey", String(66), nullable=False),
            Column("valid", Boolean, nullable=False),
            sqlite_autoincrement=True,
        )

        self.sent_offers = Table(
            "sent_offer",
            self.metadata,
            Column("sent_offer_id", SLBigInteger, primary_key=True),
            Column("created", TZDateTime,
                   server_default=func.now(), nullable=False),
            Column("squeak_hash", Binary(32), nullable=False),
            Column("payment_hash", Binary(32), unique=True, nullable=False),
            Column("secret_key", Binary(32), nullable=False),
            Column("nonce", Binary(32), nullable=False),
            Column("price_msat", Integer, nullable=False, default=0),
            Column("payment_request", String, nullable=False),
            Column("invoice_timestamp", Integer, nullable=False),
            Column("invoice_expiry", Integer, nullable=False),
            Column("peer_host", String, nullable=False),
            Column("peer_port", Integer, nullable=False),
            Column("paid", Boolean, nullable=False, default=False),
            sqlite_autoincrement=True,
        )

        self.received_payments = Table(
            "received_payment",
            self.metadata,
            Column("received_payment_id", SLBigInteger, primary_key=True),
            Column("created", TZDateTime,
                   server_default=func.now(), nullable=False),
            Column("squeak_hash", Binary(32), nullable=False),
            Column("payment_hash", Binary(32), unique=True, nullable=False),
            Column("price_msat", Integer, nullable=False),
            Column("settle_index", SLBigInteger, nullable=False),
            Column("peer_host", String, nullable=False),
            Column("peer_port", Integer, nullable=False),
            sqlite_autoincrement=True,
        )

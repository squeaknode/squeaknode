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
"""Remove secret_key column in sent_offers table.

Revision ID: 6ad4a9483880
Revises: 09a1001d329d
Create Date: 2021-10-11 19:32:48.666785

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import LargeBinary
from sqlalchemy.sql import column
from sqlalchemy.sql import table


# revision identifiers, used by Alembic.
revision = '6ad4a9483880'
down_revision = '09a1001d329d'
branch_labels = None
depends_on = None


FAKE_SECRET_KEY = b'\x00' * 32


def upgrade():
    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.drop_column('secret_key')


def downgrade():
    # Add the column with nullable=True.
    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('secret_key', sa.BLOB(), nullable=True))

    # Set the default value for all rows.
    sent_offers = table(
        "sent_offer",
        column("secret_key", LargeBinary(32)),
    )
    op.execute(
        sent_offers.update()
        .values(secret_key=FAKE_SECRET_KEY)
    )

    # Alter the column with nullable=False.
    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.alter_column('secret_key', nullable=False)

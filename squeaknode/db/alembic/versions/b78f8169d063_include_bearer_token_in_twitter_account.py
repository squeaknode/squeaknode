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
"""Include bearer token in twitter account.

Revision ID: b78f8169d063
Revises: b6cf462aaf7c
Create Date: 2021-12-22 13:49:11.692654

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b78f8169d063'
down_revision = 'b6cf462aaf7c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('config', schema=None) as batch_op:
        batch_op.drop_column('twitter_bearer_token')

    with op.batch_alter_table('twitter_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bearer_token', sa.String(
        ), nullable=False, server_default=sa.text("''")))


def downgrade():
    with op.batch_alter_table('twitter_account', schema=None) as batch_op:
        batch_op.drop_column('bearer_token')

    with op.batch_alter_table('config', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('twitter_bearer_token', sa.VARCHAR(), nullable=True))

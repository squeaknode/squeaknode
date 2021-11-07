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
"""Add share for free column to peers table.

Revision ID: c2d80c9fcbfa
Revises: 12d38bbf7a87
Create Date: 2021-11-07 01:07:58.170405

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c2d80c9fcbfa'
down_revision = '12d38bbf7a87'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('peer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('share_for_free', sa.Boolean(
        ), nullable=False, server_default=sa.sql.expression.false()))


def downgrade():
    with op.batch_alter_table('peer', schema=None) as batch_op:
        batch_op.drop_column('share_for_free')

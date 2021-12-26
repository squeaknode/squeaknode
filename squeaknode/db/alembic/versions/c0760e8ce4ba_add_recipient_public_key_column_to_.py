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
"""Add recipient public key column to squeaks table.

Revision ID: c0760e8ce4ba
Revises: b78f8169d063
Create Date: 2021-12-26 14:13:00.159229

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c0760e8ce4ba'
down_revision = 'b78f8169d063'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('squeak', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipient_public_key',
                                      sa.LargeBinary(length=33), nullable=True))
        batch_op.create_index(batch_op.f('ix_squeak_recipient_public_key'), [
                              'recipient_public_key'], unique=False)


def downgrade():
    with op.batch_alter_table('squeak', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_squeak_recipient_public_key'))
        batch_op.drop_column('recipient_public_key')

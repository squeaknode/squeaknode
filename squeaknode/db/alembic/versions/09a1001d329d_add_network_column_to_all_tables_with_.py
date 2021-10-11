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
"""Add network column to all tables with peer address.

Revision ID: 09a1001d329d
Revises: d7538b753a8a
Create Date: 2021-10-10 18:53:40.570906

"""
import sqlalchemy as sa
from alembic import op

from squeaknode.core.peer_address import Network


# revision identifiers, used by Alembic.
revision = '09a1001d329d'
down_revision = 'd7538b753a8a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('peer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('network', sa.String(
            length=10), nullable=False, server_default=sa.text("'{}'".format(Network.TORV3.name))))

    with op.batch_alter_table('received_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('peer_network', sa.String(
            length=10), nullable=False, server_default=sa.text("'{}'".format(Network.TORV3.name))))

    with op.batch_alter_table('received_payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('peer_network', sa.String(
            length=10), nullable=False, server_default=sa.text("'{}'".format(Network.TORV3.name))))

    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('peer_network', sa.String(
            length=10), nullable=False, server_default=sa.text("'{}'".format(Network.TORV3.name))))

    with op.batch_alter_table('sent_payment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('peer_network', sa.String(
            length=10), nullable=False, server_default=sa.text("'{}'".format(Network.TORV3.name))))


def downgrade():
    with op.batch_alter_table('sent_payment', schema=None) as batch_op:
        batch_op.drop_column('peer_network')

    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.drop_column('peer_network')

    with op.batch_alter_table('received_payment', schema=None) as batch_op:
        batch_op.drop_column('peer_network')

    with op.batch_alter_table('received_offer', schema=None) as batch_op:
        batch_op.drop_column('peer_network')

    with op.batch_alter_table('peer', schema=None) as batch_op:
        batch_op.drop_column('network')

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
"""Update squeak and profile to use new pubkey

Revision ID: cbb21be138cc
Revises: 7d807dd8d456
Create Date: 2021-12-18 14:37:27.612574

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import column
from sqlalchemy.sql import table


# revision identifiers, used by Alembic.
revision = 'cbb21be138cc'
down_revision = '7d807dd8d456'
branch_labels = None
depends_on = None


def upgrade():

    # Delete all rows from squeak table.
    squeaks = table(
        "squeak",
        column("hash", sa.LargeBinary(32)),
    )
    op.execute(
        squeaks.delete()
    )

    # Delete all rows from profile table.
    profiles = table(
        "profile",
        column("profile_id", sa.Integer),
    )
    op.execute(
        profiles.delete()
    )

    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('public_key', sa.String(length=35), nullable=False))
        batch_op.create_unique_constraint(batch_op.f(
            'uq_profile_profile_name'), ['profile_name'])
        batch_op.create_unique_constraint(batch_op.f(
            'uq_profile_public_key'), ['public_key'])
        batch_op.drop_column('address')

    with op.batch_alter_table('received_offer', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f(
            'uq_received_offer_payment_hash'), ['payment_hash'])

    with op.batch_alter_table('received_payment', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f(
            'uq_received_payment_payment_hash'), ['payment_hash'])

    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f(
            'uq_sent_offer_payment_hash'), ['payment_hash'])

    with op.batch_alter_table('sent_payment', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f(
            'uq_sent_payment_payment_hash'), ['payment_hash'])

    with op.batch_alter_table('squeak', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('reply_hash', sa.LargeBinary(length=32), nullable=True))
        batch_op.add_column(
            sa.Column('block_hash', sa.LargeBinary(length=32), nullable=False))
        batch_op.add_column(
            sa.Column('block_height', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('time_s', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('author_public_key',
                                      sa.LargeBinary(length=33), nullable=False))
        batch_op.add_column(
            sa.Column('block_time_s', sa.Integer(), nullable=False))
        batch_op.drop_index('ix_squeak_author_address')
        batch_op.create_index(batch_op.f('ix_squeak_author_public_key'), [
                              'author_public_key'], unique=False)
        batch_op.drop_column('block_time')
        batch_op.drop_column('hash_block')
        batch_op.drop_column('n_block_height')
        batch_op.drop_column('n_time')
        batch_op.drop_column('author_address')
        batch_op.drop_column('hash_reply_sqk')

    with op.batch_alter_table('twitter_account', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f(
            'uq_twitter_account_handle'), ['handle'])


def downgrade():
    with op.batch_alter_table('twitter_account', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f(
            'uq_twitter_account_handle'), type_='unique')

    with op.batch_alter_table('squeak', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('hash_reply_sqk', sa.BLOB(), nullable=True))
        batch_op.add_column(
            sa.Column('author_address', sa.VARCHAR(length=35), nullable=False))
        batch_op.add_column(sa.Column('n_time', sa.INTEGER(), nullable=False))
        batch_op.add_column(
            sa.Column('n_block_height', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('hash_block', sa.BLOB(), nullable=False))
        batch_op.add_column(
            sa.Column('block_time', sa.INTEGER(), nullable=False))
        batch_op.drop_index(batch_op.f('ix_squeak_author_public_key'))
        batch_op.create_index('ix_squeak_author_address', [
                              'author_address'], unique=False)
        batch_op.drop_column('block_time_s')
        batch_op.drop_column('author_public_key')
        batch_op.drop_column('time_s')
        batch_op.drop_column('block_height')
        batch_op.drop_column('block_hash')
        batch_op.drop_column('reply_hash')

    with op.batch_alter_table('sent_payment', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f(
            'uq_sent_payment_payment_hash'), type_='unique')

    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f(
            'uq_sent_offer_payment_hash'), type_='unique')

    with op.batch_alter_table('received_payment', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f(
            'uq_received_payment_payment_hash'), type_='unique')

    with op.batch_alter_table('received_offer', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f(
            'uq_received_offer_payment_hash'), type_='unique')

    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('address', sa.VARCHAR(length=35), nullable=False))
        batch_op.drop_constraint(batch_op.f(
            'uq_profile_public_key'), type_='unique')
        batch_op.drop_constraint(batch_op.f(
            'uq_profile_profile_name'), type_='unique')
        batch_op.drop_column('public_key')

"""Add block time column to squeak table

Revision ID: a35d180bf020
Revises: c0316d4931a5
Create Date: 2021-08-24 04:27:45.463418

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'a35d180bf020'
down_revision = 'c0316d4931a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('squeak', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('block_time', sa.Integer(), nullable=False, server_default=sa.text('0')))
        batch_op.drop_column('block_header')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('squeak', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('block_header', sa.BLOB(), nullable=False, server_default=sa.literal('')))
        batch_op.drop_column('block_time')

    # ### end Alembic commands ###

"""Rename client_host and client_port columns

Revision ID: 78b6e078848c
Revises: 7868889c72e3
Create Date: 2021-08-23 00:25:53.612711

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '78b6e078848c'
down_revision = '7868889c72e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('received_payment', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('peer_host', sa.String(), nullable=False))
        batch_op.add_column(
            sa.Column('peer_port', sa.Integer(), nullable=False))
        batch_op.drop_column('client_port')
        batch_op.drop_column('client_host')

    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('peer_host', sa.String(), nullable=False))
        batch_op.add_column(
            sa.Column('peer_port', sa.Integer(), nullable=False))
        batch_op.drop_column('client_port')
        batch_op.drop_column('client_host')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('client_host', sa.VARCHAR(), nullable=False))
        batch_op.add_column(
            sa.Column('client_port', sa.INTEGER(), nullable=False))
        batch_op.drop_column('peer_port')
        batch_op.drop_column('peer_host')

    with op.batch_alter_table('received_payment', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('client_host', sa.VARCHAR(), nullable=False))
        batch_op.add_column(
            sa.Column('client_port', sa.INTEGER(), nullable=False))
        batch_op.drop_column('peer_port')
        batch_op.drop_column('peer_host')

    # ### end Alembic commands ###

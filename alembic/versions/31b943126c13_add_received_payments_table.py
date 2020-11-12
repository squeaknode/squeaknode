"""Add received payments table

Revision ID: 31b943126c13
Revises: dc185d885f13
Create Date: 2020-11-12 01:29:19.946046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31b943126c13'
down_revision = 'dc185d885f13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('received_payment',
    sa.Column('received_payment_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('squeak_hash', sa.String(length=64), nullable=False),
    sa.Column('preimage_hash', sa.String(length=64), nullable=False),
    sa.Column('price_msat', sa.Integer(), nullable=False),
    sa.Column('settle_index', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('received_payment_id'),
    sa.UniqueConstraint('preimage_hash')
    )
    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.drop_column('settle_index')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sent_offer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('settle_index', sa.INTEGER(), nullable=True))

    op.drop_table('received_payment')
    # ### end Alembic commands ###

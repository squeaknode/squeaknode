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
"""Remove custom price per profile

Revision ID: 7d807dd8d456
Revises: 5bd8f4075339
Create Date: 2021-11-18 22:11:56.264683

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '7d807dd8d456'
down_revision = '5bd8f4075339'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('custom_price_msat')
        batch_op.drop_column('use_custom_price')


def downgrade():
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('use_custom_price',
                                      sa.BOOLEAN(), nullable=False, server_default=sa.sql.expression.false()))
        batch_op.add_column(sa.Column('custom_price_msat',
                                      sa.INTEGER(), nullable=False, server_default=sa.text("0")))

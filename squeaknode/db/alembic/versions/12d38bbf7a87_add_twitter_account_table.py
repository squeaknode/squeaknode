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
"""Add twitter account table.

Revision ID: 12d38bbf7a87
Revises: f7e2c66a9188
Create Date: 2021-11-04 02:02:25.596692

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '12d38bbf7a87'
down_revision = 'f7e2c66a9188'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('twitter_account',
                    sa.Column('twitter_account_id',
                              sa.Integer(), nullable=False),
                    sa.Column('handle', sa.String(), nullable=False),
                    sa.Column('profile_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('twitter_account_id'),
                    sa.UniqueConstraint('handle')
                    )


def downgrade():
    op.drop_table('twitter_account')

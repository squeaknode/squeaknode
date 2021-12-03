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
"""Add seed peers table

Revision ID: 044a51904e04
Revises: 7d807dd8d456
Create Date: 2021-12-02 23:42:17.394253

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '044a51904e04'
down_revision = '7d807dd8d456'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('seed_peer',
                    sa.Column('seed_peer_name', sa.String(), nullable=False),
                    sa.Column('autoconnect', sa.Boolean(), nullable=False),
                    sa.Column('share_for_free', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('seed_peer_name')
                    )


def downgrade():
    op.drop_table('seed_peer')

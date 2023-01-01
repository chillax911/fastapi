"""add content column to posts table

Revision ID: 0911e1367e8f
Revises: 7c5cb600e9ab
Create Date: 2022-12-31 07:43:24.685229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0911e1367e8f'
down_revision = '7c5cb600e9ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

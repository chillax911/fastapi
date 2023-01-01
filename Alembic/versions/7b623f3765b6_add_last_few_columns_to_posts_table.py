"""add last few columns to posts table

Revision ID: 7b623f3765b6
Revises: 58fd0f5db2fe
Create Date: 2022-12-31 13:43:49.164292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b623f3765b6'
down_revision = '58fd0f5db2fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published' , sa.Boolean()               , nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

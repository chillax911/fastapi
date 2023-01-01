"""create posts table

Revision ID: 7c5cb600e9ab
Revises: 
Create Date: 2022-12-31 07:09:30.653458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c5cb600e9ab'
down_revision = None
branch_labels = None
depends_on = None  


def upgrade() -> None:
    op.create_table('posts',sa.Column('id'      , sa.Integer() , nullable=False, primary_key=True)
                           ,sa.Column('title'   , sa.String()  , nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass

"""add foreign key to posts table

Revision ID: 58fd0f5db2fe
Revises: f0e3575df25e
Create Date: 2022-12-31 13:16:43.082650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58fd0f5db2fe'
down_revision = 'f0e3575df25e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', 
        source_table  ="posts"  , local_cols =['owner_id'], 
        referent_table="users"  , remote_cols=['id'], 
        ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

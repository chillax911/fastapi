"""add users table

Revision ID: f0e3575df25e
Revises: 0911e1367e8f
Create Date: 2022-12-31 07:49:40.048573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0e3575df25e'
down_revision = '0911e1367e8f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id'        , sa.Integer()                , nullable=False),
        sa.Column('email'     , sa.String()                 , nullable=False),
        sa.Column('password'  , sa.String()                 , nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True) , nullable=False, 
                server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

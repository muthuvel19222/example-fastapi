"""create user table

Revision ID: 08f793272ba7
Revises: 3abe4bfe2bb1
Create Date: 2023-05-11 01:32:57.545998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08f793272ba7'
down_revision = '3abe4bfe2bb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.String(), nullable=False),
                     sa.Column('email',sa.String(), nullable=False),
                     sa.Column('password',sa.String(), nullable=False),
                     sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

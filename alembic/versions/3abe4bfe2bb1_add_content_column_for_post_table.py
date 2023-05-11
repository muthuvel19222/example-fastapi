"""add content column for  post table

Revision ID: 3abe4bfe2bb1
Revises: b4c735f3e720
Create Date: 2023-05-11 01:16:30.534835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3abe4bfe2bb1'
down_revision = 'b4c735f3e720'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                    sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass

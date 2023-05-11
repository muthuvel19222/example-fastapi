"""create post table

Revision ID: b4c735f3e720
Revises: 
Create Date: 2023-05-11 01:02:57.135272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c735f3e720'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title',sa.String(), nullable=False)) #step 5
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass

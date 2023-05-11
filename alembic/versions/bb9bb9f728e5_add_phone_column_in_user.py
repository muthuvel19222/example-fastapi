"""add phone column in user

Revision ID: bb9bb9f728e5
Revises: cbbe585e5b16
Create Date: 2023-05-11 02:47:05.836064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb9bb9f728e5'
down_revision = 'cbbe585e5b16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_numer',sa.Integer(), nullable=True)) #step 5
    pass


def downgrade() -> None:
    op.drop_column('users','phone_number')
    pass

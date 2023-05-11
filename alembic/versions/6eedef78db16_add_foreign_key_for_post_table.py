"""add foreign key for post table

Revision ID: 6eedef78db16
Revises: 08f793272ba7
Create Date: 2023-05-11 01:43:56.419231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eedef78db16'
down_revision = '08f793272ba7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                    sa.Column('owner_id',sa.String(), nullable=False))
    op.create_foreign_key('post_user_fk',source_table='posts',referent_table="users",
                          local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass

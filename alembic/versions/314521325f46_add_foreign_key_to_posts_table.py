"""add foreign key to posts table

Revision ID: 314521325f46
Revises: 0dd3f8f3fddc
Create Date: 2025-03-22 08:34:27.815536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '314521325f46'
down_revision: Union[str, None] = '0dd3f8f3fddc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False)
                )
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users.fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass

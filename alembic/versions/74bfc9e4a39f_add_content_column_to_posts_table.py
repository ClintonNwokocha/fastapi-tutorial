"""add content column to posts table

Revision ID: 74bfc9e4a39f
Revises: a17c9ad77f6d
Create Date: 2025-03-22 06:26:23.846018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74bfc9e4a39f'
down_revision: Union[str, None] = 'a17c9ad77f6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass

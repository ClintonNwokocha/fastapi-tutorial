"""create users table

Revision ID: 0dd3f8f3fddc
Revises: 74bfc9e4a39f
Create Date: 2025-03-22 06:40:29.375343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dd3f8f3fddc'
down_revision: Union[str, None] = '74bfc9e4a39f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
        )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass

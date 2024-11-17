"""add content to posts table

Revision ID: 8be9cff286d8
Revises: 405dd80c38e2
Create Date: 2024-11-17 20:30:41.721493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8be9cff286d8'
down_revision: Union[str, None] = '405dd80c38e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass

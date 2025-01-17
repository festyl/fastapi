"""Create posts table

Revision ID: 46fcba87c670
Revises: 
Create Date: 2024-11-17 13:13:02.680189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46fcba87c670'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, primary_key=True, nullable=False), sa.Column("title", sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass

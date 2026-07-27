"""create transformations table

Revision ID: 0001
Revises:
Create Date: 2026-07-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    op.create_table(
        "transformation",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("original_text", sa.String(), nullable=False),
        sa.Column("transformed_text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("transformation")

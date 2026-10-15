"""

Revision ID: 3fe222515271
Revises:
Create Date: 2026-10-13 12:58:33.844477

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3fe222515271"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "division",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("division_name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "search_query",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("division_id", sa.Integer(), nullable=False),
        sa.Column("search_queries", postgresql.ARRAY(sa.String()), nullable=False),
        sa.ForeignKeyConstraint(
            ["division_id"],
            ["division.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_search_query_division_id"),
        "search_query",
        ["division_id"],
        unique=False,
    )

    op.create_table(
        "tender",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("division_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("city", sa.String(length=255), nullable=True),
        sa.Column("estimated_price", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("application_deadline", sa.DateTime(), nullable=True),
        sa.Column("contract_deadline", sa.DateTime(), nullable=True),
        sa.Column("summary_deadline", sa.DateTime(), nullable=True),
        sa.Column("platform_url", sa.String(length=500), nullable=True),
        sa.Column("scoring", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["division_id"],
            ["division.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tender_division_id"),
        "tender",
        ["division_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_tender_division_id"), table_name="tender")
    op.drop_table("tender")

    op.drop_index(op.f("ix_search_query_division_id"), table_name="search_query")
    op.drop_table("search_query")

    op.drop_table("division")

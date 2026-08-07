"""Add source metadata and shot attributes for Match Lab.

Revision ID: 20260807_0002
Revises: 20260726_0001
Create Date: 2026-08-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260807_0002"
down_revision: str | None = "20260726_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "matches",
        sa.Column("source_match_id", sa.String(length=40), nullable=True),
    )
    op.create_index(
        "ix_matches_source_match_id",
        "matches",
        ["source_match_id"],
        unique=True,
    )

    op.add_column(
        "match_events",
        sa.Column("source_event_id", sa.String(length=40), nullable=True),
    )
    op.add_column(
        "match_events",
        sa.Column("player_name", sa.String(length=140), nullable=True),
    )
    op.add_column(
        "match_events",
        sa.Column("period", sa.Integer(), nullable=False, server_default="1"),
    )
    op.add_column(
        "match_events",
        sa.Column("xg", sa.Float(), nullable=True),
    )
    op.add_column(
        "match_events",
        sa.Column("body_part", sa.String(length=40), nullable=True),
    )
    op.add_column(
        "match_events",
        sa.Column("shot_type", sa.String(length=40), nullable=True),
    )
    op.add_column(
        "match_events",
        sa.Column("play_pattern", sa.String(length=80), nullable=True),
    )
    op.create_index(
        "ix_match_events_source_event_id",
        "match_events",
        ["source_event_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_match_events_source_event_id", table_name="match_events")
    op.drop_column("match_events", "play_pattern")
    op.drop_column("match_events", "shot_type")
    op.drop_column("match_events", "body_part")
    op.drop_column("match_events", "xg")
    op.drop_column("match_events", "period")
    op.drop_column("match_events", "player_name")
    op.drop_column("match_events", "source_event_id")

    op.drop_index("ix_matches_source_match_id", table_name="matches")
    op.drop_column("matches", "source_match_id")

"""Persist Agent runs for notebook history and follow-up reports.

Revision ID: 20260808_0003
Revises: 20260807_0002
Create Date: 2026-08-08
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260808_0003"
down_revision: str | None = "20260807_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("run_id", sa.String(length=32), nullable=False),
        sa.Column("parent_run_id", sa.String(length=32), nullable=True),
        sa.Column("follow_up_depth", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("season", sa.String(length=9), nullable=False),
        sa.Column("requested_focus", sa.String(length=20), nullable=False),
        sa.Column("resolved_focus", sa.String(length=20), nullable=False),
        sa.Column("player_a_slug", sa.String(length=140), nullable=False),
        sa.Column("player_b_slug", sa.String(length=140), nullable=False),
        sa.Column("winner_slug", sa.String(length=140), nullable=False),
        sa.Column("generation_mode", sa.String(length=24), nullable=False),
        sa.Column("result_snapshot", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_run_id"],
            ["agent_runs.run_id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_agent_runs_created_at",
        "agent_runs",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        "ix_agent_runs_created_at_id",
        "agent_runs",
        ["created_at", "id"],
        unique=False,
    )
    op.create_index(
        "ix_agent_runs_generation_mode",
        "agent_runs",
        ["generation_mode"],
        unique=False,
    )
    op.create_index(
        "ix_agent_runs_parent_run_id",
        "agent_runs",
        ["parent_run_id"],
        unique=False,
    )
    op.create_index(
        "ix_agent_runs_resolved_focus",
        "agent_runs",
        ["resolved_focus"],
        unique=False,
    )
    op.create_index(
        "ix_agent_runs_run_id",
        "agent_runs",
        ["run_id"],
        unique=True,
    )
    op.create_index(
        "ix_agent_runs_season",
        "agent_runs",
        ["season"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_agent_runs_season", table_name="agent_runs")
    op.drop_index("ix_agent_runs_run_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_resolved_focus", table_name="agent_runs")
    op.drop_index("ix_agent_runs_parent_run_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_generation_mode", table_name="agent_runs")
    op.drop_index("ix_agent_runs_created_at_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_created_at", table_name="agent_runs")
    op.drop_table("agent_runs")

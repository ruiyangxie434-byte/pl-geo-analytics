from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"
    __table_args__ = (
        Index("ix_agent_runs_created_at_id", "created_at", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
    )
    parent_run_id: Mapped[str | None] = mapped_column(
        ForeignKey("agent_runs.run_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    follow_up_depth: Mapped[int] = mapped_column(Integer, default=0)
    question: Mapped[str] = mapped_column(Text)
    season: Mapped[str] = mapped_column(String(9), index=True)
    requested_focus: Mapped[str] = mapped_column(String(20))
    resolved_focus: Mapped[str] = mapped_column(String(20), index=True)
    player_a_slug: Mapped[str] = mapped_column(String(140))
    player_b_slug: Mapped[str] = mapped_column(String(140))
    winner_slug: Mapped[str] = mapped_column(String(140))
    generation_mode: Mapped[str] = mapped_column(String(24), index=True)
    result_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

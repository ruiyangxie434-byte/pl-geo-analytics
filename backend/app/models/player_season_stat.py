from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.player import Player


class PlayerSeasonStat(Base):
    __tablename__ = "player_season_stats"
    __table_args__ = (
        UniqueConstraint(
            "player_id",
            "season",
            name="uq_player_season_stats_player_season",
        ),
        Index("ix_player_season_stats_season_minutes", "season", "minutes"),
        CheckConstraint("minutes >= 0", name="ck_player_stats_minutes"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"),
        index=True,
    )
    season: Mapped[str] = mapped_column(String(9), index=True)
    appearances: Mapped[int] = mapped_column(Integer, default=0)
    starts: Mapped[int] = mapped_column(Integer, default=0)
    minutes: Mapped[int] = mapped_column(Integer, default=0)
    goals: Mapped[int] = mapped_column(Integer, default=0)
    assists: Mapped[int] = mapped_column(Integer, default=0)
    shots: Mapped[int] = mapped_column(Integer, default=0)
    key_passes: Mapped[int] = mapped_column(Integer, default=0)
    tackles: Mapped[int] = mapped_column(Integer, default=0)
    interceptions: Mapped[int] = mapped_column(Integer, default=0)
    expected_goals: Mapped[float | None] = mapped_column(Float, nullable=True)
    source_kind: Mapped[str] = mapped_column(
        String(20),
        default="sample",
        index=True,
    )

    player: Mapped["Player"] = relationship(back_populates="season_stats")

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.match import Match
    from app.models.player import Player


class MatchEvent(Base):
    __tablename__ = "match_events"
    __table_args__ = (
        Index("ix_match_events_match_time", "match_id", "minute", "second"),
        CheckConstraint("minute >= 0", name="ck_match_events_minute"),
        CheckConstraint(
            "period BETWEEN 1 AND 5",
            name="ck_match_events_period",
        ),
        CheckConstraint("second BETWEEN 0 AND 59", name="ck_match_events_second"),
        CheckConstraint("x IS NULL OR x BETWEEN 0 AND 100", name="ck_match_events_x"),
        CheckConstraint("y IS NULL OR y BETWEEN 0 AND 100", name="ck_match_events_y"),
        CheckConstraint(
            "xg IS NULL OR xg BETWEEN 0 AND 1",
            name="ck_match_events_xg",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_event_id: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
        unique=True,
        index=True,
    )
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id", ondelete="CASCADE"),
        index=True,
    )
    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id", ondelete="RESTRICT"),
        index=True,
    )
    player_id: Mapped[int | None] = mapped_column(
        ForeignKey("players.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    player_name: Mapped[str | None] = mapped_column(String(140), nullable=True)
    period: Mapped[int] = mapped_column(Integer, default=1)
    minute: Mapped[int] = mapped_column(Integer)
    second: Mapped[int] = mapped_column(Integer, default=0)
    event_type: Mapped[str] = mapped_column(String(40), index=True)
    outcome: Mapped[str | None] = mapped_column(String(40), nullable=True)
    x: Mapped[float | None] = mapped_column(Float, nullable=True)
    y: Mapped[float | None] = mapped_column(Float, nullable=True)
    xg: Mapped[float | None] = mapped_column(Float, nullable=True)
    body_part: Mapped[str | None] = mapped_column(String(40), nullable=True)
    shot_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    play_pattern: Mapped[str | None] = mapped_column(String(80), nullable=True)
    source_kind: Mapped[str] = mapped_column(
        String(20),
        default="sample",
        index=True,
    )

    match: Mapped["Match"] = relationship(back_populates="events")
    club: Mapped["Club"] = relationship()
    player: Mapped["Player | None"] = relationship(back_populates="match_events")

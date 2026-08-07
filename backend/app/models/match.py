from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.match_event import MatchEvent


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint(
            "season",
            "matchweek",
            "home_club_id",
            "away_club_id",
            name="uq_matches_fixture",
        ),
        Index("ix_matches_season_kickoff", "season", "kickoff_at"),
        CheckConstraint(
            "home_club_id <> away_club_id",
            name="ck_matches_distinct_clubs",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_match_id: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
        unique=True,
        index=True,
    )
    season: Mapped[str] = mapped_column(String(9), index=True)
    matchweek: Mapped[int] = mapped_column(Integer)
    kickoff_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    home_club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id", ondelete="RESTRICT"),
        index=True,
    )
    away_club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id", ondelete="RESTRICT"),
        index=True,
    )
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    venue: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(20), default="scheduled")
    source_kind: Mapped[str] = mapped_column(
        String(20),
        default="sample",
        index=True,
    )

    home_club: Mapped["Club"] = relationship(
        back_populates="home_matches",
        foreign_keys=[home_club_id],
    )
    away_club: Mapped["Club"] = relationship(
        back_populates="away_matches",
        foreign_keys=[away_club_id],
    )
    events: Mapped[list["MatchEvent"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan",
    )

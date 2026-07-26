from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
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


class Standing(Base):
    __tablename__ = "standings"
    __table_args__ = (
        UniqueConstraint("club_id", "season", name="uq_standings_club_season"),
        Index("ix_standings_season_position", "season", "position"),
        CheckConstraint("played >= 0", name="ck_standings_played"),
        CheckConstraint("points >= 0", name="ck_standings_points"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id", ondelete="CASCADE"),
        index=True,
    )
    season: Mapped[str] = mapped_column(String(9), index=True)
    position: Mapped[int] = mapped_column(Integer)
    played: Mapped[int] = mapped_column(Integer)
    won: Mapped[int] = mapped_column(Integer)
    drawn: Mapped[int] = mapped_column(Integer)
    lost: Mapped[int] = mapped_column(Integer)
    goals_for: Mapped[int] = mapped_column(Integer)
    goals_against: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    source_kind: Mapped[str] = mapped_column(
        String(20),
        default="sample",
        index=True,
    )

    club: Mapped["Club"] = relationship(back_populates="standings")

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Float, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.match import Match
    from app.models.player import Player
    from app.models.standing import Standing


class Club(Base):
    __tablename__ = "clubs"
    __table_args__ = (
        CheckConstraint(
            "stadium_latitude BETWEEN -90 AND 90",
            name="ck_clubs_latitude",
        ),
        CheckConstraint(
            "stadium_longitude BETWEEN -180 AND 180",
            name="ck_clubs_longitude",
        ),
        Index("ix_clubs_city", "city"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    short_name: Mapped[str] = mapped_column(String(40))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    city: Mapped[str] = mapped_column(String(80))
    stadium_name: Mapped[str] = mapped_column(String(120))
    stadium_latitude: Mapped[float] = mapped_column(Float)
    stadium_longitude: Mapped[float] = mapped_column(Float)
    founded_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    primary_color: Mapped[str] = mapped_column(String(7), default="#48e5a4")
    source_kind: Mapped[str] = mapped_column(
        String(20),
        default="sample",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    players: Mapped[list["Player"]] = relationship(
        back_populates="club",
        cascade="all, delete-orphan",
    )
    standings: Mapped[list["Standing"]] = relationship(
        back_populates="club",
        cascade="all, delete-orphan",
    )
    home_matches: Mapped[list["Match"]] = relationship(
        back_populates="home_club",
        foreign_keys="Match.home_club_id",
    )
    away_matches: Mapped[list["Match"]] = relationship(
        back_populates="away_club",
        foreign_keys="Match.away_club_id",
    )

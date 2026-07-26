"""Create the initial football data schema.

Revision ID: 20260726_0001
Revises:
Create Date: 2026-07-26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260726_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "clubs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("short_name", sa.String(length=40), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=80), nullable=False),
        sa.Column("stadium_name", sa.String(length=120), nullable=False),
        sa.Column("stadium_latitude", sa.Float(), nullable=False),
        sa.Column("stadium_longitude", sa.Float(), nullable=False),
        sa.Column("founded_year", sa.Integer(), nullable=True),
        sa.Column("primary_color", sa.String(length=7), nullable=False),
        sa.Column("source_kind", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "stadium_latitude BETWEEN -90 AND 90",
            name="ck_clubs_latitude",
        ),
        sa.CheckConstraint(
            "stadium_longitude BETWEEN -180 AND 180",
            name="ck_clubs_longitude",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_clubs_city", "clubs", ["city"], unique=False)
    op.create_index("ix_clubs_name", "clubs", ["name"], unique=True)
    op.create_index("ix_clubs_slug", "clubs", ["slug"], unique=True)
    op.create_index("ix_clubs_source_kind", "clubs", ["source_kind"], unique=False)

    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("club_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=140), nullable=False),
        sa.Column("shirt_number", sa.Integer(), nullable=True),
        sa.Column("position", sa.String(length=20), nullable=False),
        sa.Column("nationality", sa.String(length=80), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("source_kind", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "club_id",
            "shirt_number",
            name="uq_players_club_shirt",
        ),
    )
    op.create_index("ix_players_club_id", "players", ["club_id"], unique=False)
    op.create_index(
        "ix_players_club_position",
        "players",
        ["club_id", "position"],
        unique=False,
    )
    op.create_index("ix_players_full_name", "players", ["full_name"], unique=False)
    op.create_index("ix_players_position", "players", ["position"], unique=False)
    op.create_index("ix_players_slug", "players", ["slug"], unique=True)
    op.create_index("ix_players_source_kind", "players", ["source_kind"], unique=False)

    op.create_table(
        "standings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("club_id", sa.Integer(), nullable=False),
        sa.Column("season", sa.String(length=9), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("played", sa.Integer(), nullable=False),
        sa.Column("won", sa.Integer(), nullable=False),
        sa.Column("drawn", sa.Integer(), nullable=False),
        sa.Column("lost", sa.Integer(), nullable=False),
        sa.Column("goals_for", sa.Integer(), nullable=False),
        sa.Column("goals_against", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("source_kind", sa.String(length=20), nullable=False),
        sa.CheckConstraint("played >= 0", name="ck_standings_played"),
        sa.CheckConstraint("points >= 0", name="ck_standings_points"),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "club_id",
            "season",
            name="uq_standings_club_season",
        ),
    )
    op.create_index("ix_standings_club_id", "standings", ["club_id"], unique=False)
    op.create_index("ix_standings_season", "standings", ["season"], unique=False)
    op.create_index(
        "ix_standings_season_position",
        "standings",
        ["season", "position"],
        unique=False,
    )
    op.create_index(
        "ix_standings_source_kind",
        "standings",
        ["source_kind"],
        unique=False,
    )

    op.create_table(
        "player_season_stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("season", sa.String(length=9), nullable=False),
        sa.Column("appearances", sa.Integer(), nullable=False),
        sa.Column("starts", sa.Integer(), nullable=False),
        sa.Column("minutes", sa.Integer(), nullable=False),
        sa.Column("goals", sa.Integer(), nullable=False),
        sa.Column("assists", sa.Integer(), nullable=False),
        sa.Column("shots", sa.Integer(), nullable=False),
        sa.Column("key_passes", sa.Integer(), nullable=False),
        sa.Column("tackles", sa.Integer(), nullable=False),
        sa.Column("interceptions", sa.Integer(), nullable=False),
        sa.Column("expected_goals", sa.Float(), nullable=True),
        sa.Column("source_kind", sa.String(length=20), nullable=False),
        sa.CheckConstraint("minutes >= 0", name="ck_player_stats_minutes"),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["players.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "player_id",
            "season",
            name="uq_player_season_stats_player_season",
        ),
    )
    op.create_index(
        "ix_player_season_stats_player_id",
        "player_season_stats",
        ["player_id"],
        unique=False,
    )
    op.create_index(
        "ix_player_season_stats_season",
        "player_season_stats",
        ["season"],
        unique=False,
    )
    op.create_index(
        "ix_player_season_stats_season_minutes",
        "player_season_stats",
        ["season", "minutes"],
        unique=False,
    )
    op.create_index(
        "ix_player_season_stats_source_kind",
        "player_season_stats",
        ["source_kind"],
        unique=False,
    )

    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("season", sa.String(length=9), nullable=False),
        sa.Column("matchweek", sa.Integer(), nullable=False),
        sa.Column("kickoff_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("home_club_id", sa.Integer(), nullable=False),
        sa.Column("away_club_id", sa.Integer(), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("venue", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("source_kind", sa.String(length=20), nullable=False),
        sa.CheckConstraint(
            "home_club_id <> away_club_id",
            name="ck_matches_distinct_clubs",
        ),
        sa.ForeignKeyConstraint(
            ["away_club_id"],
            ["clubs.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["home_club_id"],
            ["clubs.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "season",
            "matchweek",
            "home_club_id",
            "away_club_id",
            name="uq_matches_fixture",
        ),
    )
    op.create_index("ix_matches_away_club_id", "matches", ["away_club_id"], unique=False)
    op.create_index("ix_matches_home_club_id", "matches", ["home_club_id"], unique=False)
    op.create_index("ix_matches_season", "matches", ["season"], unique=False)
    op.create_index(
        "ix_matches_season_kickoff",
        "matches",
        ["season", "kickoff_at"],
        unique=False,
    )
    op.create_index("ix_matches_source_kind", "matches", ["source_kind"], unique=False)

    op.create_table(
        "match_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("club_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("minute", sa.Integer(), nullable=False),
        sa.Column("second", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=40), nullable=False),
        sa.Column("outcome", sa.String(length=40), nullable=True),
        sa.Column("x", sa.Float(), nullable=True),
        sa.Column("y", sa.Float(), nullable=True),
        sa.Column("source_kind", sa.String(length=20), nullable=False),
        sa.CheckConstraint("minute >= 0", name="ck_match_events_minute"),
        sa.CheckConstraint(
            "second BETWEEN 0 AND 59",
            name="ck_match_events_second",
        ),
        sa.CheckConstraint(
            "x IS NULL OR x BETWEEN 0 AND 100",
            name="ck_match_events_x",
        ),
        sa.CheckConstraint(
            "y IS NULL OR y BETWEEN 0 AND 100",
            name="ck_match_events_y",
        ),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["player_id"], ["players.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_match_events_club_id", "match_events", ["club_id"], unique=False)
    op.create_index(
        "ix_match_events_event_type",
        "match_events",
        ["event_type"],
        unique=False,
    )
    op.create_index("ix_match_events_match_id", "match_events", ["match_id"], unique=False)
    op.create_index(
        "ix_match_events_match_time",
        "match_events",
        ["match_id", "minute", "second"],
        unique=False,
    )
    op.create_index(
        "ix_match_events_player_id",
        "match_events",
        ["player_id"],
        unique=False,
    )
    op.create_index(
        "ix_match_events_source_kind",
        "match_events",
        ["source_kind"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_match_events_source_kind", table_name="match_events")
    op.drop_index("ix_match_events_player_id", table_name="match_events")
    op.drop_index("ix_match_events_match_time", table_name="match_events")
    op.drop_index("ix_match_events_match_id", table_name="match_events")
    op.drop_index("ix_match_events_event_type", table_name="match_events")
    op.drop_index("ix_match_events_club_id", table_name="match_events")
    op.drop_table("match_events")

    op.drop_index("ix_matches_source_kind", table_name="matches")
    op.drop_index("ix_matches_season_kickoff", table_name="matches")
    op.drop_index("ix_matches_season", table_name="matches")
    op.drop_index("ix_matches_home_club_id", table_name="matches")
    op.drop_index("ix_matches_away_club_id", table_name="matches")
    op.drop_table("matches")

    op.drop_index(
        "ix_player_season_stats_source_kind",
        table_name="player_season_stats",
    )
    op.drop_index(
        "ix_player_season_stats_season_minutes",
        table_name="player_season_stats",
    )
    op.drop_index(
        "ix_player_season_stats_season",
        table_name="player_season_stats",
    )
    op.drop_index(
        "ix_player_season_stats_player_id",
        table_name="player_season_stats",
    )
    op.drop_table("player_season_stats")

    op.drop_index("ix_standings_source_kind", table_name="standings")
    op.drop_index("ix_standings_season_position", table_name="standings")
    op.drop_index("ix_standings_season", table_name="standings")
    op.drop_index("ix_standings_club_id", table_name="standings")
    op.drop_table("standings")

    op.drop_index("ix_players_source_kind", table_name="players")
    op.drop_index("ix_players_slug", table_name="players")
    op.drop_index("ix_players_position", table_name="players")
    op.drop_index("ix_players_full_name", table_name="players")
    op.drop_index("ix_players_club_position", table_name="players")
    op.drop_index("ix_players_club_id", table_name="players")
    op.drop_table("players")

    op.drop_index("ix_clubs_source_kind", table_name="clubs")
    op.drop_index("ix_clubs_slug", table_name="clubs")
    op.drop_index("ix_clubs_name", table_name="clubs")
    op.drop_index("ix_clubs_city", table_name="clubs")
    op.drop_table("clubs")

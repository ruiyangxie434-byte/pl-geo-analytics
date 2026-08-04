from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Player, PlayerSeasonStat


PER90_METRIC_KEYS = (
    "goals_per90",
    "assists_per90",
    "shots_per90",
    "key_passes_per90",
    "tackles_per90",
    "interceptions_per90",
    "expected_goals_per90",
)


@dataclass(frozen=True)
class PlayerSnapshot:
    player: Player
    stats: PlayerSeasonStat
    per90: dict[str, float]


def per90(value: int | float | None, minutes: int) -> float:
    if minutes <= 0 or value is None:
        return 0.0
    return round(float(value) * 90 / minutes, 2)


def calculate_per90(stats: PlayerSeasonStat) -> dict[str, float]:
    return {
        "goals_per90": per90(stats.goals, stats.minutes),
        "assists_per90": per90(stats.assists, stats.minutes),
        "shots_per90": per90(stats.shots, stats.minutes),
        "key_passes_per90": per90(stats.key_passes, stats.minutes),
        "tackles_per90": per90(stats.tackles, stats.minutes),
        "interceptions_per90": per90(stats.interceptions, stats.minutes),
        "expected_goals_per90": per90(
            stats.expected_goals,
            stats.minutes,
        ),
    }


def load_player_snapshots(
    db: Session,
    season: str,
    minimum_minutes: int = 1,
) -> list[PlayerSnapshot]:
    players = db.scalars(
        select(Player)
        .options(
            selectinload(Player.club),
            selectinload(Player.season_stats),
        )
        .order_by(Player.full_name)
    ).all()

    snapshots: list[PlayerSnapshot] = []
    for player in players:
        stats = next(
            (item for item in player.season_stats if item.season == season),
            None,
        )
        if stats is not None and stats.minutes >= minimum_minutes:
            snapshots.append(
                PlayerSnapshot(
                    player=player,
                    stats=stats,
                    per90=calculate_per90(stats),
                )
            )
    return snapshots


def percentile_rank(value: float, population: list[float]) -> int:
    if not population:
        return 0
    below_or_equal = sum(item <= value for item in population)
    return round(below_or_equal / len(population) * 100)

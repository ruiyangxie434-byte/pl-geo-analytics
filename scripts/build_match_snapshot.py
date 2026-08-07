#!/usr/bin/env python3
"""Build a compact, reproducible shot snapshot from StatsBomb Open Data.

The runtime API reads the generated JSON from ``data/processed`` and never
downloads data while the app is running.  This script keeps the source fields,
coordinate conversion and attribution explicit so the demo can be rebuilt.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

STATSBOMB_REPOSITORY = "https://github.com/hudl/open-data"
STATSBOMB_LICENSE = f"{STATSBOMB_REPOSITORY}/blob/master/LICENSE.pdf"
MATCH_ID = "3749448"
MATCHES_URL = (
    f"{STATSBOMB_REPOSITORY}/raw/refs/heads/master/data/matches/2/44.json"
)
EVENTS_URL = (
    f"{STATSBOMB_REPOSITORY}/raw/refs/heads/master/data/events/{MATCH_ID}.json"
)


def read_json(source: str) -> Any:
    if source.startswith(("https://", "http://")):
        with urlopen(source, timeout=30) as response:  # noqa: S310
            return json.load(response)
    with Path(source).open(encoding="utf-8") as handle:
        return json.load(handle)


def slugify_team(name: str) -> str:
    return name.casefold().replace(" ", "-")


def season_key(season_name: str) -> str:
    start, end = season_name.split("/", maxsplit=1)
    return f"{start}-{end[-2:]}"


def normalize_location(location: list[float]) -> tuple[float, float]:
    if len(location) < 2:
        raise ValueError("Shot location must contain x and y coordinates")
    x, y = float(location[0]), float(location[1])
    if not 0 <= x <= 120 or not 0 <= y <= 80:
        raise ValueError(f"Unexpected StatsBomb location: {location}")
    return round(x / 120 * 100, 4), round(y / 80 * 100, 4)


def build_snapshot(
    matches: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    match = next(
        (item for item in matches if str(item["match_id"]) == MATCH_ID),
        None,
    )
    if match is None:
        raise ValueError(f"Match {MATCH_ID} was not found in the match file")

    home_name = match["home_team"]["home_team_name"]
    away_name = match["away_team"]["away_team_name"]
    team_names = {home_name, away_name}
    shots: list[dict[str, Any]] = []

    for event in events:
        if event.get("type", {}).get("name") != "Shot":
            continue
        team_name = event["team"]["name"]
        if team_name not in team_names:
            raise ValueError(f"Unexpected shot team: {team_name}")
        x, y = normalize_location(event["location"])
        shot = event["shot"]
        shots.append(
            {
                "source_event_id": event["id"],
                "period": event["period"],
                "minute": event["minute"],
                "second": event["second"],
                "team_name": team_name,
                "team_slug": slugify_team(team_name),
                "player_name": event.get("player", {}).get("name"),
                "outcome": shot["outcome"]["name"],
                "x": x,
                "y": y,
                "xg": round(float(shot["statsbomb_xg"]), 6),
                "body_part": shot.get("body_part", {}).get("name"),
                "shot_type": shot.get("type", {}).get("name"),
                "play_pattern": event.get("play_pattern", {}).get("name"),
            }
        )

    shots.sort(
        key=lambda item: (
            item["minute"],
            item["second"],
            item["source_event_id"],
        )
    )
    if len(shots) != 28:
        raise ValueError(f"Expected 28 shots for {MATCH_ID}, found {len(shots)}")

    team_totals = {}
    for team_name in (home_name, away_name):
        team_shots = [shot for shot in shots if shot["team_name"] == team_name]
        team_totals[slugify_team(team_name)] = {
            "shots": len(team_shots),
            "goals": sum(shot["outcome"] == "Goal" for shot in team_shots),
            "xg": round(sum(shot["xg"] for shot in team_shots), 3),
        }

    return {
        "schema_version": 1,
        "source": {
            "name": "StatsBomb Open Data",
            "repository_url": STATSBOMB_REPOSITORY,
            "match_url": MATCHES_URL,
            "events_url": EVENTS_URL,
            "license_url": STATSBOMB_LICENSE,
            "source_last_updated": match["last_updated"],
        },
        "coordinate_system": {
            "source": "StatsBomb 120 x 80",
            "stored": "normalized 0-100 x 0-100",
            "formula": "x / 120 * 100; y / 80 * 100",
        },
        "match": {
            "source_match_id": MATCH_ID,
            "competition": match["competition"]["competition_name"],
            "season": season_key(match["season"]["season_name"]),
            "season_label": match["season"]["season_name"],
            "matchweek": match["match_week"],
            "match_date": match["match_date"],
            "kick_off": match["kick_off"],
            "home_team": home_name,
            "away_team": away_name,
            "home_score": match["home_score"],
            "away_score": match["away_score"],
            "venue": match["stadium"]["name"],
            "status": "completed",
        },
        "team_totals": team_totals,
        "shots": shots,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--matches",
        default=MATCHES_URL,
        help="Match-list JSON path or URL",
    )
    parser.add_argument(
        "--events",
        default=EVENTS_URL,
        help="Event JSON path or URL",
    )
    parser.add_argument(
        "--output",
        default="data/processed/statsbomb_match_3749448.json",
        help="Output JSON path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    snapshot = build_snapshot(read_json(args.matches), read_json(args.events))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {len(snapshot['shots'])} shots for match {MATCH_ID} to {output}"
    )


if __name__ == "__main__":
    main()

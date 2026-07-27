from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Club, Player, PlayerSeasonStat, Standing

SAMPLE_SEASON = "2024-25"

CLUBS = [
    {
        "name": "Liverpool",
        "short_name": "Liverpool",
        "slug": "liverpool",
        "city": "Liverpool",
        "stadium_name": "Anfield",
        "stadium_latitude": 53.4308,
        "stadium_longitude": -2.9608,
        "founded_year": 1892,
        "primary_color": "#c8102e",
    },
    {
        "name": "Arsenal",
        "short_name": "Arsenal",
        "slug": "arsenal",
        "city": "London",
        "stadium_name": "Emirates Stadium",
        "stadium_latitude": 51.5549,
        "stadium_longitude": -0.1084,
        "founded_year": 1886,
        "primary_color": "#ef0107",
    },
    {
        "name": "Manchester City",
        "short_name": "Man City",
        "slug": "manchester-city",
        "city": "Manchester",
        "stadium_name": "Etihad Stadium",
        "stadium_latitude": 53.4831,
        "stadium_longitude": -2.2004,
        "founded_year": 1880,
        "primary_color": "#6cabdd",
    },
    {
        "name": "Chelsea",
        "short_name": "Chelsea",
        "slug": "chelsea",
        "city": "London",
        "stadium_name": "Stamford Bridge",
        "stadium_latitude": 51.4817,
        "stadium_longitude": -0.1910,
        "founded_year": 1905,
        "primary_color": "#034694",
    },
    {
        "name": "Newcastle United",
        "short_name": "Newcastle",
        "slug": "newcastle-united",
        "city": "Newcastle upon Tyne",
        "stadium_name": "St James' Park",
        "stadium_latitude": 54.9752,
        "stadium_longitude": -1.6224,
        "founded_year": 1892,
        "primary_color": "#f1be48",
    },
    {
        "name": "Aston Villa",
        "short_name": "Aston Villa",
        "slug": "aston-villa",
        "city": "Birmingham",
        "stadium_name": "Villa Park",
        "stadium_latitude": 52.5085,
        "stadium_longitude": -1.8849,
        "founded_year": 1874,
        "primary_color": "#95bfe5",
    },
]

STANDINGS = {
    "liverpool": {
        "position": 1,
        "played": 38,
        "won": 25,
        "drawn": 9,
        "lost": 4,
        "goals_for": 86,
        "goals_against": 41,
        "points": 84,
    },
    "arsenal": {
        "position": 2,
        "played": 38,
        "won": 20,
        "drawn": 14,
        "lost": 4,
        "goals_for": 69,
        "goals_against": 34,
        "points": 74,
    },
    "manchester-city": {
        "position": 3,
        "played": 38,
        "won": 21,
        "drawn": 8,
        "lost": 9,
        "goals_for": 72,
        "goals_against": 44,
        "points": 71,
    },
    "chelsea": {
        "position": 4,
        "played": 38,
        "won": 20,
        "drawn": 9,
        "lost": 9,
        "goals_for": 64,
        "goals_against": 43,
        "points": 69,
    },
    "newcastle-united": {
        "position": 5,
        "played": 38,
        "won": 20,
        "drawn": 6,
        "lost": 12,
        "goals_for": 68,
        "goals_against": 47,
        "points": 66,
    },
    "aston-villa": {
        "position": 6,
        "played": 38,
        "won": 19,
        "drawn": 9,
        "lost": 10,
        "goals_for": 58,
        "goals_against": 51,
        "points": 66,
    },
}

PLAYERS = {
    "liverpool": [
        {
            "full_name": "Mohamed Salah",
            "slug": "mohamed-salah",
            "shirt_number": 11,
            "position": "FWD",
            "nationality": "Egypt",
            "date_of_birth": date(1992, 6, 15),
            "stats": {
                "appearances": 38,
                "starts": 38,
                "minutes": 3378,
                "goals": 29,
                "assists": 18,
                "shots": 130,
                "key_passes": 88,
                "tackles": 19,
                "interceptions": 4,
                "expected_goals": 25.2,
            },
        },
        {
            "full_name": "Virgil van Dijk",
            "slug": "virgil-van-dijk",
            "shirt_number": 4,
            "position": "DEF",
            "nationality": "Netherlands",
            "date_of_birth": date(1991, 7, 8),
            "stats": {
                "appearances": 37,
                "starts": 37,
                "minutes": 3330,
                "goals": 3,
                "assists": 1,
                "shots": 27,
                "key_passes": 10,
                "tackles": 36,
                "interceptions": 40,
                "expected_goals": 3.6,
            },
        },
    ],
    "arsenal": [
        {
            "full_name": "Bukayo Saka",
            "slug": "bukayo-saka",
            "shirt_number": 7,
            "position": "FWD",
            "nationality": "England",
            "date_of_birth": date(2001, 9, 5),
            "stats": {
                "appearances": 25,
                "starts": 24,
                "minutes": 2100,
                "goals": 6,
                "assists": 10,
                "shots": 63,
                "key_passes": 61,
                "tackles": 22,
                "interceptions": 9,
                "expected_goals": 8.4,
            },
        },
        {
            "full_name": "Declan Rice",
            "slug": "declan-rice",
            "shirt_number": 41,
            "position": "MID",
            "nationality": "England",
            "date_of_birth": date(1999, 1, 14),
            "stats": {
                "appearances": 35,
                "starts": 34,
                "minutes": 2957,
                "goals": 4,
                "assists": 8,
                "shots": 42,
                "key_passes": 54,
                "tackles": 58,
                "interceptions": 31,
                "expected_goals": 3.4,
            },
        },
    ],
    "manchester-city": [
        {
            "full_name": "Erling Haaland",
            "slug": "erling-haaland",
            "shirt_number": 9,
            "position": "FWD",
            "nationality": "Norway",
            "date_of_birth": date(2000, 7, 21),
            "stats": {
                "appearances": 31,
                "starts": 31,
                "minutes": 2767,
                "goals": 22,
                "assists": 3,
                "shots": 107,
                "key_passes": 19,
                "tackles": 8,
                "interceptions": 2,
                "expected_goals": 22.1,
            },
        },
        {
            "full_name": "Phil Foden",
            "slug": "phil-foden",
            "shirt_number": 47,
            "position": "MID",
            "nationality": "England",
            "date_of_birth": date(2000, 5, 28),
            "stats": {
                "appearances": 28,
                "starts": 20,
                "minutes": 1800,
                "goals": 7,
                "assists": 2,
                "shots": 58,
                "key_passes": 39,
                "tackles": 20,
                "interceptions": 10,
                "expected_goals": 7.2,
            },
        },
    ],
    "chelsea": [
        {
            "full_name": "Cole Palmer",
            "slug": "cole-palmer",
            "shirt_number": 20,
            "position": "FWD",
            "nationality": "England",
            "date_of_birth": date(2002, 5, 6),
            "stats": {
                "appearances": 37,
                "starts": 36,
                "minutes": 3180,
                "goals": 15,
                "assists": 8,
                "shots": 112,
                "key_passes": 89,
                "tackles": 27,
                "interceptions": 11,
                "expected_goals": 14.8,
            },
        },
        {
            "full_name": "Moises Caicedo",
            "slug": "moises-caicedo",
            "shirt_number": 25,
            "position": "MID",
            "nationality": "Ecuador",
            "date_of_birth": date(2001, 11, 2),
            "stats": {
                "appearances": 38,
                "starts": 38,
                "minutes": 3420,
                "goals": 1,
                "assists": 2,
                "shots": 23,
                "key_passes": 31,
                "tackles": 91,
                "interceptions": 52,
                "expected_goals": 1.3,
            },
        },
    ],
    "newcastle-united": [
        {
            "full_name": "Alexander Isak",
            "slug": "alexander-isak",
            "shirt_number": 14,
            "position": "FWD",
            "nationality": "Sweden",
            "date_of_birth": date(1999, 9, 21),
            "stats": {
                "appearances": 34,
                "starts": 34,
                "minutes": 2894,
                "goals": 23,
                "assists": 6,
                "shots": 99,
                "key_passes": 42,
                "tackles": 15,
                "interceptions": 5,
                "expected_goals": 20.3,
            },
        },
        {
            "full_name": "Bruno Guimaraes",
            "slug": "bruno-guimaraes",
            "shirt_number": 39,
            "position": "MID",
            "nationality": "Brazil",
            "date_of_birth": date(1997, 11, 16),
            "stats": {
                "appearances": 38,
                "starts": 37,
                "minutes": 3290,
                "goals": 5,
                "assists": 6,
                "shots": 42,
                "key_passes": 52,
                "tackles": 72,
                "interceptions": 37,
                "expected_goals": 4.2,
            },
        },
    ],
    "aston-villa": [
        {
            "full_name": "Ollie Watkins",
            "slug": "ollie-watkins",
            "shirt_number": 11,
            "position": "FWD",
            "nationality": "England",
            "date_of_birth": date(1995, 12, 30),
            "stats": {
                "appearances": 38,
                "starts": 31,
                "minutes": 2842,
                "goals": 16,
                "assists": 8,
                "shots": 87,
                "key_passes": 38,
                "tackles": 12,
                "interceptions": 4,
                "expected_goals": 15.7,
            },
        },
        {
            "full_name": "Youri Tielemans",
            "slug": "youri-tielemans",
            "shirt_number": 8,
            "position": "MID",
            "nationality": "Belgium",
            "date_of_birth": date(1997, 5, 7),
            "stats": {
                "appearances": 36,
                "starts": 35,
                "minutes": 3105,
                "goals": 3,
                "assists": 7,
                "shots": 48,
                "key_passes": 55,
                "tackles": 56,
                "interceptions": 28,
                "expected_goals": 3.1,
            },
        },
    ],
}


def seed_sample_data(session: Session) -> bool:
    """Insert missing public sample rows. Returns True when rows were added.

    The row-by-row checks intentionally keep this seed idempotent. They also let
    an existing stage-2 database receive newly added stage-3 sample rows without
    asking the user to delete their local SQLite file.
    """

    rows_added = False
    clubs_by_slug: dict[str, Club] = {}
    for club_data in CLUBS:
        club = session.scalar(select(Club).where(Club.slug == club_data["slug"]))
        if club is None:
            club = Club(**club_data, source_kind="sample")
            session.add(club)
            session.flush()
            rows_added = True
        clubs_by_slug[club.slug] = club

    for slug, standing_data in STANDINGS.items():
        standing = session.scalar(
            select(Standing).where(
                Standing.club_id == clubs_by_slug[slug].id,
                Standing.season == SAMPLE_SEASON,
            )
        )
        if standing is None:
            session.add(
                Standing(
                    club_id=clubs_by_slug[slug].id,
                    season=SAMPLE_SEASON,
                    source_kind="sample",
                    **standing_data,
                )
            )
            rows_added = True

    for slug, players in PLAYERS.items():
        for player_data in players:
            player = session.scalar(
                select(Player).where(Player.slug == player_data["slug"])
            )
            if player is None:
                player = Player(
                    club_id=clubs_by_slug[slug].id,
                    full_name=player_data["full_name"],
                    slug=player_data["slug"],
                    shirt_number=player_data["shirt_number"],
                    position=player_data["position"],
                    nationality=player_data["nationality"],
                    date_of_birth=player_data["date_of_birth"],
                    source_kind="sample",
                )
                session.add(player)
                session.flush()
                rows_added = True

            stats = session.scalar(
                select(PlayerSeasonStat).where(
                    PlayerSeasonStat.player_id == player.id,
                    PlayerSeasonStat.season == SAMPLE_SEASON,
                )
            )
            if stats is None:
                session.add(
                    PlayerSeasonStat(
                        player_id=player.id,
                        season=SAMPLE_SEASON,
                        source_kind="sample",
                        **player_data["stats"],
                    )
                )
                rows_added = True

    session.commit()
    return rows_added

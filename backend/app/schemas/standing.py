from datetime import date

from pydantic import BaseModel


class StandingClub(BaseModel):
    id: int
    name: str
    short_name: str
    slug: str
    primary_color: str


class StandingItem(BaseModel):
    position: int
    club: StandingClub
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    source_kind: str


class StandingTableData(BaseModel):
    season: str
    items: list[StandingItem]
    total: int
    is_partial: bool
    snapshot_date: date
    source_name: str
    source_url: str
    sample_notice: str

from datetime import date

from pydantic import BaseModel, ConfigDict


class StadiumData(BaseModel):
    name: str
    latitude: float
    longitude: float


class ClubSummary(BaseModel):
    id: int
    name: str
    short_name: str
    slug: str
    city: str
    stadium: StadiumData
    founded_year: int | None
    primary_color: str
    source_kind: str


class PlayerSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    slug: str
    shirt_number: int | None
    position: str
    nationality: str
    date_of_birth: date | None
    source_kind: str


class ClubDetail(ClubSummary):
    players: list[PlayerSummary]


class ClubListData(BaseModel):
    items: list[ClubSummary]
    total: int
    player_total: int
    limit: int
    offset: int
    sample_notice: str

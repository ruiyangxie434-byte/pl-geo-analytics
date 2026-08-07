from datetime import datetime

from pydantic import BaseModel


class MatchTeamData(BaseModel):
    id: int
    name: str
    short_name: str
    slug: str
    primary_color: str
    score: int
    shots: int
    goals: int
    total_xg: float


class MatchShotData(BaseModel):
    source_event_id: str
    period: int
    minute: int
    second: int
    team_name: str
    team_slug: str
    team_color: str
    player_name: str | None
    outcome: str
    is_goal: bool
    x: float
    y: float
    xg: float
    body_part: str | None
    shot_type: str | None
    play_pattern: str | None


class MatchSummaryData(BaseModel):
    source_match_id: str
    competition: str
    season: str
    matchweek: int
    kickoff_at: datetime | None
    venue: str
    status: str
    home_team: MatchTeamData
    away_team: MatchTeamData
    shot_count: int
    goal_count: int
    total_xg: float
    source_kind: str


class MatchListData(BaseModel):
    items: list[MatchSummaryData]
    total: int
    source_name: str
    source_url: str
    license_url: str
    sample_notice: str


class MatchDetailData(MatchSummaryData):
    shots: list[MatchShotData]
    source_name: str
    source_url: str
    license_url: str
    source_last_updated: str
    coordinate_note: str
    interpretation_note: str

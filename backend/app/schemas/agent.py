from typing import Literal

from pydantic import BaseModel, Field, field_validator


AgentFocus = Literal["balanced", "scoring", "creativity", "pressing"]
AgentRequestedFocus = Literal[
    "auto",
    "balanced",
    "scoring",
    "creativity",
    "pressing",
]
AgentGenerationMode = Literal["local_rules", "qwen_enhanced"]
AgentGenerationStatus = Literal[
    "completed",
    "not_configured",
    "fallback",
    "pending",
]


class AgentAnalysisRequest(BaseModel):
    question: str = Field(min_length=6, max_length=500)
    player_slugs: list[str] | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )
    season: str = Field(default="2024-25", pattern=r"^\d{4}-\d{2}$")
    focus: AgentRequestedFocus = "auto"

    @field_validator("player_slugs")
    @classmethod
    def validate_unique_players(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        if value is not None and len(set(value)) != len(value):
            raise ValueError("请选择两名不同的球员")
        return value


class AgentPlayerOption(BaseModel):
    slug: str
    full_name: str
    club_name: str
    club_color: str
    position: str
    minutes: int


class AgentPlayerOptionData(BaseModel):
    items: list[AgentPlayerOption]
    total: int
    season: str
    sample_notice: str


class AgentPlayerProfile(AgentPlayerOption):
    nationality: str


class AgentMetricValue(BaseModel):
    player_slug: str
    value: float
    percentile: int


class AgentMetricComparison(BaseModel):
    key: str
    label: str
    unit: str
    weight: float
    values: list[AgentMetricValue]
    leader_slug: str | None


class AgentStep(BaseModel):
    index: int
    title: str
    tool: str
    detail: str
    status: Literal["completed"]


class AgentEvidence(BaseModel):
    title: str
    detail: str
    leader_slug: str | None


class AgentRecommendation(BaseModel):
    winner_slug: str
    headline: str
    summary: str
    confidence: float
    scores: dict[str, int]


class AgentGeneration(BaseModel):
    mode: AgentGenerationMode
    status: AgentGenerationStatus
    provider: Literal["local", "qwen"]
    model: str | None
    note: str


class AgentCapabilitiesData(BaseModel):
    qwen_configured: bool
    provider: Literal["qwen"]
    model: str
    default_mode: AgentGenerationMode
    message: str


class AgentAnalysisData(BaseModel):
    run_id: str
    task_type: Literal["player_comparison"]
    question: str
    season: str
    requested_focus: AgentRequestedFocus
    focus: AgentFocus
    focus_label: str
    players: list[AgentPlayerProfile]
    steps: list[AgentStep]
    metrics: list[AgentMetricComparison]
    evidence: list[AgentEvidence]
    recommendation: AgentRecommendation
    generation: AgentGeneration
    limitations: list[str]
    sample_notice: str

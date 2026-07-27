from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.agent import (
    AgentAnalysisData,
    AgentAnalysisRequest,
    AgentPlayerOptionData,
)
from app.schemas.common import ApiResponse
from app.services.analysis_agent import (
    AgentInputError,
    analyze_players,
    list_agent_players,
)

router = APIRouter(prefix="/agent", tags=["analysis-agent"])


@router.get("/players", response_model=ApiResponse[AgentPlayerOptionData])
def get_agent_players(
    season: str = Query(default="2024-25", pattern=r"^\d{4}-\d{2}$"),
    db: Session = Depends(get_db),
) -> ApiResponse[AgentPlayerOptionData]:
    return ApiResponse(
        message="Agent 可分析球员获取成功",
        data=list_agent_players(db, season),
    )


@router.post("/analyze", response_model=ApiResponse[AgentAnalysisData])
def run_agent_analysis(
    payload: AgentAnalysisRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[AgentAnalysisData]:
    try:
        result = analyze_players(db, payload)
    except AgentInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return ApiResponse(
        message="足球分析 Agent 已完成任务",
        data=result,
    )

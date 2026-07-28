from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.agent import (
    AgentAnalysisData,
    AgentAnalysisRequest,
    AgentCapabilitiesData,
    AgentPlayerOptionData,
)
from app.schemas.common import ApiResponse
from app.services.analysis_agent import (
    AgentInputError,
    analyze_players,
    list_agent_players,
)
from app.services.qwen_service import enhance_analysis_with_qwen

router = APIRouter(prefix="/agent", tags=["analysis-agent"])


@router.get(
    "/capabilities",
    response_model=ApiResponse[AgentCapabilitiesData],
)
def get_agent_capabilities() -> ApiResponse[AgentCapabilitiesData]:
    settings = get_settings()
    configured = settings.qwen_configured
    return ApiResponse(
        message="Agent 能力状态获取成功",
        data=AgentCapabilitiesData(
            qwen_configured=configured,
            provider="qwen",
            model=settings.qwen_model,
            default_mode=(
                "qwen_enhanced" if configured else "local_rules"
            ),
            message=(
                "千问增强已启用，统计结果仍由本地工具计算。"
                if configured
                else "未配置千问 API Key，当前使用本地规则模式。"
            ),
        ),
    )


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
        base_result = analyze_players(db, payload)
    except AgentInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    result = enhance_analysis_with_qwen(
        base_result,
        get_settings(),
    )

    return ApiResponse(
        message="足球分析 Agent 已完成任务",
        data=result,
    )

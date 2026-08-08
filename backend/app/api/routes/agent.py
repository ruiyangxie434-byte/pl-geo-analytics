from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.agent import (
    AgentAnalysisData,
    AgentAnalysisRequest,
    AgentCapabilitiesData,
    AgentFollowUpRequest,
    AgentPlayerOptionData,
    AgentRunDetailData,
    AgentRunListData,
)
from app.schemas.common import ApiResponse
from app.services.analysis_agent import (
    AgentInputError,
    analyze_players,
    list_agent_players,
)
from app.services.agent_notebook import (
    AgentRunNotFoundError,
    add_follow_up_context,
    build_run_detail,
    get_agent_run,
    list_agent_runs,
    save_agent_run,
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
    save_agent_run(db, result)

    return ApiResponse(
        message="足球分析 Agent 已完成任务并保存记录",
        data=result,
    )


@router.get("/runs", response_model=ApiResponse[AgentRunListData])
def get_agent_runs(
    limit: int = Query(default=8, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> ApiResponse[AgentRunListData]:
    return ApiResponse(
        message="Agent 分析记录获取成功",
        data=list_agent_runs(db, limit=limit, offset=offset),
    )


@router.get(
    "/runs/{run_id}",
    response_model=ApiResponse[AgentRunDetailData],
)
def get_agent_run_detail(
    run_id: str,
    db: Session = Depends(get_db),
) -> ApiResponse[AgentRunDetailData]:
    try:
        run = get_agent_run(db, run_id)
    except AgentRunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ApiResponse(
        message="Agent 分析记录获取成功",
        data=build_run_detail(run),
    )


@router.post(
    "/runs/{run_id}/follow-up",
    response_model=ApiResponse[AgentAnalysisData],
)
def run_agent_follow_up(
    run_id: str,
    payload: AgentFollowUpRequest,
    db: Session = Depends(get_db),
) -> ApiResponse[AgentAnalysisData]:
    try:
        parent = get_agent_run(db, run_id)
    except AgentRunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    parent_result = build_run_detail(parent).result
    request = AgentAnalysisRequest(
        question=payload.question,
        player_slugs=[player.slug for player in parent_result.players],
        season=parent_result.season,
        focus=payload.focus,
    )
    try:
        base_result = analyze_players(db, request)
    except AgentInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    contextual_result = add_follow_up_context(base_result, parent)
    result = enhance_analysis_with_qwen(
        contextual_result,
        get_settings(),
    )
    save_agent_run(db, result)
    return ApiResponse(
        message="Agent 已基于上次记录完成追问并保存新版本",
        data=result,
    )

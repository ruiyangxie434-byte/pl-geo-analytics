import json
from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError

from app.core.config import Settings
from app.schemas.agent import (
    AgentAnalysisData,
    AgentGeneration,
    AgentRecommendation,
    AgentStep,
)


class QwenNarrative(BaseModel):
    headline: str = Field(min_length=4, max_length=120)
    summary: str = Field(min_length=20, max_length=700)


class QwenGenerationError(RuntimeError):
    """Raised when Qwen cannot return a valid grounded narrative."""


SYSTEM_PROMPT = """
你是“英超智析 Agent”的回答表达层。
后端已经完成数据库查询、每90分钟换算、百分位和加权得分计算。
你的任务仅是把给定的结构化证据组织成简洁、专业的中文结论。

必须遵守：
1. 只能使用用户输入中提供的球员、赛季、得分、指标和限制。
2. 不得补充伤病、转会、比赛结果、实时状态或任何未提供的事实。
3. 不得改变 winner_slug、综合得分、百分位或置信度。
4. 清楚区分数据事实与分析判断，不使用“绝对更强”等绝对化措辞。
5. 只返回 JSON 对象，字段必须为 headline 和 summary。
""".strip()


def _build_grounding_payload(result: AgentAnalysisData) -> dict[str, Any]:
    return {
        "question": result.question,
        "season": result.season,
        "focus": result.focus_label,
        "players": [
            {
                "slug": player.slug,
                "name": player.full_name,
                "club": player.club_name,
                "position": player.position,
                "minutes": player.minutes,
            }
            for player in result.players
        ],
        "winner_slug": result.recommendation.winner_slug,
        "scores": result.recommendation.scores,
        "confidence": result.recommendation.confidence,
        "evidence": [
            {
                "title": item.title,
                "detail": item.detail,
                "leader_slug": item.leader_slug,
            }
            for item in result.evidence
        ],
        "limitations": result.limitations,
        "sample_notice": result.sample_notice,
        "run_context": result.context.model_dump(),
    }


def _request_qwen_narrative(
    result: AgentAnalysisData,
    settings: Settings,
    client: httpx.Client | None = None,
) -> QwenNarrative:
    if not settings.qwen_configured:
        raise QwenGenerationError("Qwen is not configured")

    endpoint = (
        f"{settings.qwen_base_url.rstrip('/')}/chat/completions"
    )
    request_body = {
        "model": settings.qwen_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    _build_grounding_payload(result),
                    ensure_ascii=False,
                ),
            },
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
    }

    owns_client = client is None
    active_client = client or httpx.Client(
        timeout=settings.qwen_timeout_seconds,
    )
    try:
        response = active_client.post(
            endpoint,
            headers={
                "Authorization": (
                    f"Bearer {settings.dashscope_api_key}"
                ),
                "Content-Type": "application/json",
            },
            json=request_body,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise QwenGenerationError("Qwen returned empty content")
        return QwenNarrative.model_validate_json(content)
    except (
        httpx.HTTPError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        ValidationError,
    ) as exc:
        raise QwenGenerationError(
            "Qwen returned an invalid response"
        ) from exc
    finally:
        if owns_client:
            active_client.close()


def _append_generation_step(
    result: AgentAnalysisData,
    *,
    tool: str,
    detail: str,
) -> list[AgentStep]:
    return [
        *result.steps,
        AgentStep(
            index=len(result.steps) + 1,
            title="组织最终回答",
            tool=tool,
            detail=detail,
            status="completed",
        ),
    ]


def enhance_analysis_with_qwen(
    result: AgentAnalysisData,
    settings: Settings,
    client: httpx.Client | None = None,
) -> AgentAnalysisData:
    if not settings.qwen_configured:
        return result.model_copy(
            update={
                "steps": _append_generation_step(
                    result,
                    tool="local_narrative",
                    detail=(
                        "未配置千问 API Key，本次使用本地模板组织结论；"
                        "统计计算和证据链不受影响。"
                    ),
                ),
                "generation": AgentGeneration(
                    mode="local_rules",
                    status="not_configured",
                    provider="local",
                    model=None,
                    note=(
                        "尚未配置千问，当前显示本地规则结论。"
                    ),
                ),
            }
        )

    try:
        narrative = _request_qwen_narrative(
            result,
            settings,
            client=client,
        )
    except QwenGenerationError:
        return result.model_copy(
            update={
                "steps": _append_generation_step(
                    result,
                    tool="qwen_fallback",
                    detail=(
                        "千问本次未能返回有效结果，系统已自动使用"
                        "本地模板结论。"
                    ),
                ),
                "generation": AgentGeneration(
                    mode="local_rules",
                    status="fallback",
                    provider="qwen",
                    model=settings.qwen_model,
                    note=(
                        "千问暂时不可用，本次已安全回退到本地规则。"
                    ),
                ),
            }
        )

    enhanced_recommendation = AgentRecommendation(
        winner_slug=result.recommendation.winner_slug,
        headline=narrative.headline,
        summary=narrative.summary,
        confidence=result.recommendation.confidence,
        scores=result.recommendation.scores,
    )
    return result.model_copy(
        update={
            "steps": _append_generation_step(
                result,
                tool="qwen_grounded_narrative",
                detail=(
                    f"使用 {settings.qwen_model} 基于已计算证据"
                    "组织中文回答，模型不能修改得分与指标。"
                ),
            ),
            "recommendation": enhanced_recommendation,
            "generation": AgentGeneration(
                mode="qwen_enhanced",
                status="completed",
                provider="qwen",
                model=settings.qwen_model,
                note=(
                    "统计结果由本地引擎计算，千问仅负责理解语境"
                    "并组织回答。"
                ),
            ),
        }
    )

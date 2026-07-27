from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Player, PlayerSeasonStat
from app.schemas.agent import (
    AgentAnalysisData,
    AgentAnalysisRequest,
    AgentEvidence,
    AgentFocus,
    AgentMetricComparison,
    AgentMetricValue,
    AgentPlayerOption,
    AgentPlayerOptionData,
    AgentPlayerProfile,
    AgentRecommendation,
    AgentStep,
)

SAMPLE_NOTICE = (
    "当前结论仅基于 2024-25 赛季的小型公开演示样例，用于验证 Agent "
    "工作流，不代表实时球探意见。"
)

FOCUS_LABELS: dict[AgentFocus, str] = {
    "balanced": "综合表现",
    "scoring": "终结与得分",
    "creativity": "创造与组织",
    "pressing": "高位逼抢适配",
}

METRICS = {
    "goals_per90": ("进球", "每90分钟"),
    "assists_per90": ("助攻", "每90分钟"),
    "shots_per90": ("射门", "每90分钟"),
    "key_passes_per90": ("关键传球", "每90分钟"),
    "tackles_per90": ("抢断", "每90分钟"),
    "interceptions_per90": ("拦截", "每90分钟"),
    "expected_goals_per90": ("预期进球", "每90分钟"),
}

FOCUS_WEIGHTS: dict[AgentFocus, dict[str, float]] = {
    "balanced": {
        "goals_per90": 0.22,
        "assists_per90": 0.17,
        "shots_per90": 0.10,
        "key_passes_per90": 0.18,
        "tackles_per90": 0.17,
        "interceptions_per90": 0.16,
    },
    "scoring": {
        "goals_per90": 0.34,
        "expected_goals_per90": 0.27,
        "shots_per90": 0.20,
        "assists_per90": 0.10,
        "key_passes_per90": 0.09,
    },
    "creativity": {
        "key_passes_per90": 0.34,
        "assists_per90": 0.30,
        "shots_per90": 0.10,
        "goals_per90": 0.12,
        "tackles_per90": 0.07,
        "interceptions_per90": 0.07,
    },
    "pressing": {
        "tackles_per90": 0.34,
        "interceptions_per90": 0.28,
        "key_passes_per90": 0.13,
        "assists_per90": 0.09,
        "goals_per90": 0.09,
        "shots_per90": 0.07,
    },
}

PLAYER_ALIASES = {
    "萨卡": "bukayo-saka",
    "帕尔默": "cole-palmer",
    "萨拉赫": "mohamed-salah",
    "哈兰德": "erling-haaland",
    "伊萨克": "alexander-isak",
    "福登": "phil-foden",
    "赖斯": "declan-rice",
    "沃特金斯": "ollie-watkins",
    "范戴克": "virgil-van-dijk",
    "凯塞多": "moises-caicedo",
}


class AgentInputError(ValueError):
    pass


@dataclass(frozen=True)
class PlayerSnapshot:
    player: Player
    stats: PlayerSeasonStat
    per90: dict[str, float]


def _per90(value: int | float | None, minutes: int) -> float:
    if minutes <= 0 or value is None:
        return 0.0
    return round(float(value) * 90 / minutes, 2)


def _calculate_per90(stats: PlayerSeasonStat) -> dict[str, float]:
    return {
        "goals_per90": _per90(stats.goals, stats.minutes),
        "assists_per90": _per90(stats.assists, stats.minutes),
        "shots_per90": _per90(stats.shots, stats.minutes),
        "key_passes_per90": _per90(stats.key_passes, stats.minutes),
        "tackles_per90": _per90(stats.tackles, stats.minutes),
        "interceptions_per90": _per90(stats.interceptions, stats.minutes),
        "expected_goals_per90": _per90(stats.expected_goals, stats.minutes),
    }


def _load_snapshots(db: Session, season: str) -> list[PlayerSnapshot]:
    rows = db.scalars(
        select(Player)
        .options(
            selectinload(Player.club),
            selectinload(Player.season_stats),
        )
        .order_by(Player.full_name)
    ).all()

    snapshots: list[PlayerSnapshot] = []
    for player in rows:
        stats = next(
            (item for item in player.season_stats if item.season == season),
            None,
        )
        if stats is not None and stats.minutes > 0:
            snapshots.append(
                PlayerSnapshot(
                    player=player,
                    stats=stats,
                    per90=_calculate_per90(stats),
                )
            )
    return snapshots


def list_agent_players(db: Session, season: str) -> AgentPlayerOptionData:
    snapshots = _load_snapshots(db, season)
    return AgentPlayerOptionData(
        items=[
            AgentPlayerOption(
                slug=item.player.slug,
                full_name=item.player.full_name,
                club_name=item.player.club.short_name,
                club_color=item.player.club.primary_color,
                position=item.player.position,
                minutes=item.stats.minutes,
            )
            for item in snapshots
        ],
        total=len(snapshots),
        season=season,
        sample_notice=SAMPLE_NOTICE,
    )


def _resolve_player_slugs(
    request: AgentAnalysisRequest,
    snapshots: list[PlayerSnapshot],
) -> list[str]:
    available = {item.player.slug: item for item in snapshots}
    if request.player_slugs is not None:
        missing = [slug for slug in request.player_slugs if slug not in available]
        if missing:
            raise AgentInputError(f"没有找到球员：{', '.join(missing)}")
        return request.player_slugs

    question = request.question.casefold()
    matched: list[str] = []
    for snapshot in snapshots:
        player = snapshot.player
        candidates = {
            player.full_name.casefold(),
            player.slug.replace("-", " ").casefold(),
            player.full_name.split()[-1].casefold(),
        }
        if any(candidate in question for candidate in candidates):
            matched.append(player.slug)

    for alias, slug in PLAYER_ALIASES.items():
        if alias in request.question and slug in available and slug not in matched:
            matched.append(slug)

    if len(matched) < 2:
        raise AgentInputError("请在问题中明确提到两名球员，或使用球员选择器")
    return matched[:2]


def _percentile(value: float, population: list[float]) -> int:
    if not population:
        return 0
    below_or_equal = sum(item <= value for item in population)
    return round(below_or_equal / len(population) * 100)


def _build_metrics(
    selected: list[PlayerSnapshot],
    population: list[PlayerSnapshot],
    focus: AgentFocus,
) -> tuple[list[AgentMetricComparison], dict[str, int]]:
    weights = FOCUS_WEIGHTS[focus]
    scores = {item.player.slug: 0.0 for item in selected}
    comparisons: list[AgentMetricComparison] = []

    for key, weight in weights.items():
        population_values = [item.per90[key] for item in population]
        values = [
            AgentMetricValue(
                player_slug=item.player.slug,
                value=item.per90[key],
                percentile=_percentile(item.per90[key], population_values),
            )
            for item in selected
        ]
        for value in values:
            scores[value.player_slug] += value.percentile * weight

        raw_values = [value.value for value in values]
        leader = None
        if abs(raw_values[0] - raw_values[1]) >= 0.01:
            leader = values[raw_values.index(max(raw_values))].player_slug

        label, unit = METRICS[key]
        comparisons.append(
            AgentMetricComparison(
                key=key,
                label=label,
                unit=unit,
                weight=weight,
                values=values,
                leader_slug=leader,
            )
        )

    return comparisons, {slug: round(value) for slug, value in scores.items()}


def _build_evidence(
    metrics: list[AgentMetricComparison],
    names: dict[str, str],
) -> list[AgentEvidence]:
    ranked = sorted(
        metrics,
        key=lambda item: abs(item.values[0].percentile - item.values[1].percentile)
        * item.weight,
        reverse=True,
    )
    evidence: list[AgentEvidence] = []
    for metric in ranked[:3]:
        first, second = metric.values
        if metric.leader_slug is None:
            detail = (
                f"两人的{metric.label}均为 {first.value:.2f}，"
                "当前样例下没有明显差距。"
            )
        else:
            leader = next(
                value
                for value in metric.values
                if value.player_slug == metric.leader_slug
            )
            other = next(
                value
                for value in metric.values
                if value.player_slug != metric.leader_slug
            )
            detail = (
                f"{names[leader.player_slug]}为 {leader.value:.2f}，"
                f"{names[other.player_slug]}为 {other.value:.2f}；"
                f"样例百分位分别为 {leader.percentile} 和 {other.percentile}。"
            )
        evidence.append(
            AgentEvidence(
                title=f"{metric.label}对比",
                detail=detail,
                leader_slug=metric.leader_slug,
            )
        )
    return evidence


def analyze_players(
    db: Session,
    request: AgentAnalysisRequest,
) -> AgentAnalysisData:
    population = _load_snapshots(db, request.season)
    if len(population) < 2:
        raise AgentInputError("当前赛季没有足够的球员样例用于比较")

    slugs = _resolve_player_slugs(request, population)
    by_slug = {item.player.slug: item for item in population}
    selected = [by_slug[slug] for slug in slugs]
    metrics, scores = _build_metrics(selected, population, request.focus)
    names = {item.player.slug: item.player.full_name for item in selected}

    winner_slug = max(scores, key=scores.get)
    loser_slug = next(slug for slug in slugs if slug != winner_slug)
    score_gap = abs(scores[winner_slug] - scores[loser_slug])
    confidence = round(min(0.82, 0.58 + score_gap / 250), 2)
    focus_label = FOCUS_LABELS[request.focus]

    limitations = [
        "数据为小型赛季样例，未包含伤病、对手强度、比赛状态和战术角色。",
        "百分位只在当前样例球员池内计算，不能等同于完整英超排名。",
    ]
    if selected[0].player.position != selected[1].player.position:
        limitations.append("两名球员登记位置不同，结论应结合实际场上职责理解。")

    return AgentAnalysisData(
        run_id=f"run_{uuid4().hex[:10]}",
        task_type="player_comparison",
        question=request.question,
        season=request.season,
        focus=request.focus,
        focus_label=focus_label,
        players=[
            AgentPlayerProfile(
                slug=item.player.slug,
                full_name=item.player.full_name,
                club_name=item.player.club.short_name,
                club_color=item.player.club.primary_color,
                position=item.player.position,
                minutes=item.stats.minutes,
                nationality=item.player.nationality,
            )
            for item in selected
        ],
        steps=[
            AgentStep(
                index=1,
                title="理解任务",
                tool="intent_router",
                detail=f"识别为双球员比较，重点分析“{focus_label}”。",
                status="completed",
            ),
            AgentStep(
                index=2,
                title="读取赛季数据",
                tool="player_stats_query",
                detail=(
                    f"从数据库定位 {names[slugs[0]]} 与 {names[slugs[1]]} "
                    f"的 {request.season} 赛季记录。"
                ),
                status="completed",
            ),
            AgentStep(
                index=3,
                title="统一指标口径",
                tool="per90_calculator",
                detail="将累计数据换算为每90分钟指标，并计算样例球员池百分位。",
                status="completed",
            ),
            AgentStep(
                index=4,
                title="生成决策建议",
                tool="evidence_ranker",
                detail="按任务权重汇总指标，只使用可追溯数据形成结论。",
                status="completed",
            ),
        ],
        metrics=metrics,
        evidence=_build_evidence(metrics, names),
        recommendation=AgentRecommendation(
            winner_slug=winner_slug,
            headline=f"{names[winner_slug]}更适合本次“{focus_label}”任务",
            summary=(
                f"Agent 综合得分 {scores[winner_slug]} 对 {scores[loser_slug]}。"
                "该建议来自每90分钟数据与样例百分位加权，不代表绝对能力排名。"
            ),
            confidence=confidence,
            scores=scores,
        ),
        limitations=limitations,
        sample_notice=SAMPLE_NOTICE,
    )

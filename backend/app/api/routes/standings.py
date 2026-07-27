from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.seed import SAMPLE_SEASON
from app.database.session import get_db
from app.models import Standing
from app.schemas.common import ApiResponse
from app.schemas.standing import StandingClub, StandingItem, StandingTableData

router = APIRouter(prefix="/standings", tags=["standings"])

SAMPLE_NOTICE = (
    "这是 2024-25 赛季最终积分榜中的 6 队样例切片，"
    "用于验证数据结构与接口，不是完整的 20 队积分榜。"
)


@router.get("", response_model=ApiResponse[StandingTableData])
def get_standings(
    season: str = Query(
        default=SAMPLE_SEASON,
        pattern=r"^\d{4}-\d{2}$",
    ),
    db: Session = Depends(get_db),
) -> ApiResponse[StandingTableData]:
    standings = db.scalars(
        select(Standing)
        .options(joinedload(Standing.club))
        .where(Standing.season == season)
        .order_by(Standing.position)
    ).all()

    items = [
        StandingItem(
            position=standing.position,
            club=StandingClub(
                id=standing.club.id,
                name=standing.club.name,
                short_name=standing.club.short_name,
                slug=standing.club.slug,
                primary_color=standing.club.primary_color,
            ),
            played=standing.played,
            won=standing.won,
            drawn=standing.drawn,
            lost=standing.lost,
            goals_for=standing.goals_for,
            goals_against=standing.goals_against,
            goal_difference=standing.goal_difference,
            points=standing.points,
            source_kind=standing.source_kind,
        )
        for standing in standings
    ]

    return ApiResponse(
        message="积分榜获取成功",
        data=StandingTableData(
            season=season,
            items=items,
            total=len(items),
            is_partial=len(items) < 20,
            sample_notice=SAMPLE_NOTICE,
        ),
    )

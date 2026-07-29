from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import ApiResponse
from app.schemas.health import HealthData

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=ApiResponse[HealthData],
    summary="检查 API 服务状态",
)
async def health_check() -> ApiResponse[HealthData]:
    settings = get_settings()
    return ApiResponse(
        message="Premier League Insight Agent API is running",
        data=HealthData(
            service=settings.app_name,
            status="healthy",
            environment=settings.app_env,
            version=settings.app_version,
        ),
    )

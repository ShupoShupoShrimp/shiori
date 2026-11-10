from fastapi import APIRouter
from shiori.api.schemas.health import HealthyResponse

router = APIRouter(tags=["Health"])


@router.get("/healthz", response_model=HealthyResponse)
async def health_check() -> HealthyResponse:
    return HealthyResponse(status="ok", database="connected")

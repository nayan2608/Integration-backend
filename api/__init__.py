from fastapi import APIRouter

from api import integrations


router: APIRouter = APIRouter()


router.include_router(
    integrations.router,
    tags=["integrations"],
)


__all__ = ["router"]

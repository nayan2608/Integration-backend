from fastapi import APIRouter


from api.integrations import airtable, hubspot, notion

router: APIRouter = APIRouter()

router.include_router(hubspot.router)
router.include_router(notion.router)
router.include_router(airtable.router)


__all__ = ["router"]

from fastapi import APIRouter, Form, Request

from database.enum import IntegrationTypeEnum
from services.integrations import integration_processors
from utils.integrations import IntegrationProcessor


router: APIRouter = APIRouter()

integration_processor: type[IntegrationProcessor] | None = integration_processors.get(
    IntegrationTypeEnum.NOTION
)


@router.post("/integrations/notion/authorize")
async def authorize_notion_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    if integration_processor:
        return await integration_processor.authorize(user_id, org_id)


@router.get("/integrations/notion/oauth2callback")
async def oauth2callback_notion_integration(request: Request):
    if integration_processor:
        return await integration_processor.oauth2callback(request)


@router.post("/integrations/notion/credentials")
async def get_notion_credentials_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    if integration_processor:
        return await integration_processor.get_credentials(user_id, org_id)


@router.post("/integrations/notion/load")
async def get_notion_items(credentials: str = Form(...)):
    if integration_processor:
        return await integration_processor.get_items(credentials)

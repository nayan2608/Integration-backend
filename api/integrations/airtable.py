from fastapi import APIRouter, Form, Request

from database.enum import IntegrationTypeEnum
from services.integrations import integration_processors
from utils.integrations import IntegrationProcessor


router: APIRouter = APIRouter()

integration_processor: type[IntegrationProcessor] | None = integration_processors.get(
    IntegrationTypeEnum.AIRTABLE
)


@router.post("/integrations/airtable/authorize")
async def authorize_airtable_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    if integration_processor:
        return await integration_processor.authorize(user_id, org_id)


@router.get("/integrations/airtable/oauth2callback")
async def oauth2callback_airtable_integration(request: Request):
    if integration_processor:
        return await integration_processor.oauth2callback(request)


@router.post("/integrations/airtable/credentials")
async def get_airtable_credentials_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    if integration_processor:
        return await integration_processor.get_credentials(user_id, org_id)


@router.post("/integrations/airtable/load")
async def get_airtable_items(credentials: str = Form(...)):
    if integration_processor:
        return await integration_processor.get_items(credentials)

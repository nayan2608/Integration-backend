from fastapi import APIRouter, Form, Request

from api import integrations

from database.enum import IntegrationTypeEnum
from services.integrations import integration_processors
from utils.integrations import IntegrationProcessor


router: APIRouter = APIRouter()


integration_processor: type[IntegrationProcessor] | None = integration_processors.get(
    IntegrationTypeEnum.HUBSPOT
)


@router.post("/integrations/hubspot/authorize")
async def authorize_hubspot_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    if integration_processor:
        return await integration_processor.authorize(user_id, org_id)


@router.get("/integrations/hubspot/oauth2callback")
async def oauth2callback_hubspot_integration(request: Request):
    if integration_processor:
        return await integration_processor.oauth2callback(request)


@router.post("/integrations/hubspot/credentials")
async def get_hubspot_credentials_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    if integration_processor:
        return await integration_processor.get_credentials(user_id, org_id)


@router.post("/integrations/hubspot/load")
async def load_slack_data_integration(credentials: str = Form(...)):
    if integration_processor:
        return await integration_processor.get_items(credentials)

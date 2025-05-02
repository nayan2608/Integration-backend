from fastapi import APIRouter, Form, Request

from services.integrations.airtable import (
    authorize_airtable,
    oauth2callback_airtable,
    get_airtable_credentials,
    get_items_airtable,
)


router: APIRouter = APIRouter()


@router.post("/integrations/airtable/authorize")
async def authorize_airtable_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    return await authorize_airtable(user_id, org_id)


@router.get("/integrations/airtable/oauth2callback")
async def oauth2callback_airtable_integration(request: Request):
    return await oauth2callback_airtable(request)


@router.post("/integrations/airtable/credentials")
async def get_airtable_credentials_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    return await get_airtable_credentials(user_id, org_id)


@router.post("/integrations/airtable/load")
async def get_airtable_items(credentials: str = Form(...)):
    return await get_items_airtable(credentials)

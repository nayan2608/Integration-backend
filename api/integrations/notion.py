from fastapi import APIRouter, Form, Request

from services.integrations.notion import (
    authorize_notion,
    get_items_notion,
    get_notion_credentials,
    oauth2callback_notion,
)


router: APIRouter = APIRouter()


@router.post("/integrations/notion/authorize")
async def authorize_notion_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    return await authorize_notion(user_id, org_id)


@router.get("/integrations/notion/oauth2callback")
async def oauth2callback_notion_integration(request: Request):
    return await oauth2callback_notion(request)


@router.post("/integrations/notion/credentials")
async def get_notion_credentials_integration(
    user_id: str = Form(...), org_id: str = Form(...)
):
    return await get_notion_credentials(user_id, org_id)


@router.post("/integrations/notion/load")
async def get_notion_items(credentials: str = Form(...)):
    return await get_items_notion(credentials)

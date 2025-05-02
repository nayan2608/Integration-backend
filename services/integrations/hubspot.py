# slack.py
import json
import secrets
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import requests
from core.config import settings
from schemas.integration_item import IntegrationItem
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis


CLIENT_ID = settings.HUBSPOT_CLIENT_ID
CLIENT_SECRET = settings.HUBSPOT_CLIENT_SECRET
REDIRECT_URI = "http://localhost:8000/integrations/hubspot/oauth2callback"
scope = "oauth crm.objects.contacts.read"
encoded_client_id_secret = base64.b64encode(
    f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
).decode()

authorization_url = f"https://app.hubspot.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://localhost:8000/integrations/hubspot/oauth2callback&scope=oauth%20crm.objects.contacts.read"


async def authorize_hubspot(user_id: str, org_id: str) -> str:
    """State data dictionary."""
    state_data = {
        "state": secrets.token_urlsafe(32),
        "user_id": user_id,
        "org_id": org_id,
    }

    """Encodes the state data to a JSON string."""
    encoded_state = json.dumps(state_data)

    """Stores the state data in Redis with an expiration time."""
    try:
        redis_key = f"hubspot_state:{org_id}:{user_id}"
        await add_key_value_redis(redis_key, encoded_state, expire=600)
    except Exception as e:
        # Handle the exception (log it, raise an error, etc.)
        raise RuntimeError(f"Failed to store state in Redis: {str(e)}")

    return f"{authorization_url}&state={encoded_state}"


async def oauth2callback_hubspot(request: Request) -> HTMLResponse:
    """Validates the state from the request query parameters."""
    error = request.query_params.get("error")
    if error:
        raise HTTPException(status_code=400, detail=error)

    code = request.query_params.get("code")
    encoded_state = request.query_params.get("state")

    if not encoded_state:
        raise HTTPException(status_code=400, detail="State parameter missing.")

    state_data = json.loads(encoded_state)
    original_state = state_data.get("state")
    user_id = state_data.get("user_id")
    org_id = state_data.get("org_id")

    saved_state = await get_value_redis(f"hubspot_state:{org_id}:{user_id}")

    if not saved_state or original_state != json.loads(saved_state).get("state"):
        raise HTTPException(status_code=400, detail="State does not match.")

    """Exchanges the authorization code for an access token."""
    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                "https://api.hubapi.com/oauth/v1/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "redirect_uri": REDIRECT_URI,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            ),
            delete_key_redis(f"hubspot_state:{org_id}:{user_id}"),
        )

    """Stores the state data in Redis with an expiration time."""
    try:
        redis_key = f"hubspot_credentials:{org_id}:{user_id}"
        await add_key_value_redis(
            redis_key,
            json.dumps(response.json()),
            expire=600,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to store state in Redis: {str(e)}")

    # Return a simple HTML response to close the window
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)


async def get_hubspot_credentials(user_id: str, org_id: str) -> dict:
    """Retrieves and deletes HubSpot credentials from Redis."""
    redis_key = f"hubspot_credentials:{org_id}:{user_id}"

    # Retrieve credentials from Redis
    credentials = await get_value_redis(redis_key)
    if not credentials:
        raise HTTPException(status_code=400, detail="No credentials found.")

    # Parse the credentials JSON
    try:
        credentials_data = json.loads(credentials)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode credentials.")

    # Delete the credentials from Redis
    await delete_key_redis(redis_key)

    return credentials_data


def create_integration_item_metadata_object(response_json: dict) -> IntegrationItem:
    """Creates an IntegrationItem object from a JSON response."""
    full_name = (
        response_json["properties"]["firstname"]
        + response_json["properties"]["lastname"]
    )

    return IntegrationItem(
        id=response_json["id"],
        name=full_name,
        creation_time=response_json["properties"]["createdate"],
        last_modified_time=response_json["properties"]["lastmodifieddate"],
    )


async def get_items_hubspot(credentials: str) -> list[IntegrationItem]:
    """Fetches items from HubSpot and returns a list of IntegrationItem objects."""
    credentials_dict = json.loads(credentials)
    access_token = credentials_dict.get("access_token")

    if not access_token:
        raise ValueError("Missing access token in credentials.")

    response = requests.get(
        "https://api.hubapi.com/crm/v3/objects/contacts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch items from HubSpot.",
        )

    results = response.json().get("results", [])
    list_of_integration_item_metadata = [
        create_integration_item_metadata_object(result) for result in results
    ]
    print(list_of_integration_item_metadata)
    return list_of_integration_item_metadata

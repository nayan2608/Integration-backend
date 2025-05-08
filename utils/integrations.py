from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.responses import HTMLResponse

from schemas.integration_item import IntegrationItem


class IntegrationProcessor(ABC):
    @classmethod
    @abstractmethod
    async def authorize(cls, user_id: str, org_id: str) -> str:
        pass

    @classmethod
    @abstractmethod
    async def oauth2callback(cls, request: Request) -> HTMLResponse:
        pass

    @classmethod
    @abstractmethod
    async def get_credentials(cls, user_id: str, org_id: str) -> dict:
        pass

    @classmethod
    @abstractmethod
    async def get_items(cls, credentials: str) -> list[IntegrationItem]:
        pass

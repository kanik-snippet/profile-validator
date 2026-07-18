from __future__ import annotations

from app.core.config import get_settings
from app.core.http import http_client

class VerisoulAuth:

    def __init__(self) -> None:
        settings = get_settings()

        self.url = settings.verisoul_auth_url
        self.api_key = settings.verisoul_api_key

        
    async def authenticate(
        self,
        *,
        session_id: str,
        account: dict,
    ) -> dict:

        response = await http_client.client.post(
            self.url,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            },
            json={
                "session_id": session_id,
                "account": account,
            },
        )

        response.raise_for_status()

        return response.json()

from typing import Any

import httpx

from app.core.config import get_settings
from app.core.http import http_client

class OctoClient:
    """
    Low-level Octo Browser API client.

    Responsibilities:
    - Create profile (Cloud API)
    - Update profile (Cloud API)
    - Delete profile (Cloud API)
    - Start profile (Local API)
    - Stop profile (Local API)

    No business logic belongs here.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self.cloud_url = settings.octo_api_base_url.rstrip("/")
        self.local_url = settings.octo_local_api.rstrip("/")

        self.headers = {
            "X-Octo-Api-Token": settings.octo_api_token,
            "Content-Type": "application/json",
        }
   

    ############################################################
    # Internal request helper
    ############################################################

    async def _request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        **kwargs,
    ) -> dict[str, Any]:

        client = http_client.client

        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs,
        )

        response.raise_for_status()

        if not response.content:
            return {}

        return response.json()

    ############################################################
    # Cloud API
    ############################################################

    async def create_profile(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        return await self._request(
            "POST",
            f"{self.cloud_url}/profiles",
            headers=self.headers,
            json=payload,
        )

    async def update_profile(
        self,
        profile_uuid: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        return await self._request(
            "PATCH",
            f"{self.cloud_url}/profiles/{profile_uuid}",
            headers=self.headers,
            json=payload,
        )

    async def delete_profile(
        self,
        profile_uuid: str,
    ) -> dict[str, Any]:

        return await self._request(
            "DELETE",
            f"{self.cloud_url}/profiles/{profile_uuid}",
            headers=self.headers,
        )

    async def get_profile(
        self,
        profile_uuid: str,
    ) -> dict[str, Any]:

        return await self._request(
            "GET",
            f"{self.cloud_url}/profiles/{profile_uuid}",
            headers=self.headers,
        )

    ############################################################
    # Local API
    ############################################################

    async def start_profile(
        self,
        profile_uuid: str,
        *,
        headless: bool = False,
        debug_port: bool = True,
        timeout: int = 120,
    ) -> dict[str, Any]:

        payload = {
            "uuid": profile_uuid,
            "headless": headless,
            "debug_port": debug_port,
            "timeout": timeout,
            "only_local": True,
            "flags": [],
            "password": "",
        }

        return await self._request(
            "POST",
            f"{self.local_url}/profiles/start",
            headers={"Content-Type": "application/json"},
            json=payload,
        )

    async def stop_profile(
        self,
        profile_uuid: str,
    ) -> dict[str, Any]:

        payload = {
            "uuid": profile_uuid,
        }

        return await self._request(
            "POST",
            f"{self.local_url}/profiles/stop",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
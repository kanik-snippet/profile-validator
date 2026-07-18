from __future__ import annotations

from app.octo.client import OctoClient


class OctoManager:
    """
    Business layer for Octo Browser.

    Responsibilities:
        - Create profile
        - Configure profile
        - Start browser
        - Stop browser
        - Delete profile

    Does NOT know anything about Playwright or Verisoul.
    """

    def __init__(self, client: OctoClient):
        self.client = client

    async def create_profile(
        self,
        *,
        title: str,
        description: str = "",
        platform: str = "win",
        tags: list[str] | None = None,
        proxy: dict | None = None,
    ) -> str:

        payload = {
            "title": title,
            "description": description,
            "tags": tags or [],
            "fingerprint": {
                "os": platform
            }
        }

        if proxy:
            payload["proxy"] = proxy

        response = await self.client.create_profile(payload)

        return response["data"]["uuid"]

    async def update_start_page(
        self,
        profile_uuid: str,
        start_url: str,
    ) -> None:

        payload = {
            "start_pages": [
                start_url
            ]
        }

        await self.client.update_profile(profile_uuid, payload)

    async def start_profile(
        self,
        profile_uuid: str,
        *,
        headless: bool = False,
    ) -> dict:

        response = await self.client.start_profile(
            profile_uuid=profile_uuid,
            headless=headless,
        )

        return response

    async def stop_profile(self, profile_uuid: str) -> None:
        await self.client.stop_profile(profile_uuid)

    async def delete_profile(self, profile_uuid: str) -> None:
        await self.client.delete_profile(profile_uuid)

    async def prepare_profile(
        self,
        *,
        title: str,
        start_url: str,
        platform: str = "win",
        proxy: dict | None = None,
        headless: bool = False,
    ) -> dict:
        """
        Complete workflow:

            create
                ↓
            update start page
                ↓
            start browser

        Returns Local API response.
        """

        profile_uuid = await self.create_profile(
            title=title,
            platform=platform,
            proxy=proxy,
        )

        await self.update_start_page(
            profile_uuid,
            start_url,
        )

        browser = await self.start_profile(
            profile_uuid,
            headless=headless,
        )

        browser["profile_uuid"] = profile_uuid

        return browser
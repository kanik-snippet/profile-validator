from __future__ import annotations

import httpx


class HttpClient:

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def startup(self) -> None:

        if self._client is not None:
            return

        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=30,
                read=120,
                write=30,
                pool=30,
            ),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
            follow_redirects=True,
        )

    async def shutdown(self) -> None:

        if self._client is None:
            return

        await self._client.aclose()
        self._client = None

    @property
    def client(self) -> httpx.AsyncClient:

        if self._client is None:
            raise RuntimeError(
                "HTTP client has not been initialized."
            )

        return self._client


http_client = HttpClient()
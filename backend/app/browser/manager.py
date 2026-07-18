from __future__ import annotations

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


class BrowserManager:
    """
    Manages Playwright connection to an Octo Browser profile.

    Responsibilities:
        - Connect to existing Octo browser
        - Expose Browser/Context/Page
        - Navigate pages
        - Close connection

    Does NOT create Octo profiles.
    Does NOT call Verisoul.
    """

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None

    async def connect(self, ws_endpoint: str) -> Browser:
        """
        Connect to an already running Octo profile.
        """

        if self.browser:
            return self.browser

        self._playwright = await async_playwright().start()

        self.browser = await self._playwright.chromium.connect_over_cdp(
            ws_endpoint
        )

        contexts = self.browser.contexts

        if contexts:
            self.context = contexts[0]
        else:
            self.context = await self.browser.new_context()

        return self.browser

    async def page(self) -> Page:
        """
        Return an existing page or create one.
        """

        if self.context is None:
            raise RuntimeError("Browser is not connected.")

        pages = self.context.pages

        if pages:
            return pages[0]

        return await self.context.new_page()

    async def new_page(self) -> Page:
        """
        Always create a new tab.
        """

        if self.context is None:
            raise RuntimeError("Browser is not connected.")

        return await self.context.new_page()

    async def goto(
        self,
        url: str,
        *,
        wait_until: str = "domcontentloaded",
        timeout: int = 30000,
    ) -> Page:
        """
        Navigate to URL.
        """

        page = await self.page()

        await page.goto(
            url,
            wait_until=wait_until,
            timeout=timeout,
        )

        return page

    async def current_page(self) -> Page:
        return await self.page()

    async def close(self) -> None:
        """
        Disconnect Playwright.

        Octo browser continues running.
        """

        if self.browser:
            await self.browser.close()
            self.browser = None

        self.context = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
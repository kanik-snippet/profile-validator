import logging

logger = logging.getLogger(__name__)


class BrowserController:
    """Phase 1 placeholder for a Playwright CDP connection."""

    async def connect(self, debug_port: int) -> None:
        logger.info("Dummy browser connected on port %s", debug_port)

    async def disconnect(self) -> None:
        logger.info("Dummy browser disconnected")

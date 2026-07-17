import asyncio
import hashlib
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class VerisoulTester:
    """Phase 1 deterministic simulator; replace with page automation in Phase 4."""

    async def test_profile(self, profile_key: str) -> tuple[int, str]:
        await asyncio.sleep(get_settings().dummy_test_delay_seconds)
        score = int(hashlib.sha256(profile_key.encode()).hexdigest()[:8], 16) % 101
        logger.info("Dummy Verisoul score for %s: %s", profile_key, score)
        return score, "Dummy Verisoul validation result"

import logging
from dataclasses import dataclass
from uuid import uuid4

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OctoProfile:
    id: str
    debug_port: int


class OctoManager:
    """Phase 1 in-memory Octo API adapter; replace internals in Phase 2."""

    def create_profile(self, platform: str, proxy: str) -> OctoProfile:
        profile = OctoProfile(id=f"dummy-{uuid4().hex[:12]}", debug_port=9222)
        logger.info("Created Octo profile %s for %s", profile.id, platform)
        return profile

    def start_profile(self, profile_id: str) -> int:
        logger.info("Started Octo profile %s", profile_id)
        return 9222

    def stop_profile(self, profile_id: str) -> None:
        logger.info("Stopped Octo profile %s", profile_id)

    def delete_profile(self, profile_id: str) -> None:
        logger.info("Deleted Octo profile %s", profile_id)

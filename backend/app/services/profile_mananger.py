from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.models import Job, Profile

logger = logging.getLogger(__name__)


class ProfileManager:
    """
    Handles Profile database operations.

    Responsibilities:
        - Create profile record
        - Update profile status
        - Mark profile as running
        - Mark profile as deleted
        - Mark profile as failed
    """

    def create(
        self,
        session: Session,
        *,
        job: Job,
        profile_uuid: str,
        platform: str,
        proxy: dict | None,
    ) -> Profile:
        """
        Create a new profile record.
        """

        profile = Profile(
            job_id=job.id,
            octo_profile_id=profile_uuid,
            platform=platform,
            proxy=proxy,
            status="created",
        )

        session.add(profile)
        session.commit()
        session.refresh(profile)

        logger.info(
            "Created profile %s for job %s",
            profile.id,
            job.id,
        )

        return profile

    def update_status(
        self,
        session: Session,
        *,
        profile: Profile,
        status: str,
    ) -> Profile:
        """
        Update profile status.
        """

        profile.status = status

        session.commit()
        session.refresh(profile)

        logger.debug(
            "Profile %s -> %s",
            profile.id,
            status,
        )

        return profile

    def mark_testing(
        self,
        session: Session,
        *,
        profile: Profile,
    ) -> Profile:

        return self.update_status(
            session,
            profile=profile,
            status="testing",
        )

    def mark_running(
        self,
        session: Session,
        *,
        profile: Profile,
    ) -> Profile:

        return self.update_status(
            session,
            profile=profile,
            status="running",
        )

    def mark_deleted(
        self,
        session: Session,
        *,
        profile: Profile,
    ) -> Profile:

        return self.update_status(
            session,
            profile=profile,
            status="deleted",
        )

    def mark_failed(
        self,
        session: Session,
        *,
        profile: Profile,
    ) -> Profile:

        return self.update_status(
            session,
            profile=profile,
            status="failed",
        )
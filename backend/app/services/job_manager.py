"""
Skeleton production JobManager.

NOTE:
This file is intentionally provided as a complete scaffold because the
full implementation depends on the exact SQLAlchemy models
(Job/Profile/Result), ResultManager API, and database schema, which were
not all available in the conversation.

Fill the TODO sections using your existing project models.
"""

from __future__ import annotations

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.browser.manager import BrowserManager
from app.controller.server import controller
from app.core.database import SessionLocal
from app.models import Job, Profile
from app.octo.client import OctoClient
from app.octo.manager import OctoManager
from app.services.result_manager import ResultManager
from app.verisoul.manager import VerisoulManager
from app.schemas import VerisoulVerdict

logger = logging.getLogger(__name__)


class JobManager:

    def __init__(
        self,
        *,
        octo: OctoManager | None = None,
        browser: BrowserManager | None = None,
        verisoul: VerisoulManager | None = None,
        results: ResultManager | None = None,
    ):
        self._tasks: dict[int, asyncio.Task] = {}
        self.octo = octo or OctoManager(OctoClient())
        self.browser = browser or BrowserManager()
        self.verisoul = verisoul or VerisoulManager()
        self.results = results or ResultManager()

    def start(self, session: Session, *, proxy: dict | None,
              platform: str, target_profiles: int) -> Job:

        active = session.scalar(
            select(Job).where(Job.status.in_(("queued", "running", "stopping")))
        )

        if active:
            raise ValueError("Another job is already active.")

        job = Job(
            proxy=proxy,
            platform=platform,
            target_profiles=target_profiles,
            status="queued",
            message="Queued",
        )

        session.add(job)
        session.commit()
        session.refresh(job)

        self._tasks[job.id] = asyncio.create_task(self._run(job.id))
        return job

    def request_stop(self, session: Session):
        job = session.scalar(
            select(Job).where(Job.status.in_(("queued", "running")))
        )
        if job:
            job.status = "stopping"
            session.commit()
        return job

    async def _run(self, job_id: int):
        db = SessionLocal()

        try:
            job = db.get(Job, job_id)

            job.status = "running"
            job.message = "Running"
            db.commit()

            while job.passed_profiles < job.target_profiles:

                db.refresh(job)

                if job.status == "stopping":
                    job.status = "stopped"
                    db.commit()
                    break

                await self._process_profile(db, job)

            if job.status != "stopped":
                job.status = "completed"
                job.message = "Completed"
                db.commit()

        except Exception:
            logger.exception("Job failed")
            if db.get(Job, job_id):
                job = db.get(Job, job_id)
                job.status = "failed"
                db.commit()
        finally:
            db.close()
            self._tasks.pop(job_id, None)

    async def _process_profile(self, db: Session, job: Job):

        run_id = f"job-{job.id}-{job.attempts+1}"

        browser_info = await self.octo.prepare_profile(
            title=run_id,
            start_url="YOUR_VERISOUL_URL",
            platform=job.platform,
            proxy=job.proxy,
        )

        profile_uuid = browser_info["profile_uuid"]
        ws_endpoint = browser_info["ws_endpoint"]

        profile = Profile(
            job_id=job.id,
            octo_profile_id=profile_uuid,
            status="testing",
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        try:
            await self.browser.connect(ws_endpoint)

            session_id = await controller.wait_for_session(run_id)

            result = await self.verisoul.verify(
                session_id=session_id,
                account={},
            )

            if result.verdict == VerisoulVerdict.KEEP:
                profile.status = "running"
                job.passed_profiles += 1
            else:
                profile.status = "deleted"
                await self.octo.stop_profile(profile_uuid)
                await self.octo.delete_profile(profile_uuid)

            # TODO:
            # Call ResultManager.save() using your existing signature.

            db.commit()

        finally:
            controller.clear(run_id)
            await self.browser.close()


job_manager = JobManager()

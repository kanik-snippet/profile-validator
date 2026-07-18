from __future__ import annotations

import asyncio
import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.browser.manager import BrowserManager
from app.controller.server import controller
from app.core.database import SessionLocal
from app.models import Job
from app.octo.client import OctoClient
from app.octo.manager import OctoManager
from app.services.result_manager import ResultManager
from app.verisoul.manager import VerisoulManager

logger = logging.getLogger(__name__)


class JobManager:
    """
    Coordinates the complete automation workflow.

        Job
          ↓
      Octo Profile
          ↓
      Browser
          ↓
      Controller
          ↓
      Verisoul
          ↓
      Database
    """

    def __init__(
        self,
        *,
        octo: OctoManager | None = None,
        browser: BrowserManager | None = None,
        verisoul: VerisoulManager | None = None,
        results: ResultManager | None = None,
    ) -> None:

        self._tasks: dict[int, asyncio.Task] = {}

        self.octo = octo or OctoManager(OctoClient())
        self.browser = browser or BrowserManager()
        self.verisoul = verisoul or VerisoulManager()
        self.results = results or ResultManager()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def start(
        self,
        session: Session,
        *,
        proxy: dict | None,
        platform: str,
        target_profiles: int,
    ) -> Job:
        """
        Create a new background job.
        """

        active = session.scalar(
            select(Job).where(
                Job.status.in_(
                    (
                        "queued",
                        "running",
                        "stopping",
                    )
                )
            )
        )

        if active:
            raise ValueError("Another job is already running.")

        job = Job(
            proxy=proxy,
            platform=platform,
            target_profiles=target_profiles,
            status="queued",
            message="Waiting to start",
        )

        session.add(job)
        session.commit()
        session.refresh(job)

        task = asyncio.create_task(
            self._run(job.id),
            name=f"job-{job.id}",
        )

        self._tasks[job.id] = task

        logger.info("Queued job %s", job.id)

        return job

    def request_stop(
        self,
        session: Session,
    ) -> Job | None:
        """
        Request graceful stop.
        """

        job = session.scalar(
            select(Job).where(
                Job.status.in_(
                    (
                        "queued",
                        "running",
                    )
                )
            )
        )

        if job is None:
            return None

        job.status = "stopping"
        job.message = "Stop requested"

        session.commit()

        logger.info("Stop requested for job %s", job.id)

        return job

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _should_stop(
        self,
        session: Session,
        job_id: int,
    ) -> bool:

        job = session.get(Job, job_id)

        if job is None:
            return True

        return job.status == "stopping"

    async def _run(
        self,
        job_id: int,
    ) -> None:
        """
        Implemented in Part 2.
        """
        raise NotImplementedError
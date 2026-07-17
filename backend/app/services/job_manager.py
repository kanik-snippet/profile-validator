import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.browser.controller import BrowserController
from app.core.config import get_settings
from app.models import Job, Profile
from app.octo.manager import OctoManager
from app.services.result_manager import ResultManager
from app.core.database import SessionLocal
from app.verisoul.tester import VerisoulTester

logger = logging.getLogger(__name__)


class JobManager:
    def __init__(self) -> None:
        self._tasks: dict[int, asyncio.Task] = {}
        self.octo = OctoManager()
        self.browser = BrowserController()
        self.tester = VerisoulTester()
        self.results = ResultManager()

    def start(self, session: Session, proxy: str, platform: str, target_profiles: int) -> Job:
        active = session.scalar(select(Job).where(Job.status.in_(("queued", "running", "stopping"))))
        if active:
            raise ValueError("A job is already active")
        job = Job(proxy=proxy, platform=platform, target_profiles=target_profiles, status="queued")
        session.add(job)
        session.commit()
        session.refresh(job)
        self._tasks[job.id] = asyncio.create_task(self._run(job.id), name=f"job-{job.id}")
        logger.info("Queued job %s", job.id)
        return job

    def request_stop(self, session: Session) -> Job | None:
        job = session.scalar(select(Job).where(Job.status.in_(("queued", "running"))))
        if job:
            job.status = "stopping"
            job.message = "Stop requested"
            session.commit()
            logger.info("Stop requested for job %s", job.id)
        return job

    def _should_stop(self, session: Session, job_id: int) -> bool:
        return session.get(Job, job_id).status == "stopping"

    async def _run(self, job_id: int) -> None:
        session = SessionLocal()
        try:
            job = session.get(Job, job_id)
            job.status, job.message = "running", "Creating profiles"
            session.commit()
            while job.passed_profiles < job.target_profiles:
                session.refresh(job)
                if self._should_stop(session, job_id):
                    job.status, job.message = "stopped", "Stopped by user"
                    session.commit()
                    return
                octo_profile = self.octo.create_profile(job.platform, job.proxy)
                profile = Profile(job_id=job.id, octo_profile_id=octo_profile.id, platform=job.platform, proxy=job.proxy, status="created")
                session.add(profile)
                job.attempts += 1
                session.commit()
                session.refresh(profile)

                port = self.octo.start_profile(octo_profile.id)
                profile.status = "testing"
                session.commit()
                await self.browser.connect(port)
                score, reason = await self.tester.test_profile(octo_profile.id)
                await self.browser.disconnect()
                passed = score <= get_settings().pass_score_max
                if passed:
                    profile.status = "running"
                    job.passed_profiles += 1
                    self.results.save(session, job.id, profile.id, score, "PASS", reason)
                else:
                    self.octo.stop_profile(octo_profile.id)
                    self.octo.delete_profile(octo_profile.id)
                    profile.status = "deleted"
                    self.results.save(session, job.id, profile.id, score, "FAIL", reason)
                job.message = f"{job.passed_profiles}/{job.target_profiles} good profiles ready"
                session.commit()
            job.status, job.message = "completed", f"{job.target_profiles} good profiles are running"
            session.commit()
            logger.info("Completed job %s", job.id)
        except Exception:
            logger.exception("Job %s failed", job_id)
            if job := session.get(Job, job_id):
                job.status, job.message = "failed", "Unexpected automation error; see logs"
                session.commit()
        finally:
            session.close()
            self._tasks.pop(job_id, None)


job_manager = JobManager()

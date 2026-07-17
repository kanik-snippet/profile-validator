import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.schemas import JobResponse, JobStartRequest, ProfileResponse, ResultResponse
from app.models import Job, Profile, Result
from app.services.job_manager import job_manager
from app.core.database import get_session

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    logger.info("Health check requested")
    return {"status": "ok"}


@router.post("/job/start", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
def start_job(payload: JobStartRequest, session: Session = Depends(get_session)) -> Job:
    try:
        return job_manager.start(session, payload.proxy, payload.platform, payload.target_profiles)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/job/stop", response_model=JobResponse)
def stop_job(session: Session = Depends(get_session)) -> Job:
    job = job_manager.request_stop(session)
    if not job:
        raise HTTPException(status_code=404, detail="No active job")
    return job


@router.get("/job/status", response_model=JobResponse)
def job_status(session: Session = Depends(get_session)) -> Job:
    job = session.scalar(select(Job).order_by(Job.id.desc()))
    if not job:
        raise HTTPException(status_code=404, detail="No jobs found")
    return job


@router.get("/profiles", response_model=list[ProfileResponse])
def profiles(session: Session = Depends(get_session)) -> list[Profile]:
    return list(session.scalars(select(Profile).order_by(Profile.id.desc())))


@router.get("/results", response_model=list[ResultResponse])
def results(session: Session = Depends(get_session)) -> list[Result]:
    return list(session.scalars(select(Result).order_by(Result.id.desc())))

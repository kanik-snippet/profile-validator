import logging

from sqlalchemy.orm import Session

from app.models import Result

logger = logging.getLogger(__name__)


class ResultManager:
    def save(self, session: Session, job_id: int, profile_id: int | None, score: int, status: str, reason: str) -> Result:
        result = Result(job_id=job_id, profile_id=profile_id, score=score, status=status, reason=reason)
        session.add(result)
        session.commit()
        session.refresh(result)
        logger.info("Saved %s result for job %s", status, job_id)
        return result

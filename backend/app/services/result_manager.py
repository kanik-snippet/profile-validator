from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.models import Result
from app.schemas import VerisoulResult

logger = logging.getLogger(__name__)


class ResultManager:
    """
    Persists Verisoul verification results.

    This class only writes results to the database.
    It contains no business logic.
    """

    def save(
        self,
        session: Session,
        *,
        job_id: int,
        profile_id: int | None,
        result: VerisoulResult,
    ) -> Result:
        record = Result(
            job_id=job_id,
            profile_id=profile_id,
            score=result.score,
            status=result.verdict.value,
            reason=result.reason,
        )

        session.add(record)
        session.commit()
        session.refresh(record)

        logger.info(
            "Saved %s result for job=%s profile=%s score=%s",
            result.verdict.value,
            job_id,
            profile_id,
            result.score,
        )

        return record
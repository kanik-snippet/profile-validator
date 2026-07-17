from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.profile import Profile


class ResultStatus(str, Enum):
    KEEP = "KEEP"
    CLOSE = "CLOSE"


class Result(Base):
    __tablename__ = "results"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    job_id: Mapped[str] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    profile_id: Mapped[str] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    status: Mapped[ResultStatus] = mapped_column(
        SqlEnum(ResultStatus, name="result_status"),
        nullable=False,
        index=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    screenshot_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    raw_response: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    # Relationships

    job: Mapped["Job"] = relationship(
        back_populates="results",
    )

    profile: Mapped["Profile"] = relationship(
        back_populates="results",
    )
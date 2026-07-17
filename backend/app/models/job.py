from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.proxy import Proxy
    from app.models.result import Result


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    proxy_id: Mapped[str | None] = mapped_column(
        ForeignKey("proxies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    platform: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    target_profiles: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    passed_profiles: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    failed_profiles: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    status: Mapped[JobStatus] = mapped_column(
        SqlEnum(JobStatus, name="job_status"),
        default=JobStatus.QUEUED,
        nullable=False,
        index=True,
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    proxy: Mapped["Proxy | None"] = relationship(
        back_populates="jobs",
    )

    profiles: Mapped[list["Profile"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )

    results: Mapped[list["Result"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
    )
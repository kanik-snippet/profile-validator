from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.proxy import Proxy
    from app.models.result import Result


class ProfileStatus(str, Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    TESTING = "testing"
    PASSED = "passed"
    FAILED = "failed"
    STOPPED = "stopped"
    DELETED = "deleted"


class Profile(Base):
    __tablename__ = "profiles"

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

    proxy_id: Mapped[str | None] = mapped_column(
        ForeignKey("proxies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    octo_profile_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    platform: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    browser_type: Mapped[str] = mapped_column(
        String(30),
        default="chrome",
        nullable=False,
    )

    status: Mapped[ProfileStatus] = mapped_column(
        SqlEnum(ProfileStatus, name="profile_status"),
        default=ProfileStatus.CREATED,
        nullable=False,
        index=True,
    )

    last_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    last_verdict: Mapped[str | None] = mapped_column(
        String(20),
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

    # Relationships

    job: Mapped["Job"] = relationship(
        back_populates="profiles",
    )

    proxy: Mapped["Proxy | None"] = relationship(
        back_populates="profiles",
    )

    results: Mapped[list["Result"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
    )
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Job(Timestamped, Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    proxy: Mapped[str] = mapped_column(String(500))
    platform: Mapped[str] = mapped_column(String(30))
    target_profiles: Mapped[int] = mapped_column(Integer)
    passed_profiles: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="queued")
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Profile(Timestamped, Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True)
    octo_profile_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    platform: Mapped[str] = mapped_column(String(30))
    proxy: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="created")


class Result(Timestamped, Base):
    __tablename__ = "results"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=True)
    score: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(10))
    reason: Mapped[str] = mapped_column(Text)
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class Proxy(Timestamped, Base):
    __tablename__ = "proxies"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(500), unique=True)
    status: Mapped[str] = mapped_column(String(30), default="available")

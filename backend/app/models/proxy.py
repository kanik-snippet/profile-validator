from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.profile import Profile


class ProxyStatus(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    DISABLED = "disabled"


class Proxy(Base):
    __tablename__ = "proxies"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    host: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    port: Mapped[int] = mapped_column(
        nullable=False,
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    protocol: Mapped[str] = mapped_column(
        String(20),
        default="http",
        nullable=False,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[ProxyStatus] = mapped_column(
        SqlEnum(ProxyStatus, name="proxy_status"),
        default=ProxyStatus.AVAILABLE,
        nullable=False,
        index=True,
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

    jobs: Mapped[list["Job"]] = relationship(
        back_populates="proxy",
    )

    profiles: Mapped[list["Profile"]] = relationship(
        back_populates="proxy",
    )

    @property
    def proxy_url(self) -> str:
        """
        Returns proxy in URL format.

        Example:
        http://user:pass@host:port
        """

        if self.username and self.password:
            return (
                f"{self.protocol}://"
                f"{self.username}:{self.password}@"
                f"{self.host}:{self.port}"
            )

        return f"{self.protocol}://{self.host}:{self.port}"
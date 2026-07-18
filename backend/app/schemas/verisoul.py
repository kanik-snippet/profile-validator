from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class VerisoulSignals(BaseModel):

    session_id: str | None = None

    device_id: str | None = None

    score: int = 0

    bot_probability: float = 0.0

    country: str | None = None

    proxy: bool = False

    emulator: bool = False

    raw: dict[str, Any] = Field(default_factory=dict)


class VerisoulVerdict(str, Enum):
    KEEP = "KEEP"
    CLOSE = "CLOSE"


class VerisoulResult(BaseModel):

    verdict: VerisoulVerdict

    score: int

    reason: str

    signals: VerisoulSignals
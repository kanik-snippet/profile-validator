from __future__ import annotations

from typing import Any

from app.schemas.verisoul import VerisoulSignals


class VerisoulParser:
    """
    Parses the raw Verisoul authentication response
    into a normalized schema.
    """

    def parse(
        self,
        response: dict[str, Any],
    ) -> VerisoulSignals:

        session = response.get("session", {})
        risk = response.get("risk", {})
        bot = response.get("bot", {})
        device = response.get("device", {})

        return VerisoulSignals(
            session_id=session.get("id"),
            device_id=device.get("id"),
            score=risk.get("score", 0),
            bot_probability=bot.get("probability", 0.0),
            country=device.get("country"),
            proxy=device.get("proxy", False),
            emulator=device.get("emulator", False),
            raw=response,
        )
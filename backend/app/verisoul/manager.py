from __future__ import annotations

from app.core.config import get_settings
from app.schemas import (
    VerisoulResult,
    VerisoulSignals,
    VerisoulVerdict,
)


class VerisoulClassifier:

    def __init__(self) -> None:

        settings = get_settings()

        self.minimum_score = settings.verisoul_score_threshold

    def classify(
        self,
        signals: VerisoulSignals,
    ) -> VerisoulResult:

        if signals.score < self.minimum_score:
            return VerisoulResult(
                verdict=VerisoulVerdict.CLOSE,
                score=signals.score,
                reason="Score below threshold",
                signals=signals,
            )

        if signals.proxy:
            return VerisoulResult(
                verdict=VerisoulVerdict.CLOSE,
                score=signals.score,
                reason="Proxy detected",
                signals=signals,
            )

        if signals.emulator:
            return VerisoulResult(
                verdict=VerisoulVerdict.CLOSE,
                score=signals.score,
                reason="Emulator detected",
                signals=signals,
            )

        return VerisoulResult(
            verdict=VerisoulVerdict.KEEP,
            score=signals.score,
            reason="Verification passed",
            signals=signals,
        )
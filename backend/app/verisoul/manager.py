from __future__ import annotations

from app.schemas import VerisoulResult

from app.verisoul.auth import VerisoulAuth
from app.verisoul.classifier import VerisoulClassifier
from app.verisoul.parser import VerisoulParser


class VerisoulManager:
    """
    High-level service responsible for the complete
    Verisoul verification workflow.

        Authenticate
            ↓
        Parse Response
            ↓
        Classify Result
            ↓
        Return VerisoulResult
    """

    def __init__(self) -> None:

        self.auth = VerisoulAuth()
        self.parser = VerisoulParser()
        self.classifier = VerisoulClassifier()

    async def verify(
        self,
        *,
        session_id: str,
        account: dict[str, str],
    ) -> VerisoulResult:
        """
        Executes the complete Verisoul verification flow.
        """

        response = await self.auth.authenticate(
            session_id=session_id,
            account=account,
        )

        signals = self.parser.parse(response)

        return self.classifier.classify(signals)
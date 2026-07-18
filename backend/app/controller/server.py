from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel


class SessionEvent(BaseModel):
    run_id: str
    session_id: str


class BrowserEvent(BaseModel):
    run_id: str
    event: str
    data: dict[str, Any] = {}


class ControllerServer:
    """
    Local event controller used by the Verisoul page.

    Receives events from the browser and exposes them to
    the backend.
    """

    def __init__(self) -> None:
        self.router = APIRouter()

        self.sessions: dict[str, str] = {}
        self.events: dict[str, list[dict]] = {}

        self._register_routes()

    def _register_routes(self) -> None:

        @self.router.get("/health")
        async def health():
            return {"status": "ok"}

        @self.router.post("/session")
        async def session(event: SessionEvent):
            self.sessions[event.run_id] = event.session_id
            return {"success": True}

        @self.router.post("/event")
        async def browser_event(event: BrowserEvent):
            self.events.setdefault(event.run_id, []).append(
                {
                    "event": event.event,
                    "data": event.data,
                }
            )
            return {"success": True}

        @self.router.get("/session/{run_id}")
        async def get_session(run_id: str):

            session = self.sessions.get(run_id)

            if session is None:
                raise HTTPException(
                    status_code=404,
                    detail="Session not available",
                )

            return {
                "session_id": session,
            }

    async def wait_for_session(
        self,
        run_id: str,
        timeout: int = 60,
    ) -> str:

        end = asyncio.get_running_loop().time() + timeout

        while asyncio.get_running_loop().time() < end:

            session = self.sessions.get(run_id)

            if session:
                return session

            await asyncio.sleep(0.5)

        raise TimeoutError(
            f"Session timeout ({run_id})"
        )

    def get_events(self, run_id: str) -> list[dict]:
        return self.events.get(run_id, [])

    def clear(self, run_id: str) -> None:
        self.sessions.pop(run_id, None)
        self.events.pop(run_id, None)


controller = ControllerServer()
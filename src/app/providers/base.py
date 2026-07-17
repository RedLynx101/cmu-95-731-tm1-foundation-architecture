from typing import Protocol

from app.models import AskResponse


class AnswerProvider(Protocol):
    name: str

    async def answer(self, question: str) -> AskResponse:
        """Return a structured answer for a validated question."""

from app.models import AskResponse


class StubAnswerProvider:
    name = "stub"

    async def answer(self, question: str) -> AskResponse:
        return AskResponse(
            answer=f"Stub response for: {question}",
            sources=[],
            confidence="stub",
            escalation_flag=False,
        )

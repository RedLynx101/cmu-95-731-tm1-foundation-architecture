from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

    @field_validator("question")
    @classmethod
    def normalize_question(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("question must contain non-whitespace characters")
        return normalized


class SourceReference(BaseModel):
    title: str
    url: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)
    confidence: Literal["stub", "low", "medium", "high"]
    escalation_flag: bool


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    provider: str

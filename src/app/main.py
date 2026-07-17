import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI

from app.config import load_settings
from app.models import AskRequest, AskResponse, HealthResponse
from app.providers.factory import create_provider

settings = load_settings()
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)
provider = create_provider(settings.model_provider)

app = FastAPI(
    title="CMU Services API",
    description="Minimum viable question-answering service for TM1.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(provider=provider.name)


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    request_id = str(uuid4())
    started = perf_counter()
    response = await provider.answer(request.question)
    latency_ms = (perf_counter() - started) * 1000
    logger.info(
        "ask_completed request_id=%s provider=%s question_chars=%d latency_ms=%.1f",
        request_id,
        provider.name,
        len(request.question),
        latency_ms,
    )
    return response

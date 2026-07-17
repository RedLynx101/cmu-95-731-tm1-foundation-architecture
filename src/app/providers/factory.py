from app.providers.base import AnswerProvider
from app.providers.stub import StubAnswerProvider


def create_provider(provider_name: str) -> AnswerProvider:
    if provider_name == "stub":
        return StubAnswerProvider()
    raise ValueError(
        f"Unsupported MODEL_PROVIDER={provider_name!r}. "
        "TM1 implements only the deterministic 'stub' provider."
    )

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_provider: str = "stub"
    log_level: str = "INFO"


def load_settings() -> Settings:
    return Settings(
        model_provider=os.getenv("MODEL_PROVIDER", "stub").strip().lower(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
    )

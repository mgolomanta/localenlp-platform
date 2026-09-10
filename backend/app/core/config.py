import os
from dataclasses import dataclass
from functools import lru_cache


def _csv(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    host: str
    port: int
    log_level: str
    cors_origins: list[str]
    hf_token: str | None
    model_cache_dir: str
    translation_batch_size: int
    max_input_chars: int
    max_upload_mb: int
    max_translation_tokens: int
    num_beams: int
    whisper_model: str
    whisper_language: str | None


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "LocaleNLP Translation API"),
        environment=os.getenv("ENVIRONMENT", "development"),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        cors_origins=_csv(os.getenv("CORS_ORIGINS", "http://localhost:3000")),
        hf_token=os.getenv("HF_TOKEN") or None,
        model_cache_dir=os.getenv("MODEL_CACHE_DIR", "/tmp/huggingface"),
        translation_batch_size=int(os.getenv("TRANSLATION_BATCH_SIZE", "8")),
        max_input_chars=int(os.getenv("MAX_INPUT_CHARS", "50000")),
        max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "20")),
        max_translation_tokens=int(os.getenv("MAX_TRANSLATION_TOKENS", "512")),
        num_beams=int(os.getenv("NUM_BEAMS", "4")),
        whisper_model=os.getenv("WHISPER_MODEL", "base"),
        whisper_language=os.getenv("WHISPER_LANGUAGE") or None,
    )

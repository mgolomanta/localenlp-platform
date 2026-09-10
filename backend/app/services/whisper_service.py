import logging
import os
import tempfile
from threading import Lock

import whisper

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class WhisperService:
    def __init__(self):
        self.settings = get_settings()
        self._model = None
        self._lock = Lock()

    def load(self):
        if self._model is not None:
            return self._model
        with self._lock:
            if self._model is None:
                logger.info("Loading Whisper model: %s", self.settings.whisper_model)
                self._model = whisper.load_model(self.settings.whisper_model)
        return self._model

    def transcribe_bytes(self, content: bytes, filename: str, language: str | None = None):
        suffix = os.path.splitext(filename or "")[1] or ".audio"
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        try:
            with open(path, "wb") as f:
                f.write(content)
            model = self.load()
            options = {}
            lang = language or self.settings.whisper_language
            if lang:
                options["language"] = lang
            result = model.transcribe(path, **options)
            return result.get("text", "").strip()
        finally:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


whisper_service = WhisperService()

import logging
import time

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.config import get_settings
from app.core.models import LANGUAGES, supported_pairs
from app.services.extractors import extract_text_from_bytes, extension_from_filename
from app.services.model_manager import model_manager
from app.services.translator import translate_text
from app.services.whisper_service import whisper_service

logger = logging.getLogger(__name__)
router = APIRouter()


def _pair_exists(source: str, target: str) -> bool:
    return (source, target) in {(p["source"], p["target"]) for p in supported_pairs()}


@router.get("/health")
def health():
    return {"status": "ok", "service": "localenlp-api", "environment": get_settings().environment, "device": str(model_manager.device)}


@router.get("/languages")
def languages():
    return {"languages": list(LANGUAGES.values()), "pairs": supported_pairs()}


@router.get("/models")
def models():
    return {"available": supported_pairs(), "loaded": model_manager.loaded_models()}


@router.post("/translate")
def translate(payload: dict):
    source = payload.get("source_lang")
    target = payload.get("target_lang")
    text = payload.get("text", "")
    if not source or not target:
        raise HTTPException(status_code=400, detail="source_lang and target_lang are required")
    if not _pair_exists(source, target):
        raise HTTPException(status_code=400, detail=f"Unsupported language pair: {source} -> {target}")
    started = time.perf_counter()
    try:
        result = translate_text(text, source, target)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        logger.exception("Translation failed")
        raise HTTPException(status_code=500, detail="Translation failed")
    return {"source_lang": source, "target_lang": target, "translation": result, "elapsed_ms": round((time.perf_counter() - started) * 1000, 2)}


@router.post("/translate/file")
async def translate_file(file: UploadFile = File(...), source_lang: str = Form(...), target_lang: str = Form(...)):
    settings = get_settings()
    if not _pair_exists(source_lang, target_lang):
        raise HTTPException(status_code=400, detail="Unsupported language pair")
    extension = extension_from_filename(file.filename or "")
    if extension not in {"pdf", "docx", "html", "htm", "md", "srt", "txt", "text"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.max_upload_mb} MB limit")
    try:
        extracted = extract_text_from_bytes(content, file.filename or "")
        translation = translate_text(extracted, source_lang, target_lang)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        logger.exception("File translation failed")
        raise HTTPException(status_code=500, detail="File translation failed")
    return {"filename": file.filename, "source_lang": source_lang, "target_lang": target_lang, "extracted_text": extracted, "translation": translation}


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    settings = get_settings()
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.max_upload_mb} MB limit")
    try:
        text = whisper_service.transcribe_bytes(content, file.filename or "audio")
    except Exception:
        logger.exception("Transcription failed")
        raise HTTPException(status_code=500, detail="Transcription failed")
    return {"filename": file.filename, "text": text}


@router.post("/transcribe-and-translate")
async def transcribe_and_translate(file: UploadFile = File(...), source_lang: str = Form(...), target_lang: str = Form(...)):
    settings = get_settings()
    if not _pair_exists(source_lang, target_lang):
        raise HTTPException(status_code=400, detail="Unsupported language pair")
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.max_upload_mb} MB limit")
    try:
        text = whisper_service.transcribe_bytes(content, file.filename or "audio", language=source_lang)
        translation = translate_text(text, source_lang, target_lang)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        logger.exception("Audio translation failed")
        raise HTTPException(status_code=500, detail="Audio translation failed")
    return {"filename": file.filename, "source_lang": source_lang, "target_lang": target_lang, "transcription": text, "translation": translation}

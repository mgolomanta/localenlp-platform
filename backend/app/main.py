import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO), format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

app = FastAPI(title=settings.app_name, version="1.0.0", description="LocaleNLP translation and speech API.")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"name": settings.app_name, "docs": "/docs", "health": "/api/health"}

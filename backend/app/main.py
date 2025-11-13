"""
backend/app/main.py
FastAPI application entrypoint.
"""
import logging
from fastapi import FastAPI

from app.core.settings import settings
from app.api.v1.endpoints import router as v1_router
from app.core.logging_setup import configure_logging

configure_logging()
logger = logging.getLogger("k8s-yaml-analyzer")

app = FastAPI(
    title="K8s YAML Analyzer",
    description="Validate and analyze Kubernetes YAML for schema, security and best practices.",
    version="0.1.0",
)

app.include_router(v1_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    logger.info("Starting K8s YAML Analyzer backend (version=%s)", settings.APP_VERSION)

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "service": "k8s-yaml-analyzer", "version": settings.APP_VERSION}
@app.get("/health")
def health():
    return {"status": "ok"}

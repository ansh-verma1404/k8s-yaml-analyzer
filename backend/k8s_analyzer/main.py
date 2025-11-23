"""
FastAPI application entrypoint.
"""

import logging
from fastapi import FastAPI
import uvicorn

from k8s_analyzer.core.settings import settings
from k8s_analyzer.api.v1.endpoints import router as v1_router
from k8s_analyzer.admission.router import router as admission_router

from k8s_analyzer.core.logging_setup import configure_logging

# logging
configure_logging()
logger = logging.getLogger("k8s-yaml-analyzer")

# FastAPI app
app = FastAPI(
    title="K8s YAML Analyzer",
    description="Validate and analyze Kubernetes YAML for schema, security and best practices.",
    version="0.1.0",
)

# API routes
app.include_router(v1_router, prefix="/api/v1")

# Admission webhook route
app.include_router(admission_router)   # exposes POST /validate

@app.on_event("startup")
async def on_startup():
    logger.info("Starting K8s YAML Analyzer backend (version=%s)", settings.APP_VERSION)

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "service": "k8s-yaml-analyzer", "version": settings.APP_VERSION}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("k8s_analyzer.main:app", host="0.0.0.0", port=8443, reload=True)


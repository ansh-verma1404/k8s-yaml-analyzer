# backend/app/api/v1/endpoints.py
from fastapi import APIRouter, File, UploadFile, Body, HTTPException
from typing import Optional
import logging

from app.api.v1.models import ScanResult, Finding
from app.analyzer.parser import parse_yaml_documents
from app.analyzer.best_practices import find_best_practices_issues
from app.analyzer.security_checks import find_security_issues
from app.analyzer.schema_validator import validate_schema_for_docs
from app.analyzer.report import build_report

logger = logging.getLogger("k8s-yaml-analyzer.api")

router = APIRouter()

@router.post("/scan", response_model=ScanResult)
async def scan(file: UploadFile = File(None), raw_yaml: Optional[str] = Body(None, media_type="text/plain")):
    """
    Scan uploaded YAML file or raw YAML text for schema, security and best-practice issues.
    Provide either multipart file upload (file) or raw YAML text (raw_yaml).
    """
    content = None
    if file is not None:
        try:
            content_bytes = await file.read()
            content = content_bytes.decode("utf-8")
        except Exception as e:
            logger.exception("Failed to read uploaded file")
            raise HTTPException(status_code=400, detail="Failed to read uploaded file")
    elif raw_yaml is not None:
        content = raw_yaml
    else:
        raise HTTPException(status_code=400, detail="No file or raw_yaml provided")

    try:
        docs = parse_yaml_documents(content)
    except Exception as e:
        logger.exception("Parsing YAML failed")
        raise HTTPException(status_code=400, detail=f"YAML parse error: {e}")

    findings = []

    # schema validation (best-effort -- offline stub if no schema available)
    try:
        schema_issues = validate_schema_for_docs(docs)
        findings.extend(schema_issues)
    except Exception:
        logger.exception("Schema validation failed, continuing with other checks")

    # best practices
    try:
        bp_issues = find_best_practices_issues(docs)
        findings.extend(bp_issues)
    except Exception:
        logger.exception("Best practices check failed")

    # security checks
    try:
        sec_issues = find_security_issues(docs)
        findings.extend(sec_issues)
    except Exception:
        logger.exception("Security checks failed")

    result = build_report(findings)
    return result

# backend/app/admission/webhook_handler.py
"""
A small admission webhook handler that accepts AdmissionReview v1 JSON and returns
AdmissionReview v1 response. This file focuses on the decision logic and uses the
same analyzer modules. The HTTP server wiring is done by FastAPI endpoints in main
(if you choose to mount it there) or by using a small separate ASGI app.
"""
import logging
from typing import Dict, Any
from app.analyzer.parser import parse_yaml_documents
from app.analyzer.best_practices import find_best_practices_issues
from app.analyzer.security_checks import find_security_issues
from app.analyzer.schema_validator import validate_schema_for_docs

logger = logging.getLogger("k8s-yaml-analyzer.admission")

def admission_review_response(admission_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Accepts the parsed admission review request dict and returns a dict ready to be JSON serialized.
    This function is framework-agnostic (FastAPI/Routing just calls it).
    """
    uid = admission_request.get("uid")
    # Kubernetes AdmissionReview encodes the object under request.object (a dict)
    req_object = admission_request.get("object") or admission_request.get("oldObject") or {}
    # Convert object to YAML and re-parse to keep same analyzer flow (or create list with single dict)
    docs = [req_object]  # we will treat a single object as one doc

    findings = []
    try:
        findings.extend(validate_schema_for_docs(docs))
    except Exception:
        logger.exception("schema validation exception in webhook")
    try:
        findings.extend(find_best_practices_issues(docs))
    except Exception:
        logger.exception("best practices exception in webhook")
    try:
        findings.extend(find_security_issues(docs))
    except Exception:
        logger.exception("security checks exception in webhook")

    # Decide: deny if any finding severity is HIGH or CRITICAL
    deny = False
    messages = []
    for f in findings:
        sev = getattr(f, "severity", "").upper() if hasattr(f, "severity") else f.get("severity", "").upper()
        messages.append(f"{getattr(f,'rule_id', getattr(f,'rule_id', None))}: {getattr(f,'message', str(f))}")
        if sev in ("HIGH", "CRITICAL"):
            deny = True

    if deny:
        response = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": False,
                "status": {
                    "code": 403,
                    "message": "Admission denied by k8s-yaml-analyzer: " + "; ".join(messages)
                }
            }
        }
    else:
        response = {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "uid": uid,
                "allowed": True
            }
        }

    return response

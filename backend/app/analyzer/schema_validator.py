# backend/app/analyzer/schema_validator.py
from typing import List, Dict, Any
from app.utils.kubernetes_schema import basic_k8s_resource_checks
from app.api.v1.models import Finding

def validate_schema_for_docs(docs: List[Dict[str, Any]]) -> List[Finding]:
    """
    Perform light-weight schema/shape checks.
    This is intentionally conservative and offline — it doesn't fetch the full
    Kubernetes OpenAPI schema. For production you can wire up the k8s OpenAPI spec.
    """
    findings = []
    for idx, doc in enumerate(docs):
        # ensure required top-level keys exist
        kind = doc.get("kind")
        api_version = doc.get("apiVersion")
        metadata = doc.get("metadata")
        if not kind or not api_version or not metadata:
            findings.append(Finding(
                rule_id="S001",
                title="Kubernetes resource missing top-level fields",
                message="Resource missing one of: kind, apiVersion, metadata",
                severity="MEDIUM",
                path=None,
                doc_index=idx
            ))
            # skip deeper checks for this doc
            continue

        # run basic K8s resource checks (a handful of heuristics)
        issues = basic_k8s_resource_checks(doc, idx)
        findings.extend(issues)
    return findings

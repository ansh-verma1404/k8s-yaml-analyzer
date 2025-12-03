from typing import List, Dict, Any
from k8s_analyzer.api.v1.models import Finding


def validate_schema_for_docs(docs: List[Dict[str, Any]]) -> List[Finding]:
    findings = []

    for idx, doc in enumerate(docs):

        kind = doc.get("kind")
        api_version = doc.get("apiVersion")
        metadata = doc.get("metadata")

        # CRITICAL errors
        if not kind or not api_version or not metadata:
            findings.append(Finding(
                rule_id="SCHEMA_001",
                title="Missing required top-level fields",
                message="Missing one of: kind, apiVersion, metadata",
                severity="CRITICAL",
                path=None,
                doc_index=idx
            ))
            continue

        # MEDIUM: missing metadata.name
        if not metadata.get("name"):
            findings.append(Finding(
                rule_id="SCHEMA_002",
                title="Missing metadata.name",
                message="Resource does not specify metadata.name",
                severity="MEDIUM",
                path="metadata.name",
                doc_index=idx
            ))

        # LOW: missing labels
        labels = metadata.get("labels", {})
        if not labels:
            findings.append(Finding(
                rule_id="SCHEMA_003",
                title="Missing labels",
                message="Resource has no metadata.labels (recommended for selectors and grouping)",
                severity="LOW",
                path="metadata.labels",
                doc_index=idx
            ))

    return findings

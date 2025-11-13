# backend/app/utils/kubernetes_schema.py
from typing import Dict, Any, List
from app.api.v1.models import Finding

def basic_k8s_resource_checks(doc: Dict[str, Any], doc_index: int) -> List[Finding]:
    """
    A few lightweight heuristics that approximate schema problems:
     - For Deployment/DaemonSet/StatefulSet ensure spec.template.spec exists and has containers
     - For Pod ensure spec.containers exist
     - For Service ensure spec.ports exists
    This is not a replacement for full OpenAPI schema validation.
    """
    findings = []
    kind = (doc.get("kind") or "").lower()
    spec = doc.get("spec", {}) or {}

    if kind in ("deployment", "daemonset", "statefulset"):
        template = spec.get("template")
        if not template:
            findings.append(Finding(
                rule_id="S002",
                title="Missing template in workload spec",
                message=f"{doc.get('kind')} missing spec.template",
                severity="MEDIUM",
                path="spec.template",
                doc_index=doc_index
            ))
        else:
            pod_spec = template.get("spec") or {}
            if not pod_spec.get("containers"):
                findings.append(Finding(
                    rule_id="S003",
                    title="No containers in workload template spec",
                    message=f"{doc.get('kind')} spec.template.spec has no containers",
                    severity="MEDIUM",
                    path="spec.template.spec.containers",
                    doc_index=doc_index
                ))

    if kind == "pod":
        if not spec.get("containers"):
            findings.append(Finding(
                rule_id="S004",
                title="Pod has no containers",
                message="Pod.spec.containers is empty or missing",
                severity="MEDIUM",
                path="spec.containers",
                doc_index=doc_index
            ))

    if kind == "service":
        if not spec.get("ports"):
            findings.append(Finding(
                rule_id="S005",
                title="Service missing ports",
                message="Service.spec.ports is empty or missing",
                severity="MEDIUM",
                path="spec.ports",
                doc_index=doc_index
            ))

    return findings

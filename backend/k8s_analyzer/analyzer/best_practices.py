# backend/app/analyzer/best_practices.py
from typing import List, Dict, Any
from k8s_analyzer.api.v1.models import Finding

def find_best_practices_issues(docs: List[Dict[str, Any]]) -> List[Finding]:
    findings = []
    for idx, doc in enumerate(docs):
        kind = (doc.get("kind") or "").lower()
        # check for resource limits/requests in pod spec containers
        spec = doc.get("spec", {})
        # handle Pod direct and template patterns
        pod_spec = None
        if kind == "pod":
            pod_spec = spec
        else:
            tpl = spec.get("template") or {}
            pod_spec = tpl.get("spec") or spec

        if pod_spec:
            containers = pod_spec.get("containers", []) or []
            for i, c in enumerate(containers):
                resources = c.get("resources", {})
                if not resources or not resources.get("limits") or not resources.get("requests"):
                    findings.append(Finding(
                        rule_id="BP001",
                        title="Missing CPU/memory requests or limits",
                        message=f"Container '{c.get('name', str(i))}' missing resources.requests or resources.limits",
                        severity="MEDIUM",
                        path=f"spec.template.spec.containers[{i}].resources" if kind != "pod" else f"spec.containers[{i}].resources",
                        doc_index=idx
                    ))

        # prefer explicit image tags (detect implicit latest)
        # handled more in security checks, but a lighter warning here:
        if pod_spec:
            for i, c in enumerate(pod_spec.get("containers", []) or []):
                image = c.get("image", "")
                if image and (image.endswith(":latest") or ":" not in image):
                    findings.append(Finding(
                        rule_id="BP002",
                        title="Use explicit image tags",
                        message=f"Container '{c.get('name', str(i))}' uses ':latest' or no tag: {image}",
                        severity="LOW",
                        path=f"spec.template.spec.containers[{i}].image" if kind != "pod" else f"spec.containers[{i}].image",
                        doc_index=idx
                    ))

    return findings

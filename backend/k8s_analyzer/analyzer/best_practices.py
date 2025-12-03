from typing import List, Dict, Any
from k8s_analyzer.api.v1.models import Finding


def find_best_practices_issues(docs: List[Dict[str, Any]]) -> List[Finding]:
    findings = []

    for idx, doc in enumerate(docs):
        kind = (doc.get("kind") or "").lower()
        spec = doc.get("spec", {})

        # Determine PodSpec
        if kind == "pod":
            pod_spec = spec
        else:
            pod_spec = spec.get("template", {}).get("spec", {})

        if not pod_spec:
            continue

        containers = pod_spec.get("containers", []) or []

        # -------------------------------------------------------------------
        # BP_001: Missing requests/limits
        # -------------------------------------------------------------------
        for i, c in enumerate(containers):
            res = c.get("resources", {})
            if not res or not res.get("requests") or not res.get("limits"):
                findings.append(Finding(
                    rule_id="BP_001",
                    title="Missing CPU/Memory requests or limits",
                    message=f"Container '{c.get('name', str(i))}' does not define resources.requests and resources.limits",
                    severity="MEDIUM",
                    path=f"spec.containers[{i}].resources",
                    doc_index=idx
                ))

        # -------------------------------------------------------------------
        # BP_002: Image tag (ONLY place for image tag check)
        # -------------------------------------------------------------------
        for i, c in enumerate(containers):
            image = c.get("image", "")
            if image and (":" not in image or image.endswith(":latest")):
                findings.append(Finding(
                    rule_id="BP_002",
                    title="Use explicit image tags",
                    message=f"Container '{c.get('name', str(i))}' uses ':latest' or no tag: {image}",
                    severity="LOW",
                    path=f"spec.containers[{i}].image",
                    doc_index=idx
                ))

    return findings

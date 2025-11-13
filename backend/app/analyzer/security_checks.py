# backend/app/analyzer/security_checks.py
from typing import List, Dict, Any
from app.api.v1.models import Finding

def find_security_issues(docs: List[Dict[str, Any]]) -> List[Finding]:
    """
    SAST-style security checks on the resource dicts.
    """
    findings: List[Finding] = []

    for idx, doc in enumerate(docs):
        kind = (doc.get("kind") or "").lower()
        spec = doc.get("spec", {})
        # find pod spec
        if kind == "pod":
            pod_spec = spec
        else:
            template = spec.get("template") or {}
            pod_spec = template.get("spec") or spec

        # check containers
        if pod_spec:
            for i, c in enumerate(pod_spec.get("containers", []) or []):
                cname = c.get("name", f"container[{i}]")
                # image tag
                image = c.get("image", "")
                if image and (image.endswith(":latest") or ":" not in image):
                    findings.append(Finding(
                        rule_id="SEC001",
                        title="Avoid :latest or implicit image tags",
                        message=f"Container '{cname}' uses latest/implicit tag: {image}",
                        severity="LOW",
                        path=f"spec.template.spec.containers[{i}].image" if kind != "pod" else f"spec.containers[{i}].image",
                        doc_index=idx
                    ))
                # privileged
                sc = c.get("securityContext") or {}
                if sc.get("privileged") is True:
                    findings.append(Finding(
                        rule_id="SEC002",
                        title="Avoid privileged containers",
                        message=f"Container '{cname}' has securityContext.privileged=true",
                        severity="HIGH",
                        path=f"spec.template.spec.containers[{i}].securityContext.privileged" if kind != "pod" else f"spec.containers[{i}].securityContext.privileged",
                        doc_index=idx
                    ))
                # runAsNonRoot
                ran_nr = sc.get("runAsNonRoot")
                run_user = sc.get("runAsUser")
                if ran_nr is False or (ran_nr is None and (run_user is None or run_user == 0)):
                    findings.append(Finding(
                        rule_id="SEC003",
                        title="Containers should not run as root",
                        message=f"Container '{cname}' does not enforce non-root user (runAsNonRoot missing/false or runAsUser=0)",
                        severity="MEDIUM",
                        path=f"spec.template.spec.containers[{i}].securityContext" if kind != "pod" else f"spec.containers[{i}].securityContext",
                        doc_index=idx
                    ))

                # hostPath volumes (indirect check)
                volumes = pod_spec.get("volumes", []) or []
                for vi, v in enumerate(volumes):
                    if "hostPath" in v:
                        findings.append(Finding(
                            rule_id="SEC004",
                            title="Avoid hostPath volumes",
                            message=f"Pod uses hostPath volume '{v.get('name', 'unknown')}', can expose host filesystem",
                            severity="HIGH",
                            path=f"spec.template.spec.volumes[{vi}]" if kind != "pod" else f"spec.volumes[{vi}]",
                            doc_index=idx
                        ))

        # secrets & configmaps checks
        if kind == "secret":
            # if stringData present (cleartext)
            if doc.get("stringData"):
                findings.append(Finding(
                    rule_id="SEC005",
                    title="Secret contains stringData (cleartext)",
                    message="Secret has stringData which stores clear-text secret values; prefer base64-encoded data or external secret store",
                    severity="CRITICAL",
                    path="stringData",
                    doc_index=idx
                ))
            # data should be base64 - we do a best-effort check
            data = doc.get("data", {}) or {}
            for key, val in data.items():
                if not isinstance(val, str):
                    findings.append(Finding(
                        rule_id="SEC006",
                        title="Secret data not base64 string",
                        message=f"Secret.data.{key} is not a base64 string",
                        severity="CRITICAL",
                        path=f"data.{key}",
                        doc_index=idx
                    ))

        if kind == "configmap":
            data = doc.get("data", {}) or {}
            for key in data.keys():
                lk = key.lower()
                if "password" in lk or "secret" in lk or "token" in lk or "key" in lk:
                    findings.append(Finding(
                        rule_id="SEC007",
                        title="ConfigMap contains likely secret-like keys",
                        message=f"ConfigMap key '{key}' may contain sensitive data; do not store secrets in ConfigMap",
                        severity="CRITICAL",
                        path=f"data.{key}",
                        doc_index=idx
                    ))

    return findings

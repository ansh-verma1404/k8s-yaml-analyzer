from typing import List, Dict, Any
from k8s_analyzer.api.v1.models import Finding


def find_security_issues(docs: List[Dict[str, Any]]) -> List[Finding]:
    findings = []

    for idx, doc in enumerate(docs):
        kind = (doc.get("kind") or "").lower()
        spec = doc.get("spec", {})

        # Determine PodSpec
        if kind == "pod":
            pod_spec = spec
        else:
            pod_spec = spec.get("template", {}).get("spec", {})

        # No pod spec = skip container/security checks
        if pod_spec:
            containers = pod_spec.get("containers", []) or []

            # SEC_001: Privileged containers
            for i, c in enumerate(containers):
                sc = c.get("securityContext", {})
                if sc.get("privileged") is True:
                    findings.append(Finding(
                        rule_id="SEC_001",
                        title="Privileged container detected",
                        message=f"Container '{c.get('name', str(i))}' has privileged=true",
                        severity="HIGH",
                        path=f"spec.containers[{i}].securityContext.privileged",
                        doc_index=idx
                    ))

            # SEC_002: Running as root
            for i, c in enumerate(containers):
                sc = c.get("securityContext", {})
                ran_nr = sc.get("runAsNonRoot")
                run_user = sc.get("runAsUser")

                if ran_nr is False or (run_user == 0) or (ran_nr is None and run_user is None):
                    findings.append(Finding(
                        rule_id="SEC_002",
                        title="Container may run as root",
                        message=f"Container '{c.get('name', str(i))}' does not enforce non-root execution",
                        severity="MEDIUM",
                        path=f"spec.containers[{i}].securityContext",
                        doc_index=idx
                    ))

            # SEC_003: HostPath (only once per Pod)
            volumes = pod_spec.get("volumes", [])
            for v in volumes:
                if "hostPath" in v:
                    findings.append(Finding(
                        rule_id="SEC_003",
                        title="Use of hostPath volume",
                        message=f"Pod uses hostPath volume '{v.get('name','unknown')}'. This risks host filesystem exposure.",
                        severity="HIGH",
                        path="spec.volumes",
                        doc_index=idx
                    ))
                    break  # avoid duplicates

        # -------------------------------------------------------------------
        # Secret checks
        # -------------------------------------------------------------------
        if kind == "secret":
            if doc.get("stringData"):
                findings.append(Finding(
                    rule_id="SEC_004",
                    title="Secret contains stringData",
                    message="stringData stores cleartext secrets",
                    severity="CRITICAL",
                    path="stringData",
                    doc_index=idx
                ))

        # -------------------------------------------------------------------
        # ConfigMap dangerous keys
        # -------------------------------------------------------------------
        if kind == "configmap":
            for key in (doc.get("data") or {}):
                if any(x in key.lower() for x in ["password", "secret", "token", "key"]):
                    findings.append(Finding(
                        rule_id="SEC_005",
                        title="Suspicious key in ConfigMap",
                        message=f"Key '{key}' in ConfigMap appears to contain sensitive data",
                        severity="CRITICAL",
                        path=f"data.{key}",
                        doc_index=idx
                    ))

    return findings

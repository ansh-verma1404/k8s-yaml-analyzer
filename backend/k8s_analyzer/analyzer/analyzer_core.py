from typing import List, Dict, Tuple, Set
from k8s_analyzer.api.v1.models import Finding

SEVERITY_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}

def dedupe_findings(findings: List[Finding]) -> List[Finding]:
    """Remove duplicate findings by (rule_id, doc_index, path, message)."""
    seen: Set[Tuple[str, int, str, str]] = set()
    result = []

    for f in findings:
        key = (
            f.rule_id,
            f.doc_index or -1,
            f.path or "",
            f.message or "",
        )
        if key not in seen:
            seen.add(key)
            result.append(f)

    return result


def analyze_all(docs) -> List[Finding]:
    """Unified entrypoint used by FastAPI & CLI."""
    from k8s_analyzer.analyzer.schema_validator import validate_schema_for_docs
    from k8s_analyzer.analyzer.best_practices import find_best_practices_issues
    from k8s_analyzer.analyzer.security_checks import find_security_issues

    all_findings: List[Finding] = []
    all_findings.extend(validate_schema_for_docs(docs))
    all_findings.extend(find_best_practices_issues(docs))
    all_findings.extend(find_security_issues(docs))

    # Remove duplicates across all validators
    final = dedupe_findings(all_findings)
    return final

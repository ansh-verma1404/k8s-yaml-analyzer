from typing import List
from collections import Counter
from k8s_analyzer.api.v1.models import ScanResult, Finding


def build_report(findings_list: List[Finding]) -> ScanResult:
    normalized = [
        f if isinstance(f, Finding) else Finding(**f)
        for f in findings_list
    ]

    summary_counter = Counter(f.severity.upper() for f in normalized)

    summary = {
        "CRITICAL": summary_counter.get("CRITICAL", 0),
        "HIGH": summary_counter.get("HIGH", 0),
        "MEDIUM": summary_counter.get("MEDIUM", 0),
        "LOW": summary_counter.get("LOW", 0),
    }

    fail = summary["CRITICAL"] > 0 or summary["HIGH"] > 0

    return ScanResult(
        ok=not fail,
        findings=normalized,
        summary=summary
    )

# backend/app/analyzer/report.py
from typing import List, Dict
from k8s_analyzer.api.v1.models import ScanResult, Finding
from collections import Counter

def build_report(findings_list: List[Finding]) -> ScanResult:
    # findings_list may contain either Finding pydantic objects or dict-like objects;
    normalized = []
    for f in findings_list:
        if isinstance(f, Finding):
            normalized.append(f)
        else:
            # dict
            normalized.append(Finding(**f))

    summary_counter = Counter()
    for f in normalized:
        summary_counter[f.severity.upper()] += 1

    # ensure keys for standard severities
    summary = {
        "CRITICAL": summary_counter.get("CRITICAL", 0),
        "HIGH": summary_counter.get("HIGH", 0),
        "MEDIUM": summary_counter.get("MEDIUM", 0),
        "LOW": summary_counter.get("LOW", 0),
    }

    return ScanResult(ok=True, findings=normalized, summary=summary)

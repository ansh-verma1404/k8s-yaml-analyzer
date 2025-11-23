#!/usr/bin/env python3
"""
Simple CLI to scan kube YAML files locally.

Usage:
    python cli.py file1.yaml file2.yaml ...
Exit codes:
    0 : no findings (or only LOW)
    1 : usage/parse error
    2 : findings include MEDIUM or HIGH (configurable)
    3 : critical findings detected
"""
import sys
import json
from typing import List
from k8s_analyzer.analyzer.parser import parse_yaml_documents
from k8s_analyzer.analyzer.schema_validator import validate_schema_for_docs
from k8s_analyzer.analyzer.best_practices import find_best_practices_issues
from k8s_analyzer.analyzer.security_checks import find_security_issues
from k8s_analyzer.analyzer.report import build_report

def scan_text(text: str):
    docs = parse_yaml_documents(text)
    findings = []
    findings.extend(validate_schema_for_docs(docs))
    findings.extend(find_best_practices_issues(docs))
    findings.extend(find_security_issues(docs))
    return findings

def main(argv: List[str]):
    if len(argv) < 2:
        print("Usage: cli.py <file1.yaml> [file2.yaml ...]")
        return 1
    overall_findings = []
    for path in argv[1:]:
        try:
            with open(path, "r") as fh:
                txt = fh.read()
        except Exception as e:
            print(f"Failed to read {path}: {e}", file=sys.stderr)
            return 1
        try:
            findings = scan_text(txt)
            overall_findings.extend(findings)
        except Exception as e:
            print(f"Error scanning {path}: {e}", file=sys.stderr)
            return 1

    report = build_report(overall_findings)
    # print JSON report
    print(report.json(indent=2, ensure_ascii=False))

    # determine exit code: 3=CRITICAL,2=HIGH/MEDIUM,0 otherwise
    if report.summary.get("CRITICAL", 0) > 0:
        return 3
    if report.summary.get("HIGH", 0) > 0 or report.summary.get("MEDIUM", 0) > 0:
        return 2
    return 0

if __name__ == "__main__":
    rc = main(sys.argv)
    sys.exit(rc)

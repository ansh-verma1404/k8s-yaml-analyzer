# backend/app/api/v1/models.py
from typing import Optional, List, Dict
from pydantic import BaseModel

class Finding(BaseModel):
    rule_id: str
    title: str
    message: str
    severity: str
    path: Optional[str] = None
    doc_index: Optional[int] = None

class ScanResult(BaseModel):
    ok: bool
    findings: List[Finding]
    summary: Dict[str, int]

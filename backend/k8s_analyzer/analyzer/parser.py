# backend/app/analyzer/parser.py
from typing import List, Dict, Any
import yaml

def parse_yaml_documents(yaml_text: str) -> List[Dict[str, Any]]:
    docs = list(yaml.safe_load_all(yaml_text))
    docs = [d for d in docs if d is not None]
    return docs

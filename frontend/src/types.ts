export interface Finding {
  rule_id: string;
  title: string;
  message: string;
  severity: string;
  path?: string;
  doc_index?: number;
}

export interface ScanResult {
  ok: boolean;
  findings: Finding[];
  summary: Record<string, number>;
}

import axios from "axios";
import type { ScanResult } from "./types";

// API endpoint that nginx proxies to backend
const API_BASE = "/api";

export async function scanYaml(file: File): Promise<ScanResult> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(`${API_BASE}/v1/scan`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
}

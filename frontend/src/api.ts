import axios from "axios";
import type { ScanResult } from "./types";

// use relative path so vite proxy works
const API_BASE = "/api";

export async function scanYaml(file: File): Promise<ScanResult> {
  const form = new FormData();
  form.append("file", file);
  const res = await axios.post(`${API_BASE}/v1/scan`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

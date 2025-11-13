import React, { useState } from "react";
import { scanYaml } from "../api";
import type { ScanResult } from "../types";

interface Props {
  onResult: (res: ScanResult, yamlText: string) => void;
}

const FileUploader: React.FC<Props> = ({ onResult }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    setError(null);

    const text = await file.text();

    try {
      const result = await scanYaml(file);
      onResult(result, text);
    } catch (err: unknown) {
      console.error(err);
      setError("Failed to scan YAML");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input type="file" accept=".yaml,.yml" onChange={handleUpload} />
      {loading && <p>Scanning...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default FileUploader;

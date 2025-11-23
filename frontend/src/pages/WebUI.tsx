import { useState } from "react";
import FileUploader from "../components/FileUploader";
import FindingsTable from "../components/FindingsTable";
import YamlViewer from "../components/YamlViewer";
import type { ScanResult } from "../types";

export default function WebUI() {
  const [result, setResult] = useState<ScanResult | null>(null);
  const [yamlText, setYamlText] = useState("");

  return (
    <div className="app">
      <h1>Web UI — K8s YAML Analyzer</h1>
      <p>Upload your YAML file and get instant scan results.</p>

      <FileUploader
        onResult={(res, text) => {
          setResult(res);
          setYamlText(text);
        }}
      />

      {result && (
        <div>
          <h2>Summary</h2>
          <ul style={{ display: "flex", gap: "1rem" }}>
            {Object.entries(result.summary).map(([sev, count]) => (
              <li key={sev}>
                <strong>{sev}</strong>: {count}
              </li>
            ))}
          </ul>

          <FindingsTable findings={result.findings} />
          <YamlViewer yamlText={yamlText} />
        </div>
      )}
    </div>
  );
}

import { useState } from "react";
import FileUploader from "./components/FileUploader";
import FindingsTable from "./components/FindingsTable";
import YamlViewer from "./components/YamlViewer";
import type { ScanResult } from "./types";
import "./index.css";

function App() {
  const [result, setResult] = useState<ScanResult | null>(null);
  const [yamlText, setYamlText] = useState<string>("");

  return (
    <div className="app">
      <h1>K8s YAML Analyzer</h1>
      <p>Upload a Kubernetes YAML to validate and visualize findings.</p>

      <FileUploader
        onResult={(res, text) => {
          setResult(res);
          setYamlText(text);
        }}
      />

      {result && (
        <>
          <div>
            <h2>Summary</h2>
            <ul style={{ display: "flex", gap: "1rem", listStyle: "none" }}>
              {Object.entries(result.summary).map(([sev, count]) => (
                <li key={sev}>
                  <strong>{sev}</strong>: {count}
                </li>
              ))}
            </ul>
          </div>

          <FindingsTable findings={result.findings} />
          <YamlViewer yamlText={yamlText} />
        </>
      )}
    </div>
  );
}

export default App;

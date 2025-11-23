export default function CLITool() {
  return (
    <div className="app">
      <h1>CLI Tool — k8s-yaml-cli</h1>
      <p>Use analyzer via command line.</p>

      <h2>Install</h2>
      <pre>
        pip install k8s-yaml-analyzer
      </pre>

      <h2>Scan YAML file</h2>
      <pre>
        k8s-yaml scan deployment.yaml
      </pre>

      <h2>Output Example</h2>
      <pre>
{`CRITICAL: privileged container detected
HIGH: image tag 'latest' not recommended
LOW: consider adding resource limits`}
      </pre>
    </div>
  );
}

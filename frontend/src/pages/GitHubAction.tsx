export default function GitHubAction() {
  return (
    <div className="app">
      <h1>GitHub Action — CI/CD Plugin</h1>
      <p>Automatically scan Kubernetes YAML in pipelines.</p>

      <h2>workflow.yaml</h2>
      <pre>
{`name: YAML Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Analyzer
        uses: ansh-verma1404/k8s-yaml-analyzer-action@v1
        with:
          path: manifests/`}
      </pre>

      <h2>Use Case</h2>
      <p>Fails the pipeline if insecure YAML is detected.</p>
    </div>
  );
}

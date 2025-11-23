export default function AdmissionController() {
  return (
    <div className="app">
      <h1>Kubernetes Admission Controller</h1>
      <p>Block insecure YAML at deployment-time in your cluster.</p>

      <h2>Install Webhook</h2>
      <pre>
{`kubectl apply -f admission-controller.yaml`}
      </pre>

      <h2>Flow</h2>
      <pre>
{`kubectl apply -> K8s API Server -> Webhook (Analyzer) -> Allow/Deny`}
      </pre>

      <h2>Example Rejection</h2>
      <pre>
{`ERROR: privileged container blocked
Reason: Violates security best practices`}
      </pre>
    </div>
  );
}

export default function AdmissionController() {
  return (
    <div className="app">
      <h1>Kubernetes Admission Controller</h1>
      <p>Block insecure YAML at deployment-time in your cluster.</p>

      <h2>Deploy Webhook backend</h2>
      <pre>
{'kubectl apply -f webhook-deployment.yaml  kubectl apply -f webhook-service.yaml'}
      </pre>

      <h2>Flow</h2>
      <pre>
{`kubectl create secret tls webhook-tls \
  --cert=tls.crt \
  --key=tls.key \
  -n <namespace-name>
`}
      </pre>

      <h2>Install webhook configuration</h2>
      <pre>
{`kubectl apply -f webhook-config.yaml
`}
      </pre>
    </div>
  );
}

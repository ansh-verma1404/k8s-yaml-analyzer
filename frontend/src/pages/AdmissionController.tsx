export default function AdmissionController() {
  return (
    <div className="app">
      <h1>Kubernetes Admission Controller</h1>
      <p>Block insecure Kubernetes YAML at deployment-time using our admission webhook.</p>

      <h2>1. Deploy Webhook Backend</h2>
      <pre>
{`kubectl apply -f k8s-manifests/webhook-deployment.yaml
kubectl apply -f k8s-manifests/webhook-service.yaml
`}
      </pre>

      <h2>2. Create TLS Secret for Webhook</h2>
      <pre>
{`kubectl create secret tls analyzer-webhook-tls \\
  --cert=tls.crt \\
  --key=tls.key \\
  -n default
`}
      </pre>

      <h2>3. Install Mutating/Validating Admission Webhook Configuration</h2>
      <pre>
{`kubectl apply -f k8s-manifests/admission-webhook.yaml
`}
      </pre>

      <h2>4. Test the webhook</h2>
      <pre>
{`kubectl apply -f test-manifests/insecure-pod.yaml
# Should be denied

kubectl apply -f test-manifests/secure-pod.yaml
# Should be allowed
`}
      </pre>
    </div>
  );
}

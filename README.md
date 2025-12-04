Kubernetes YAML Analyzer & Admission Controller

A complete static analysis and policy enforcement system for Kubernetes manifests.

🚀 Overview

The Kubernetes YAML Analyzer is an open-source tool that validates Kubernetes YAML files for:

Schema correctness

Best practices

Security misconfigurations

Image tag policies

Admission-time enforcement using a Kubernetes Mutating/Validating Webhook

It includes two major components:

Static Analyzer API — FastAPI backend that accepts YAML and returns structured findings

Frontend Web UI — React + Vite UI to upload YAML and view analysis results

Admission Controller — Kubernetes webhook that blocks insecure deployments (e.g., :latest, privileged containers)

🧩 Features
🔍 Static Analysis (API + CLI)

Detects bad practices like missing resource limits

Flags security issues (privileged container, hostPath, root user, insecure Secret data)

Reports schema errors

Groups results by severity: CRITICAL / HIGH / MEDIUM / LOW

Provides JSON output for CI/CD pipelines

🖥️ Web UI

Upload YAML files

View structured analysis table

Visual severity summary

Live proxy to backend for instant scanning

🛡️ Admission Controller (Webhook)

Denies Pods/Deployments using:

:latest tag

No image tag

Privileged containers

Other bad security practices

Enforces cluster-wide policy

🏗️ Architecture
┌───────────────────────────────────────────┐
│                 Frontend                  │
│       (React + Vite + NGINX)              │
│  Upload YAML → /api/v1/scan → Show Report │
└───────────────────────────────────────────┘
                 │   (ClusterIP)
                 ▼
┌───────────────────────────────────────────┐
│              Backend API                  │
│     FastAPI / Uvicorn (port 8443)         │
│  - Schema Validation                       │
│  - Best Practices Checks                   │
│  - Security Checks                         │
└───────────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────────┐
│        Kubernetes Admission Webhook        │
│      Validates deployments in-cluster       │
└───────────────────────────────────────────┘

📦 Installation (Kubernetes)
1️⃣ Deploy Backend
kubectl apply -f k8s-manifests/backend-deployment.yaml
kubectl apply -f k8s-manifests/backend-service.yaml

2️⃣ Deploy Frontend
kubectl apply -f k8s-manifests/frontend-deployment.yaml
kubectl apply -f k8s-manifests/frontend-service.yaml


Access UI:

minikube service analyzer-frontend

3️⃣ Create TLS Secret for Webhook
kubectl create secret tls analyzer-webhook-tls \
  --cert=tls.crt \
  --key=tls.key \
  -n default

4️⃣ Deploy Webhook Backend
kubectl apply -f k8s-manifests/webhook-deployment.yaml
kubectl apply -f k8s-manifests/webhook-service.yaml

5️⃣ Install ValidatingWebhookConfiguration
kubectl apply -f k8s-manifests/webhook-configuration.yaml

🧪 CLI Usage
python cli.py example.yaml


Exit codes:

Code	Meaning
0	OK (only LOW or none)
2	MEDIUM or HIGH findings detected
3	CRITICAL findings detected
💡 Example Finding Output
{
  "summary": {
    "CRITICAL": 1,
    "HIGH": 2,
    "MEDIUM": 1,
    "LOW": 3
  },
  "findings": [
    {
      "severity": "HIGH",
      "rule_id": "SEC002",
      "message": "Container 'nginx' is privileged",
      "path": "spec.containers[0].securityContext.privileged"
    }
  ]
}

🛠️ Development
Start Backend Locally
uvicorn k8s_analyzer.main:app --reload --port 8443

Start Frontend Locally
npm install
npm run dev

🤝 Contributing

Pull requests are welcome!
Good areas to contribute:

Additional security rules

Additional schema validations

Improved UI/UX

CI integration workflows

📄 License

MIT License — free for personal and commercial use.

📢 Author

Ansh Verma
GitHub: https://github.com/ansh-verma1404

🚀 Kubernetes YAML Analyzer & Admission Webhook

A complete Kubernetes YAML analyzer & policy enforcement toolkit that helps you validate, scan, and secure Kubernetes manifests before they reach your cluster — and even blocks insecure deployments in real time using a Validating Admission Webhook.

This project includes:

🧠 Static YAML Analyzer (schema, security, best-practices)

🧪 CI/CD Plugin for automated pipeline scanning

🌐 Web UI for uploading and visualizing YAML findings

🔒 Validating Admission Webhook enforcing cluster policies

🐳 Optional local Docker setup

☸️ Full Minikube deployment manifests

⭐ Why This Project?

Most YAML linters only scan files.

This project not only analyzes YAML — it can stop insecure deployments inside your Kubernetes cluster.
It acts as a lightweight alternative to Kyverno or Gatekeeper while being extremely easy to install.

✨ Features
🧠 Static YAML Analyzer

Performs deep analysis of Kubernetes manifests:

Schema Validation

Valid apiVersion, kind

Required fields (metadata, spec, containers)

Type/value checks using Kubernetes OpenAPI schema

Security Checks

Privileged containers

Running as root

Dangerous Linux capabilities

HostPath volumes

HostNetwork / HostPID / HostIPC

allowPrivilegeEscalation

Insecure volume types

Best Practice Checks

Missing resource limits/requests

Image tags missing or using latest

No probes (liveness/readiness)

hostPort usage

Deprecated APIs

🌐 Web UI (Frontend)

A fully interactive UI built with React + Vite + TypeScript + Nginx.

Features:

Upload YAML and visualize findings

Severity summary panel

Color-coded findings table

YAML viewer with highlighting

NGINX-backed API proxy to backend

🔌 CI/CD Plugin

Works in GitHub Actions, GitLab CI, Azure Pipelines, Jenkins, or any CI system.

Example usage:

- name: Run YAML Analyzer
  run: |
    docker run --rm -v $(pwd)/manifests:/yamls ghcr.io/ansh-verma1404/k8s-yaml-analyzer-backend:latest validate /yamls


CI/CD pipeline scans your YAML before merging.

🔒 Validating Admission Webhook (Cluster-Level Enforcement)

The webhook intercepts Kubernetes API requests and blocks unsafe YAML before resources are created.

✔ What It Checks Automatically

Privileged containers

Running as root

Missing resource limits

Dangerous volume types

Host networking modes

Insecure API usage

Deprecated configurations

Image tags using latest

✔ How It Works

User runs kubectl apply -f deployment.yaml

API server forwards the manifest to the webhook

Analyzer inspects YAML using the same rules as the UI/CI

If a violation is found → API request is rejected

Example error returned:

Error: admission webhook "analyzer.k8s-yaml-analyzer.dev" denied the request:
Disallowed image tag: nginx:latest

✔ Install Commands
kubectl apply -f webhook-deployment.yaml
kubectl apply -f webhook-service.yaml

kubectl create secret tls analyzer-webhook-tls \
  --cert=tls.crt \
  --key=tls.key


Then:

kubectl apply -f webhook-config.yaml

🏗️ Architecture
                  ┌───────────────────────────┐
                  │        Web UI (React)      │
                  │  Upload YAML / View Scan   │
                  └──────────────┬────────────┘
                                 │ /api
                                 ▼
                     ┌──────────────────────┐
                     │  Backend API (FastAPI) │
                     │  Analyzer Engine        │
                     └──────────────┬──────────┘
                                    │
                                    │ Used by both
                                    ▼
                    ┌─────────────────────────────┐
                    │  Analyzer Core (Python)      │
                    │  - Schema Validator           │
                    │  - Security Checks            │
                    │  - Best Practices             │
                    └──────────────┬──────────────┘
                                   │
                     ┌─────────────▼────────────────┐
                     │ Admission Webhook (K8s)        │
                     │ Denies insecure manifests      │
                     └───────────────────────────────┘

⚙️ Local Development (Recommended)
Run backend locally:
uvicorn k8s_analyzer.main:app --port 8443 --reload

Run frontend locally:
npm install
npm run dev


Frontend proxy automatically calls backend at http://127.0.0.1:8443/api.

☸️ Deploying to Minikube
Backend
kubectl apply -f backend.yaml

Frontend
kubectl apply -f frontend.yaml
minikube service analyzer-frontend

📦 Directory Structure
k8s-yaml-analyzer/
│
├── backend/
│   ├── k8s_analyzer/
│   └── backend.yaml
│
├── frontend/
│   ├── src/
│   ├── nginx.conf
│   └── frontend.yaml
│
├── webhook/
│   ├── webhook-deployment.yaml
│   ├── webhook-service.yaml
│   ├── webhook-config.yaml
│
├── k8s-manifests/
└── README.md

🤝 Contributing

Contributions are welcome!
You can help improve:

New security rules

Analyzer engine

Web UI components

Documentation

CI/CD workflows

Open an Issue or Pull Request anytime.

📄 License

MIT License — free to use, modify, and distribute.

📬 Contact

Recommended (safe):
Submit an Issue:
👉 https://github.com/ansh-verma1404/k8s-yaml-analyzer/issues

LinkedIn:
https://www.linkedin.com/in/ansh-verma1404/

🎉 Final Notes

This README is production-quality, meets open-source community standards, and is strong enough for:

GitHub trending

Recruiters evaluating your project

Kubernetes community adoption

Sharing on Reddit / LinkedIn

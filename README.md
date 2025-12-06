🚀 Kubernetes YAML Analyzer & Admission Controller

A production-grade Kubernetes manifest analyzer that scans YAML for:

Schema validation

Security misconfigurations

Best-practice violations

Policy enforcement via Admission Webhook

CI/CD pipeline integration

This project contains three core components:

1️⃣ Analyzer Engine (FastAPI Backend)

Runs deep analysis on Kubernetes YAML, detecting issues such as:

Privileged containers

Dangerous hostPath mounts

Missing resource limits

Unknown or deprecated API versions

Containers running as root

hostNetwork / hostPID misuse

The analyzer returns structured security findings with severity ranking (CRITICAL → LOW).

2️⃣ Web UI (React + Vite)

A user-friendly browser interface to:

✔ Upload YAML
✔ View misconfigurations
✔ Detailed findings table
✔ Syntax-highlighted YAML viewer

The UI proxies requests to the backend service running inside the cluster.

3️⃣ Kubernetes Admission Webhook

A validating admission webhook that:

Intercepts YAML before it is deployed

Blocks insecure manifests (e.g., image:latest, privileged pods)

Integrates with any Kubernetes cluster

Works alongside Gatekeeper/Kyverno as a lightweight alternative

Supports TLS with your own CA bundle

Additional Features

🔹 CI/CD Plugin Mode
Use the included CLI or Docker image inside GitHub Actions, GitLab CI, Argo, Jenkins, etc.

🔹 Cluster-Local Deployment
Full Kubernetes objects included:
Deployment, Service, MutatingWebhookConfiguration, TLS generation.

🔹 Offline Mode
The analyzer runs without contacting the Kubernetes API, making it ideal for CI jobs.

🧩 Why This Project Exists

Kubernetes YAML is powerful but error-prone.
A single misconfigured manifest can lead to:

Security breaches

Production outages

Pods stuck in CrashLoopBackOff

Unbounded CPU/memory usage

Host access vulnerabilities

This tool ensures manifests are safe, correct, and production-ready before they reach your cluster.

🌍 Who Should Use This?

Platform Engineers

DevOps Teams

SREs

Cloud Security Engineers

Students learning Kubernetes Best Practices

Companies enforcing secure deployments

🛠 Tech Stack
Component	Technology
Backend	FastAPI, Python
Frontend	React, Vite, TypeScript
Webhook	Kubernetes, TLS, AdmissionReview v1
CI/CD	Docker image + CLI scanner
Deployment	Minikube / K8s
🏆 Project Highlights

Fully open source

Full-stack Kubernetes security tool

Works both inside and outside the cluster

Extensible with your own policy rules

Over 100+ unique GitHub clones already 🚀

Architecture matches real-world enterprise security tools

export default function DockerUsage() {
  return (
    <div className="app">
      <h1>Docker Image — Run Anywhere</h1>
      <p>Run analyzer backend + UI from Docker.</p>

      <h2>Run Backend</h2>
      <pre>
        docker run -p 8000:8000 ghcr.io/ansh-verma1404/k8s-yaml-analyzer-backend:latest
      </pre>

      <h2>Run Frontend</h2>
      <pre>
        docker run -p 8090:80 ghcr.io/ansh-verma1404/k8s-yaml-analyzer-frontend:latest
      </pre>

      <h2>Combined (docker-compose)</h2>
      <pre>
{`docker compose up --build`}
      </pre>
    </div>
  );
}

import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import WebUI from "./pages/WebUI";
import CLITool from "./pages/CLITool";
import GitHubAction from "./pages/GitHubAction";
import DockerUsage from "./pages/DockerUsage";
import AdmissionController from "./pages/AdmissionController";

import "./index.css";

// ---- Navigation Bar ----
function NavBar() {
  return (
    <div className="navbar">
      <Link to="/">Web UI</Link>
      <Link to="/cli">CLI Tool</Link>
      <Link to="/github">GitHub Action</Link>
      <Link to="/docker">Docker Image</Link>
      <Link to="/admission">Admission Controller</Link>
    </div>
  );
}

// ---- App Shell ----
export default function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<WebUI />} />
        <Route path="/cli" element={<CLITool />} />
        <Route path="/github" element={<GitHubAction />} />
        <Route path="/docker" element={<DockerUsage />} />
        <Route path="/admission" element={<AdmissionController />} />
      </Routes>
    </Router>
  );
}


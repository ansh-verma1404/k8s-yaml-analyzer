import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();

  const navItem = (path: string, label: string) => (
    <Link
      to={path}
      className={`nav-item ${pathname === path ? "active" : ""}`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="logo">K8s YAML Analyzer</div>
        <div className="nav-links">
          {navItem("/", "Home")}
          {navItem("/analyze", "Analyzer")}
          {navItem("/cli", "CLI Usage")}
          {navItem("/cicd", "CI/CD Guide")}
        </div>
      </div>
    </nav>
  );
}

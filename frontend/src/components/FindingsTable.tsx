import React, { useState } from "react";
import type { Finding } from "../types";
import classNames from "classnames";

interface Props {
  findings: Finding[];
}

const badgeColor = (sev: string) => {
  switch (sev.toUpperCase()) {
    case "CRITICAL":
      return "bg-red-600 text-white";
    case "HIGH":
      return "bg-orange-500 text-white";
    case "MEDIUM":
      return "bg-yellow-400 text-black";
    case "LOW":
      return "bg-green-400 text-black";
    default:
      return "bg-gray-500 text-white";
  }
};

const FindingsTable: React.FC<Props> = ({ findings }) => {
  const [filter, setFilter] = useState<string>("ALL");

  const filtered =
    filter === "ALL"
      ? findings
      : findings.filter((f) => f.severity.toUpperCase() === filter);

  return (
    <div>
      <div className="flex-header">
        <h2>Findings</h2>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="ALL">All Severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>
      </div>

      {filtered.length === 0 ? (
        <p>No findings 🎉</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Severity</th>
              <th>Rule</th>
              <th>Message</th>
              <th>Path</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((f, idx) => (
              <tr key={idx}>
                <td>
                  <span
                    className={classNames(
                      "px-2 py-1 rounded text-xs font-bold",
                      badgeColor(f.severity)
                    )}
                  >
                    {f.severity}
                  </span>
                </td>
                <td>{f.rule_id}</td>
                <td>{f.message}</td>
                <td>{f.path}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default FindingsTable;

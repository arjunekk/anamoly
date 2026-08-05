/**
 * Inspection History page: lists every past inspection, most recent first.
 *
 * Reuses the existing /inspections endpoint from Phase 11 — no new
 * backend work needed here, since that endpoint already returns full
 * history (not just a "recent 5" slice like the Dashboard does).
 */

import { useEffect, useState } from "react";
import { getHeatmapUrl } from "../api/inspectionApi";

const API_BASE_URL = "http://127.0.0.1:8000";

const SEVERITY_COLORS = {
  none: "bg-green-100 text-green-800",
  minor: "bg-yellow-100 text-yellow-800",
  moderate: "bg-orange-100 text-orange-800",
  critical: "bg-red-100 text-red-800",
};

async function fetchAllInspections() {
  const response = await fetch(`${API_BASE_URL}/inspections`);
  if (!response.ok) {
    throw new Error(`Failed to load inspection history: ${response.status}`);
  }
  return response.json();
}

export default function History() {
  const [inspections, setInspections] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAllInspections()
      .then(setInspections)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <p className="text-red-600 p-8">Error loading history: {error}</p>;
  }

  if (!inspections) {
    return <p className="text-gray-500 p-8">Loading inspection history...</p>;
  }

  if (inspections.length === 0) {
    return <p className="text-gray-500 p-8">No inspections have been run yet.</p>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        Inspection History ({inspections.length})
      </h1>

      <div className="bg-white rounded-lg border overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-gray-100 text-gray-600">
            <tr>
              <th className="p-3">Heatmap</th>
              <th className="p-3">ID</th>
              <th className="p-3">Category</th>
              <th className="p-3">Score</th>
              <th className="p-3">Severity</th>
              <th className="p-3">Timestamp</th>
              <th className="p-3">Report</th>
            </tr>
          </thead>
          <tbody>
            {inspections.map((insp) => (
              <tr key={insp.id} className="border-t hover:bg-gray-50">
                <td className="p-3">
                  <img
                    src={getHeatmapUrl(insp.heatmap_url)}
                    alt="heatmap"
                    className="w-12 h-12 object-cover rounded"
                  />
                </td>
                <td className="p-3 text-gray-600">#{insp.id}</td>
                <td className="p-3 text-gray-600">{insp.product_category}</td>
                <td className="p-3 text-gray-600">{insp.anomaly_score.toFixed(2)}</td>
                <td className="p-3">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${SEVERITY_COLORS[insp.severity] || "bg-gray-100 text-gray-800"}`}
                  >
                    {insp.severity}
                  </span>
                </td>
                <td className="p-3 text-gray-500 text-xs">
                  {new Date(insp.timestamp).toLocaleString()}
                </td>
                <td className="p-3">
                  <a
                    href={`${API_BASE_URL}/inspections/${insp.id}/report`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline text-xs"
                  >
                    Download PDF
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
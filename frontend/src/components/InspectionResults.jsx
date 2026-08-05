/**
 * Displays the results of a completed inspection: heatmap, score,
 * severity, recommendations, and a PDF report download link.
 *
 * Purely presentational — receives already-fetched data as props,
 * has no knowledge of how that data was obtained.
 */

import { getHeatmapUrl } from "../api/inspectionApi";

const SEVERITY_COLORS = {
  none: "bg-green-100 text-green-800 border-green-300",
  minor: "bg-yellow-100 text-yellow-800 border-yellow-300",
  moderate: "bg-orange-100 text-orange-800 border-orange-300",
  critical: "bg-red-100 text-red-800 border-red-300",
};

export default function InspectionResults({ result }) {
  if (!result) return null;

  const severityStyle = SEVERITY_COLORS[result.severity] || SEVERITY_COLORS.none;

  return (
    <div className="mt-8 w-full max-w-2xl flex flex-col gap-4">
      <img
        src={getHeatmapUrl(result.heatmap_url)}
        alt="Anomaly heatmap"
        className="w-full rounded-lg border"
      />

      <div className="flex items-center justify-between">
        <span className="text-gray-600">
          Anomaly Score: <span className="font-semibold">{result.anomaly_score.toFixed(2)}</span>
        </span>

        <span className={`px-3 py-1 rounded-full text-sm font-medium border ${severityStyle}`}>
          {result.severity.toUpperCase()}
        </span>
      </div>

      <a
        href={`http://127.0.0.1:8000/inspections/${result.id}/report`}
        target="_blank"
        rel="noopener noreferrer"
        className="text-center px-4 py-2 bg-gray-700 text-white rounded-md hover:bg-gray-800 transition text-sm"
      >
        Download PDF Report
      </a>

      <div className="bg-gray-50 rounded-lg p-4 border">
        <h3 className="font-semibold text-gray-700 mb-2">Recommended Actions</h3>
        <ul className="list-disc list-inside text-gray-600 space-y-1">
          {result.recommendations.map((rec, index) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
/**
 * Dashboard page: shows aggregate inspection statistics.
 */

import { useEffect, useState } from "react";
import { fetchDashboard } from "../api/dashboardApi";
import { getHeatmapUrl } from "../api/inspectionApi";

const SEVERITY_COLORS = {
  none: "bg-green-100 text-green-800",
  minor: "bg-yellow-100 text-yellow-800",
  moderate: "bg-orange-100 text-orange-800",
  critical: "bg-red-100 text-red-800",
};

function StatCard({ label, value }) {
  return (
    <div className="bg-white rounded-lg border p-4 flex flex-col gap-1">
      <span className="text-sm text-gray-500">{label}</span>
      <span className="text-2xl font-semibold text-gray-800">{value}</span>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <p className="text-red-600 p-8">Error loading dashboard: {error}</p>;
  }

  if (!data) {
    return <p className="text-gray-500 p-8">Loading dashboard...</p>;
  }

  const { stats, recent_inspections, score_trend } = data;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {/* Summary stat cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Inspections" value={stats.total_inspections} />
        <StatCard label="Defect Rate" value={`${stats.defect_rate}%`} />
        <StatCard label="Avg Anomaly Score" value={stats.average_anomaly_score} />
        <StatCard
          label="Categories Tracked"
          value={Object.keys(stats.category_stats).length}
        />
      </div>

      {/* Severity distribution */}
      <div className="bg-white rounded-lg border p-4 mb-8">
        <h2 className="font-semibold text-gray-700 mb-3">Severity Distribution</h2>
        <div className="flex gap-3 flex-wrap">
          {Object.entries(stats.severity_distribution).map(([severity, count]) => (
            <span
              key={severity}
              className={`px-3 py-1 rounded-full text-sm font-medium ${SEVERITY_COLORS[severity] || "bg-gray-100 text-gray-800"}`}
            >
              {severity}: {count}
            </span>
          ))}
        </div>
      </div>

      {/* Score trend (simple list-based visualization, no charting library) */}
      <div className="bg-white rounded-lg border p-4 mb-8">
        <h2 className="font-semibold text-gray-700 mb-3">Recent Score Trend</h2>
        <div className="flex items-end gap-1 h-32">
          {score_trend.map((point, i) => (
            <div
              key={i}
              title={`${point.anomaly_score.toFixed(1)}`}
              className="bg-blue-400 rounded-t w-4"
              style={{ height: `${Math.min(point.anomaly_score, 100)}%` }}
            />
          ))}
        </div>
      </div>

      {/* Recent inspections */}
      <div className="bg-white rounded-lg border p-4">
        <h2 className="font-semibold text-gray-700 mb-3">Recent Inspections</h2>
        <div className="flex flex-col gap-3">
          {recent_inspections.map((insp) => (
            <div key={insp.id} className="flex items-center gap-4 border-b pb-3 last:border-none">
              <img
                src={getHeatmapUrl(insp.heatmap_url)}
                alt="heatmap"
                className="w-16 h-16 object-cover rounded"
              />
              <div className="flex-1">
                <p className="text-sm text-gray-600">
                  Score: {insp.anomaly_score.toFixed(2)} — {insp.severity}
                </p>
                <p className="text-xs text-gray-400">
                  {new Date(insp.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchDashboard() {
  const response = await fetch(`${API_BASE_URL}/dashboard`);
  if (!response.ok) {
    throw new Error(`Failed to load dashboard: ${response.status}`);
  }
  return response.json();
}
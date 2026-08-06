/**
 * API client for the FastAPI backend.
 *
 * Kept separate from components so the actual fetch/axios logic
 * (URLs, error handling, response parsing) lives in one place —
 * if the backend URL or response shape changes, only this file
 * needs to change, not every component that calls it.
 */

const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchCategories() {
  const response = await fetch(`${API_BASE_URL}/categories`);
  if (!response.ok) throw new Error("Failed to load categories");
  const data = await response.json();
  return data.categories;
}

export async function inspectImage(file, category) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("category", category);

  const response = await fetch(`${API_BASE_URL}/inspect`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export function getHeatmapUrl(heatmapPath) {
  return `${API_BASE_URL}${heatmapPath}`;
}
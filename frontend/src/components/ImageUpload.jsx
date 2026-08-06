/**
 * Handles image file selection and preview before submission.
 *
 * Kept separate from the results display and page layout — this
 * component's only responsibility is: let the user pick a file,
 * show a preview, and notify the parent when they're ready to submit.
 */

import { useState, useEffect } from "react";
import { fetchCategories } from "../api/inspectionApi";

export default function ImageUpload({ onSubmit, isLoading }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");

  useEffect(() => {
    fetchCategories()
      .then((cats) => {
        setCategories(cats);
        if (cats.length > 0) setSelectedCategory(cats[0]);
      })
      .catch(() => setCategories([]));
  }, []);

  function handleFileChange(event) {
    const file = event.target.files[0];
    if (!file) return;
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  }

  function handleSubmit() {
    if (selectedFile && selectedCategory) {
      onSubmit(selectedFile, selectedCategory);
    }
  }

  return (
    <div className="flex flex-col items-center gap-4 p-6 border-2 border-dashed border-gray-300 rounded-lg">
      <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
        className="text-sm border rounded px-2 py-1"
      >
        {categories.map((cat) => (
          <option key={cat} value={cat}>
            {cat}
          </option>
        ))}
      </select>

      <input
        type="file"
        accept="image/png, image/jpeg"
        onChange={handleFileChange}
        className="text-sm text-gray-600"
      />

      {previewUrl && (
        <img
          src={previewUrl}
          alt="Selected preview"
          className="w-48 h-48 object-cover rounded-md border"
        />
      )}

      <button
        onClick={handleSubmit}
        disabled={!selectedFile || !selectedCategory || isLoading}
        className="px-4 py-2 bg-blue-600 text-white rounded-md disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-700 transition"
      >
        {isLoading ? "Inspecting..." : "Run Inspection"}
      </button>
    </div>
  );
}
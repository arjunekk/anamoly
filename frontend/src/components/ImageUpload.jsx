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
    <div className="w-full max-w-md bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-6 flex flex-col gap-4">
      <div>
        <label className="text-[11px] tracking-wide uppercase text-neutral-400 dark:text-neutral-500 block mb-1.5">
          Category
        </label>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="w-full text-sm px-3 py-2 rounded-md border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100"
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-[11px] tracking-wide uppercase text-neutral-400 dark:text-neutral-500 block mb-1.5">
          Image
        </label>
        <label className="flex items-center gap-2 border border-dashed border-neutral-300 dark:border-neutral-700 rounded-md px-3 py-3 cursor-pointer hover:border-neutral-400 dark:hover:border-neutral-600 transition-colors">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-neutral-400 shrink-0">
            <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14M14 8h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span className="text-sm text-neutral-500 dark:text-neutral-400 truncate">
            {selectedFile ? selectedFile.name : "Choose an image"}
          </span>
          <input
            type="file"
            accept="image/png, image/jpeg"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>
      </div>

      {previewUrl && (
        <img
          src={previewUrl}
          alt="Selected preview"
          className="w-full h-40 object-cover rounded-md border border-neutral-200 dark:border-neutral-800"
        />
      )}

      <button
        onClick={handleSubmit}
        disabled={!selectedFile || !selectedCategory || isLoading}
        className="w-full py-2 rounded-md text-sm font-medium bg-neutral-900 dark:bg-neutral-100 text-white dark:text-neutral-900 disabled:bg-neutral-200 dark:disabled:bg-neutral-800 disabled:text-neutral-400 dark:disabled:text-neutral-600 transition-colors active:scale-[0.98]"
      >
        {isLoading ? "Inspecting…" : "Run inspection"}
      </button>
    </div>
  );
}
import { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import InspectionResults from "./components/InspectionResults";
import { inspectImage } from "./api/inspectionApi";

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(file) {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await inspectImage(file);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <h1 className="text-2xl font-bold text-gray-800 mb-8">
        Industrial Defect Detection
      </h1>

      <ImageUpload onSubmit={handleSubmit} isLoading={isLoading} />

      {error && (
        <p className="mt-4 text-red-600 text-sm">
          Error: {error}
        </p>
      )}

      <InspectionResults result={result} />
    </div>
  );
}

export default App;
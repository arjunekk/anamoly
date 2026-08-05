import { useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import ImageUpload from "./components/ImageUpload";
import InspectionResults from "./components/InspectionResults";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import { inspectImage } from "./api/inspectionApi";

function InspectionPage() {
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

      {error && <p className="mt-4 text-red-600 text-sm">Error: {error}</p>}

      <InspectionResults result={result} />
    </div>
  );
}

function NavBar() {
  return (
    <nav className="bg-white border-b px-6 py-3 flex gap-6">
      <Link to="/" className="font-medium text-gray-700 hover:text-blue-600">
        Inspect
      </Link>
      <Link to="/dashboard" className="font-medium text-gray-700 hover:text-blue-600">
        Dashboard
      </Link>
      <Link to="/history" className="font-medium text-gray-700 hover:text-blue-600">
        History
      </Link>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<InspectionPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
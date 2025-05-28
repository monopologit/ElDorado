import './index.css';
import React, { useState } from "react";
import Upload from "./components/Upload";
import Historial from "./components/Historial";
import Trayectoria from "./components/Trayectoria";
import CameraCapture from "./components/CameraCapture";
import Navbar from "./components/Navbar";
import "./App.css";

const App = () => {
  const [view, setView] = useState("upload");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFrameCapture = async (blob, extraFields) => {
    setLoading(true);
    setResult(null);
    const formData = new FormData();
    formData.append("file", blob, "frame.jpg");
    if (extraFields) {
      if (extraFields.evento) formData.append("evento", extraFields.evento);
      if (extraFields.tunel) formData.append("tunel", extraFields.tunel);
      if (extraFields.modelo_ladrillo) formData.append("modelo_ladrillo", extraFields.modelo_ladrillo);
      if (extraFields.merma) formData.append("merma", extraFields.merma);
    }
    try {
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult({ error: "Error al enviar el frame" });
    }
    setLoading(false);
  };

  return (
    <div className="w-full min-h-screen flex flex-col bg-cyan-50">
      <Navbar view={view} setView={setView} />
      <main className="w-full flex-1 flex flex-col items-center">
        {view === "upload" && <Upload />}
        {view === "camera" && (
          <>
            <CameraCapture onCapture={handleFrameCapture} loading={loading} />
            {result && (
              <div className="bg-white border border-cyan-200 rounded-xl p-4 mt-4 shadow w-full max-w-2xl">
                {result.error ? (
                  <span style={{ color: "#d32f2f" }}>{result.error}</span>
                ) : (
                  <>
                    <b>Resultado:</b>
                    <pre style={{ background: "#f5f5f5", padding: 10, borderRadius: 6 }}>{JSON.stringify(result, null, 2)}</pre>
                  </>
                )}
              </div>
            )}
          </>
        )}
        {view === "historial" && <Historial />}
        {view === "trayectoria" && <Trayectoria />}
      </main>
    </div>
  );
}

export default App;

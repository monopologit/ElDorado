import './index.css';
import React, { useState } from "react";
import Upload from "./components/Upload";
import Historial from "./components/Historial";
import Trayectoria from "./components/Trayectoria";
import CameraCapture from "./components/CameraCapture";
import Navbar from "./components/Navbar";
import GuiaUsuario from "./components/GuiaUsuario";
import "./App.css";

const App = () => {
  const [view, setView] = useState("upload");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [feedbacks, setFeedbacks] = useState({});

  const handleFrameCapture = async (blob, extraFields) => {
    setLoading(true);
    setResult(null);
    setFeedbacks({});
    const formData = new FormData();
    formData.append("file", blob, "frame.jpg");
    if (extraFields) {
      if (extraFields.evento) formData.append("evento", extraFields.evento);
      if (extraFields.tunel) formData.append("tunel", extraFields.tunel);
      if (extraFields.merma) formData.append("merma", extraFields.merma);
    }
    let panel = extraFields?.evento === "egreso" ? "egreso" : "ingreso";
    try {
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
      let status = "ok", msg = "Registro exitoso";
      if (data.status === "ignored") { status = "ignored"; msg = "Imagen ignorada (sin vagoneta o número)"; }
      if (data.status === "error" || data.error) { status = "error"; msg = data.error || "Error al procesar"; }
      setFeedbacks({ panel, status, message: msg });
    } catch (e) {
      setResult({ error: "Error al enviar el frame" });
      setFeedbacks({ panel, status: "error", message: "Error al enviar el frame" });
    }
    setLoading(false);
  };

  return (
    <div className="w-full min-h-screen flex flex-col bg-cyan-50">
      <Navbar view={view} setView={setView} />
      <main className="w-full flex-1 flex flex-col items-center">
        {view === "upload" && <Upload />}
        {view === "camera" && (
          <CameraCapture onCapture={handleFrameCapture} loading={loading} feedbacks={feedbacks} />
        )}
        {view === "historial" && <Historial />}
        {view === "trayectoria" && <Trayectoria />}
        {view === "guia" && <GuiaUsuario />}
      </main>
    </div>
  );
}

export default App;

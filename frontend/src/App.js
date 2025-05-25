import React, { useState } from "react";
import Upload from "./components/Upload";
import Historial from "./components/Historial";
import Trayectoria from "./components/Trayectoria";
import "./App.css";

const App = () => {
  const [view, setView] = useState("upload");

  return (
    <div className="container">
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 16, marginBottom: 16 }}>
        <img src={process.env.PUBLIC_URL + "/logo.jpg"} alt="Logo empresa" style={{ height: 54, borderRadius: 8, boxShadow: "0 2px 8px #0001" }} />
        <h1 style={{ color: "#1976d2", fontWeight: 700, fontSize: 28, margin: 0 }}>
          Seguimiento de Vagonetas
        </h1>
      </div>
      <nav className="navbar">
        <button
          className={view === "upload" ? "active" : ""}
          onClick={() => setView("upload")}
        >
          Subir Imagen
        </button>
        <button
          className={view === "historial" ? "active" : ""}
          onClick={() => setView("historial")}
        >
          Ver Historial
        </button>
        <button
          className={view === "trayectoria" ? "active" : ""}
          onClick={() => setView("trayectoria")}
        >
          Trayectoria
        </button>
      </nav>
      <main className="main-content">
        {view === "upload" && <Upload />}
        {view === "historial" && <Historial />}
        {view === "trayectoria" && <Trayectoria />}
      </main>
    </div>
  );
}

export default App;

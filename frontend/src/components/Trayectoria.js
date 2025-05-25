import React, { useState } from "react";
import axios from "axios";

const Trayectoria = () => {
  const [numero, setNumero] = useState("");
  const [registros, setRegistros] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleBuscar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setRegistros([]);
    try {
      const res = await axios.get(`http://localhost:8000/trayectoria/${numero}`);
      setRegistros(res.data);
    } catch (err) {
      setError("No se encontró trayectoria para ese número de vagoneta.");
    }
    setLoading(false);
  };

  return (
    <div>
      <h2 style={{ textAlign: "center", color: "#1976d2" }}>Trayectoria de Vagoneta</h2>
      <form onSubmit={handleBuscar} style={{ marginBottom: 16 }}>
        <input
          type="text"
          placeholder="Número de vagoneta"
          value={numero}
          onChange={e => setNumero(e.target.value)}
        />
        <button type="submit">Buscar</button>
      </form>
      {loading && <p style={{ textAlign: "center" }}>Buscando...</p>}
      {error && <p style={{ color: "#d32f2f", textAlign: "center" }}>{error}</p>}
      {registros.length > 0 && (
        <div style={{ overflowX: "auto", marginTop: 24 }}>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Evento</th>
                <th>Imagen</th>
                <th>Fecha y Hora</th>
                <th>Túnel</th>
                <th>Modelo</th>
                <th>% Merma</th>
              </tr>
            </thead>
            <tbody>
              {registros.map((r, idx) => (
                <tr key={idx} style={{ background: r.evento === "ingreso" ? "#e3f6e3" : "#e3eaf2" }}>
                  <td style={{ fontWeight: 600 }}>{idx + 1}</td>
                  <td style={{ fontWeight: 600, color: r.evento === "ingreso" ? "#388e3c" : "#1976d2" }}>
                    {r.evento.charAt(0).toUpperCase() + r.evento.slice(1)}
                  </td>
                  <td>
                    <img src={`http://localhost:8000/${r.imagen_path}`} alt="vagoneta" width={80} style={{ borderRadius: 6, boxShadow: "0 2px 8px #0001" }} />
                  </td>
                  <td>{new Date(r.timestamp).toLocaleString()}</td>
                  <td>{r.tunel || "-"}</td>
                  <td>{r.modelo_ladrillo || "-"}</td>
                  <td>{r.merma !== undefined && r.merma !== null ? `${r.merma}%` : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div style={{ marginTop: 18, textAlign: "center" }}>
            <span style={{ fontWeight: 500, color: "#1976d2" }}>
              Total de eventos: {registros.length}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Trayectoria;

import React, { useEffect, useState } from "react";
import axios from "axios";

const Historial = () => {
  const [registros, setRegistros] = useState([]);
  const [numero, setNumero] = useState("");
  const [fecha, setFecha] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchRegistros = async () => {
    setLoading(true);
    let params = {};
    if (numero) params.numero = numero;
    if (fecha) params.fecha = fecha;
    try {
      const res = await axios.get("http://localhost:8000/vagonetas/", { params });
      setRegistros(res.data);
    } catch (err) {
      setRegistros([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchRegistros();
    // eslint-disable-next-line
  }, []);

  const handleFiltrar = (e) => {
    e.preventDefault();
    fetchRegistros();
  };

  return (
    <div>
      <h2 style={{ textAlign: "center", color: "#1976d2" }}>Historial de Vagonetas</h2>
      <form onSubmit={handleFiltrar}>
        <input
          type="text"
          placeholder="Número de vagoneta"
          value={numero}
          onChange={e => setNumero(e.target.value)}
        />
        <input
          type="date"
          value={fecha}
          onChange={e => setFecha(e.target.value)}
        />
        <button type="submit">Filtrar</button>
      </form>
      {loading ? (
        <p style={{ textAlign: "center" }}>Cargando...</p>
      ) : (
        <div style={{ overflowX: "auto" }}>
          <table border="1" cellPadding="6">
            <thead>
              <tr>
                <th>Imagen</th>
                <th>Número</th>
                <th>Timestamp</th>
                <th>Túnel</th>
                <th>Modelo</th>
                <th>% Merma</th>
              </tr>
            </thead>
            <tbody>
              {registros.map((r, idx) => (
                <tr key={idx}>
                  <td>
                    <img src={`http://localhost:8000/${r.imagen_path}`} alt="vagoneta" width={80} />
                  </td>
                  <td>{r.numero || "-"}</td>
                  <td>{new Date(r.timestamp).toLocaleString()}</td>
                  <td>{r.tunel || "-"}</td>
                  <td>{r.modelo_ladrillo || "-"}</td>
                  <td>{r.merma !== undefined && r.merma !== null ? `${r.merma}%` : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Historial;

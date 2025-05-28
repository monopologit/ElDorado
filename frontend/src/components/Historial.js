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
    <div className="w-full flex flex-col items-center px-2 md:px-0">
      <h2 className="text-2xl font-extrabold text-orange-600 mb-4 tracking-tight drop-shadow-sm uppercase letter-spacing-wide">Historial de Vagonetas</h2>
      <form onSubmit={handleFiltrar} className="mb-4 w-full max-w-3xl">
        <div className="flex flex-col md:flex-row md:space-x-4">
          <input
            type="text"
            placeholder="Número de vagoneta"
            value={numero}
            onChange={e => setNumero(e.target.value)}
            className="flex-1 px-4 py-2 border border-cyan-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"
          />
          <input
            type="date"
            value={fecha}
            onChange={e => setFecha(e.target.value)}
            className="flex-1 px-4 py-2 border border-cyan-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-500"
          />
          <button type="submit" className="mt-2 md:mt-0 bg-orange-600 text-white font-bold py-2 px-4 rounded-lg shadow hover:bg-orange-500 transition-all">
            Filtrar
          </button>
        </div>
      </form>
      {loading ? (
        <p style={{ textAlign: "center" }}>Cargando...</p>
      ) : (
        <div className="w-full overflow-x-auto">
          <table className="min-w-full bg-white border border-cyan-200 rounded-xl shadow text-cyan-900 text-base">
            <thead className="bg-cyan-100">
              <tr>
                <th className="px-4 py-2 font-bold text-orange-600">N°</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Evento</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Túnel</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Modelo</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Merma</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Fecha</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Imagen</th>
              </tr>
            </thead>
            <tbody>
              {registros.map((r, idx) => (
                <tr key={idx}>
                  <td className="px-4 py-2 border-b">{r.numero || "-"}</td>
                  <td className="px-4 py-2 border-b">{r.evento || "-"}</td>
                  <td className="px-4 py-2 border-b">{r.tunel || "-"}</td>
                  <td className="px-4 py-2 border-b">{r.modelo_ladrillo || "-"}</td>
                  <td className="px-4 py-2 border-b">{r.merma !== undefined && r.merma !== null ? `${r.merma}%` : "-"}</td>
                  <td className="px-4 py-2 border-b">{new Date(r.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-2 border-b">
                    <img src={`http://localhost:8000/${r.imagen_path}`} alt="vagoneta" width={80} />
                  </td>
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

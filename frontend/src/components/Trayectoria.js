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
    <div className="w-full max-w-3xl mx-auto bg-white rounded-2xl p-6 flex flex-col items-center border border-cyan-200 mt-4 mb-8 transition">
      <h2 className="text-2xl font-extrabold text-orange-600 mb-4 tracking-wider uppercase text-center">
        Trayectoria de Vagoneta
      </h2>
      <form onSubmit={handleBuscar} className="w-full flex flex-col md:flex-row gap-4 items-center mb-4">
        <input
          type="text"
          placeholder="Número de vagoneta"
          value={numero}
          onChange={e => setNumero(e.target.value)}
          className="flex-1 px-3 py-2 border border-cyan-300 rounded-lg bg-cyan-50 text-cyan-900 font-medium placeholder-cyan-400 focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
        <button type="submit" className="py-2 px-6 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-xl transition disabled:bg-cyan-300 disabled:cursor-not-allowed shadow-md tracking-wider text-lg">
          Buscar
        </button>
      </form>
      {loading && <p className="text-cyan-700 font-semibold text-center animate-pulse">Buscando...</p>}
      {error && <p className="text-red-600 text-center font-bold animate-bounce">{error}</p>}
      {registros.length > 0 && (
        <div className="w-full overflow-x-auto mt-6">
          <table className="min-w-full bg-white border border-cyan-200 rounded-xl shadow text-cyan-900 text-base">
            <thead className="bg-cyan-100">
              <tr>
                <th className="px-4 py-2 font-bold text-orange-600">#</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Evento</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Imagen</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Fecha y Hora</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Túnel</th>
                <th className="px-4 py-2 font-bold text-cyan-700">Modelo</th>
                <th className="px-4 py-2 font-bold text-cyan-700">% Merma</th>
              </tr>
            </thead>
            <tbody>
              {registros.map((r, idx) => (
                <tr key={idx} className={r.evento === "ingreso" ? "bg-green-50" : "bg-cyan-50"}>
                  <td className="px-4 py-2 border-b font-bold">{idx + 1}</td>
                  <td className={`px-4 py-2 border-b font-bold ${r.evento === "ingreso" ? "text-green-700" : "text-cyan-700"}`}>
                    {r.evento.charAt(0).toUpperCase() + r.evento.slice(1)}
                  </td>
                  <td className="px-4 py-2 border-b">
                    <img src={`http://localhost:8000/${r.imagen_path}`} alt="vagoneta" width={80} className="rounded-md shadow" />
                  </td>
                  <td className="px-4 py-2 border-b">{new Date(r.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-2 border-b">{r.tunel || "-"}</td>
                  <td className="px-4 py-2 border-b">{r.modelo_ladrillo || "-"}</td>
                  <td className="px-4 py-2 border-b">{r.merma !== undefined && r.merma !== null ? `${r.merma}%` : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="mt-4 text-center">
            <span className="font-bold text-cyan-700">Total de eventos: {registros.length}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Trayectoria;

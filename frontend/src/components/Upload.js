import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [progress, setProgress] = useState(null);
  const [evento, setEvento] = useState("ingreso");
  const [tunel, setTunel] = useState("");
  const [modeloLadrillo, setModeloLadrillo] = useState("");
  const [merma, setMerma] = useState("");

  const handleChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!files.length) return;
    setProgress({ current: 0, total: files.length });
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    formData.append("evento", evento);
    formData.append("tunel", tunel);
    formData.append("modelo_ladrillo", modeloLadrillo);
    formData.append("merma", merma);
    try {
      const res = await axios.post(
        "http://localhost:8000/upload-multiple/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              setProgress({
                current: Math.round(
                  (progressEvent.loaded / progressEvent.total) * files.length
                ),
                total: files.length,
              });
            }
          },
        }
      );
      const ok = res.data.results.filter((r) => r.status === "ok").length;
      const ignored = res.data.results.filter((r) => r.status === "ignored")
        .length;
      const fail = res.data.results.filter((r) => r.status === "error").length;
      let msg = `Subidas exitosas: ${ok}`;
      if (ignored > 0) msg += `, ignoradas (sin vagoneta): ${ignored}`;
      if (fail > 0) msg += `, fallidas: ${fail}`;
      setMessage(msg);
    } catch (err) {
      setMessage("Error al subir las imágenes");
    }
    setFiles([]);
    setProgress(null);
  };

  return (
    <div className="w-full max-w-3xl mx-auto bg-cyan-50 rounded-xl p-6 flex flex-col items-center mt-4 mb-8">
      <h2 className="text-2xl font-extrabold text-orange-600 mb-4 tracking-wider uppercase text-center">
        Subir Imagen de Vagoneta
      </h2>
      <form
        onSubmit={handleUpload}
        className="w-full flex flex-col md:flex-row md:flex-nowrap gap-4 items-center mb-4 justify-center"
      >
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={handleChange}
          className="block w-full md:w-auto px-3 py-2 border border-cyan-300 rounded-lg bg-white text-cyan-900 font-medium placeholder-cyan-400 focus:outline-none focus:ring-2 focus:ring-orange-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-orange-50 file:text-orange-700 hover:file:bg-orange-100"
        />
        <select
          value={evento}
          onChange={(e) => setEvento(e.target.value)}
          className="px-3 py-2 border border-cyan-300 rounded-lg bg-white text-cyan-900 font-semibold uppercase tracking-wider focus:outline-none focus:ring-2 focus:ring-orange-400 md:w-36"
        >
          <option value="ingreso">Ingreso</option>
          <option value="egreso">Egreso</option>
        </select>
        <input
          type="text"
          placeholder="Túnel (opcional)"
          value={tunel}
          onChange={(e) => setTunel(e.target.value)}
          className="px-3 py-2 border border-cyan-300 rounded-lg bg-white text-cyan-900 font-medium placeholder-cyan-400 focus:outline-none focus:ring-2 focus:ring-orange-400 md:w-40"
        />
        <input
          type="text"
          placeholder="Modelo de ladrillo (opcional)"
          value={modeloLadrillo}
          onChange={(e) => setModeloLadrillo(e.target.value)}
          className="px-3 py-2 border border-cyan-300 rounded-lg bg-white text-cyan-900 font-medium placeholder-cyan-400 focus:outline-none focus:ring-2 focus:ring-orange-400 md:w-48"
        />
        <input
          type="number"
          min="0"
          max="100"
          step="0.01"
          placeholder="% Merma (opcional)"
          value={merma}
          onChange={(e) => setMerma(e.target.value)}
          className="px-3 py-2 border border-cyan-300 rounded-lg bg-white text-cyan-900 font-medium placeholder-cyan-400 focus:outline-none focus:ring-2 focus:ring-orange-400 w-28"
        />
        <button
          type="submit"
          disabled={!files.length}
          className="py-2 px-6 w-full md:w-auto bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-lg transition disabled:bg-cyan-300 disabled:cursor-not-allowed tracking-wider text-lg mx-auto border border-orange-500"
        >
          Subir
        </button>
      </form>
      {progress && (
        <p className="text-cyan-700 font-semibold text-center animate-pulse">
          Subiendo {progress.current} de {progress.total}...
        </p>
      )}
      {message && (
        <p
          className={`text-center font-bold mt-2 ${
            message.includes("fallidas")
              ? "text-red-600 animate-bounce"
              : "text-green-700 animate-pulse"
          }`}
        >
          {message}
        </p>
      )}
      {files.length > 0 && (
        <div className="flex flex-wrap gap-3 justify-center mt-4">
          {files.map((file, idx) => (
            <div
              key={idx}
              className="border border-cyan-200 rounded-lg p-2 bg-white flex flex-col items-center"
            >
              <img
                src={URL.createObjectURL(file)}
                alt={file.name}
                className="w-20 h-20 object-cover rounded-md border border-cyan-100"
              />
              <div className="text-xs text-cyan-900 font-semibold text-center mt-1">
                {file.name}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Upload;

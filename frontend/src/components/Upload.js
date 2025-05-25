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
      const fail = res.data.results.filter((r) => r.status !== "ok").length;
      setMessage(`Subidas exitosas: ${ok}, fallidas: ${fail}`);
    } catch (err) {
      setMessage("Error al subir las imágenes");
    }
    setFiles([]);
    setProgress(null);
  };

  return (
    <div>
      <h2 style={{ textAlign: "center", color: "#1976d2" }}>
        Subir imagen de vagoneta
      </h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="image/*"
          multiple
          onChange={handleChange}
        />
        <select
          value={evento}
          onChange={(e) => setEvento(e.target.value)}
          style={{ marginLeft: 8 }}
        >
          <option value="ingreso">Ingreso</option>
          <option value="egreso">Egreso</option>
        </select>
        <input
          type="text"
          placeholder="Túnel (opcional)"
          value={tunel}
          onChange={(e) => setTunel(e.target.value)}
          style={{ marginLeft: 8 }}
        />
        <input
          type="text"
          placeholder="Modelo de ladrillo (opcional)"
          value={modeloLadrillo}
          onChange={(e) => setModeloLadrillo(e.target.value)}
          style={{ marginLeft: 8 }}
        />
        <input
          type="number"
          min="0"
          max="100"
          step="0.01"
          placeholder="% Merma (opcional)"
          value={merma}
          onChange={(e) => setMerma(e.target.value)}
          style={{ marginLeft: 8, width: 110 }}
        />
        <button
          type="submit"
          disabled={!files.length}
          style={{ marginLeft: 8 }}
        >
          Subir
        </button>
      </form>
      {progress && (
        <p style={{ textAlign: "center" }}>
          Subiendo {progress.current} de {progress.total}...
        </p>
      )}
      {message && (
        <p
          style={{
            color: message.includes("fallidas") ? "#d32f2f" : "#388e3c",
            textAlign: "center",
          }}
        >
          {message}
        </p>
      )}
      {files.length > 0 && (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: 8,
            justifyContent: "center",
            marginTop: 12,
          }}
        >
          {files.map((file, idx) => (
            <div
              key={idx}
              style={{
                border: "1px solid #bfc9d9",
                borderRadius: 6,
                padding: 4,
                background: "#f6f8fa",
              }}
            >
              <img
                src={URL.createObjectURL(file)}
                alt={file.name}
                style={{
                  width: 80,
                  height: 80,
                  objectFit: "cover",
                  borderRadius: 4,
                }}
              />
              <div
                style={{
                  fontSize: 12,
                  textAlign: "center",
                  marginTop: 2,
                }}
              >
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

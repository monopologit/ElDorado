import React, { useRef, useEffect, useState } from "react";

const CameraPanel = ({ label, evento, onCapture, loading }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [error, setError] = useState(null);
  const [tunel, setTunel] = useState("");
  const [modelo, setModelo] = useState("");
  const [merma, setMerma] = useState("");

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => { videoRef.current.srcObject = stream; })
      .catch(() => setError("No se pudo acceder a la cámara"));
  }, []);

  const handleCapture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
      onCapture(blob, { evento, tunel, modelo_ladrillo: modelo, merma });
    }, "image/jpeg");
  };

  return (
    <div className="w-full max-w-md bg-white rounded-2xl p-6 flex flex-col items-center mb-8 border border-cyan-200 transition">
      <h3 className="text-2xl font-extrabold text-orange-600 mb-4 tracking-wider uppercase">
        Cámara {label}
      </h3>
      {error && <div className="text-red-600 mb-2 text-center font-semibold animate-bounce">{error}</div>}
      <div className="w-full flex flex-col gap-4 mb-4">
        <label className="flex flex-col text-base font-semibold text-cyan-900 tracking-wide">
          <span className="mb-1 text-cyan-700 uppercase tracking-wider">Túnel</span>
          <input value={tunel} onChange={e => setTunel(e.target.value)} placeholder="Ej: Túnel 1" className="mt-1 px-3 py-2 border border-cyan-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 bg-cyan-50 placeholder-cyan-400 font-medium text-cyan-900" />
        </label>
        <label className="flex flex-col text-base font-semibold text-cyan-900 tracking-wide">
          <span className="mb-1 text-cyan-700 uppercase tracking-wider">Modelo ladrillo</span>
          <input value={modelo} onChange={e => setModelo(e.target.value)} placeholder="Opcional" className="mt-1 px-3 py-2 border border-cyan-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 bg-cyan-50 placeholder-cyan-400 font-medium text-cyan-900" />
        </label>
        <label className="flex flex-col text-base font-semibold text-cyan-900 tracking-wide">
          <span className="mb-1 text-cyan-700 uppercase tracking-wider">Merma (%)</span>
          <input type="number" value={merma} onChange={e => setMerma(e.target.value)} placeholder="Opcional" className="mt-1 px-3 py-2 border border-cyan-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 bg-cyan-50 placeholder-cyan-400 font-medium text-cyan-900" />
        </label>
      </div>
      <div className="w-full flex flex-col items-center mb-4">
        <video ref={videoRef} autoPlay playsInline className="rounded-xl border border-cyan-200 w-full aspect-video max-h-64 object-cover bg-black" />
        <canvas ref={canvasRef} style={{ display: "none" }} />
      </div>
      <button className="w-full py-2 px-4 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-xl transition disabled:bg-cyan-300 disabled:cursor-not-allowed tracking-wider text-lg" onClick={handleCapture} disabled={loading}>
        {loading ? "Procesando..." : `Capturar Frame (${label})`}
      </button>
    </div>
  );
};

const CameraCapture = ({ onCapture, loading }) => {
  return (
    <div className="w-full flex flex-col md:flex-row md:items-start md:justify-center gap-8 py-6 px-2 md:px-0 bg-cyan-50 min-h-screen">
      <CameraPanel label="Ingreso" evento="ingreso" onCapture={onCapture} loading={loading} />
      <CameraPanel label="Egreso" evento="egreso" onCapture={onCapture} loading={loading} />
    </div>
  );
};

export default CameraCapture;

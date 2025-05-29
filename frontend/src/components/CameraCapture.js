import React, { useRef, useEffect, useState } from "react";

const CameraPanel = ({ label, evento, onCapture, loading }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [error, setError] = useState(null);
  const [tunel, setTunel] = useState("");
  const [merma, setMerma] = useState("");
  const [devices, setDevices] = useState([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState("");

  // Listar cámaras disponibles
  useEffect(() => {
    navigator.mediaDevices.enumerateDevices().then((all) => {
      const videoDevices = all.filter((d) => d.kind === "videoinput");
      setDevices(videoDevices);
      if (videoDevices.length > 0) setSelectedDeviceId(videoDevices[0].deviceId);
    });
  }, []);

  // Cambiar stream al cambiar de cámara
  useEffect(() => {
    if (!selectedDeviceId) return;
    const constraints = { video: { deviceId: { exact: selectedDeviceId } } };
    let localStream = null;
    navigator.mediaDevices.getUserMedia(constraints)
      .then((stream) => {
        localStream = stream;
        if (videoRef.current) videoRef.current.srcObject = stream;
        setError(null);
      })
      .catch(() => setError("No se pudo acceder a la cámara seleccionada"));
    return () => {
      if (localStream) {
        localStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [selectedDeviceId]);

  const handleCapture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      onCapture(blob, { evento, tunel, merma }); // modelo_ladrillo eliminado, será detectado automáticamente
    }, "image/jpeg");
  };

  return (
    <div className="w-full max-w-md bg-white rounded-2xl p-6 flex flex-col items-center mb-8 border border-cyan-200 transition">
      <h3 className="text-2xl font-extrabold text-orange-600 mb-4 tracking-wider uppercase">
        Cámara {label}
      </h3>
      {devices.length > 1 && (
        <div className="mb-3 w-full">
          <label className="block text-cyan-700 font-semibold mb-1">Seleccionar cámara:</label>
          <select
            className="w-full px-3 py-2 border border-cyan-300 rounded-lg bg-cyan-50 text-cyan-900 font-medium"
            value={selectedDeviceId}
            onChange={e => setSelectedDeviceId(e.target.value)}
          >
            {devices.map((d, idx) => (
              <option key={d.deviceId} value={d.deviceId}>{d.label || `Cámara ${idx + 1}`}</option>
            ))}
          </select>
        </div>
      )}
      {error && <div className="text-red-600 mb-2 text-center font-semibold animate-bounce">{error}</div>}
      <div className="w-full flex flex-col gap-4 mb-4">
        <label className="flex flex-col text-base font-semibold text-cyan-900 tracking-wide">
          <span className="mb-1 text-cyan-700 uppercase tracking-wider">Túnel</span>
          <input value={tunel} onChange={e => setTunel(e.target.value)} placeholder="Ej: Túnel 1" className="mt-1 px-3 py-2 border border-cyan-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-400 bg-cyan-50 placeholder-cyan-400 font-medium text-cyan-900" />
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

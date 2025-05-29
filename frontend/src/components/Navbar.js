import React, { useState } from "react";

const Navbar = ({ view, setView }) => {
  const [open, setOpen] = useState(false);
  return (
    <nav className="w-full bg-white border-b border-cyan-200 shadow-sm mb-6 sticky top-0 z-20">
      <div className="w-full flex flex-col md:flex-row md:items-center md:justify-between px-2 md:px-8 py-2 max-w-full">
        <div className="flex items-center gap-3 mb-2 md:mb-0">
          <img src={process.env.PUBLIC_URL + "/logo.jpg"} alt="Logo" className="h-10 w-10 rounded-lg shadow" />
          <span className="text-xl md:text-2xl font-bold text-orange-600 tracking-tight">Seguimiento de Vagonetas</span>
        </div>
        <button className="md:hidden p-2 rounded text-cyan-700 hover:bg-cyan-100 absolute right-4 top-3" onClick={() => setOpen(!open)}>
          {/* Menú hamburguesa simple */}
          <span className="block w-7 h-1 bg-cyan-700 mb-1 rounded"></span>
          <span className="block w-7 h-1 bg-cyan-700 mb-1 rounded"></span>
          <span className="block w-7 h-1 bg-cyan-700 rounded"></span>
        </button>
        <div className={`w-full md:w-auto flex-col md:flex md:flex-row md:gap-3 md:static absolute top-16 left-0 bg-white md:bg-transparent border-t md:border-none border-cyan-100 shadow md:shadow-none z-10 transition-all duration-200 ${open ? 'flex' : 'hidden'}`}>
          <button onClick={() => { setView('camera'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'camera' ? 'bg-orange-500 text-white' : 'bg-cyan-100 text-cyan-900 hover:bg-orange-100'} transition text-lg border border-orange-400`}>
            Cámara Tiempo Real
          </button>
          <button onClick={() => { setView('upload'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'upload' ? 'bg-orange-100 text-orange-700' : 'bg-cyan-50 text-cyan-900 hover:bg-orange-50'} transition`}>
            Subir Imagen
          </button>
          <button onClick={() => { setView('historial'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'historial' ? 'bg-orange-100 text-orange-700' : 'bg-cyan-50 text-cyan-900 hover:bg-orange-50'} transition`}>
            Ver Historial
          </button>
          <button onClick={() => { setView('trayectoria'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'trayectoria' ? 'bg-orange-100 text-orange-700' : 'bg-cyan-50 text-cyan-900 hover:bg-orange-50'} transition`}>
            Trayectoria
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

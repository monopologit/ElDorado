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
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-7 h-7">
            <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 6.75h15m-15 5.25h15m-15 5.25h15" />
          </svg>
        </button>
        <div className={`w-full md:w-auto flex-col md:flex md:flex-row md:gap-3 md:static absolute top-16 left-0 bg-white md:bg-transparent border-t md:border-none border-cyan-100 shadow md:shadow-none z-10 transition-all duration-200 ${open ? 'flex' : 'hidden'}`}>
          <button onClick={() => { setView('upload'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'upload' ? 'bg-orange-500 text-white' : 'bg-cyan-100 text-cyan-900 hover:bg-orange-100'} transition`}>
            Subir Imagen
          </button>
          <button onClick={() => { setView('camera'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'camera' ? 'bg-orange-500 text-white' : 'bg-cyan-100 text-cyan-900 hover:bg-orange-100'} transition`}>
            Cámara Tiempo Real
          </button>
          <button onClick={() => { setView('historial'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'historial' ? 'bg-orange-500 text-white' : 'bg-cyan-100 text-cyan-900 hover:bg-orange-100'} transition`}>
            Ver Historial
          </button>
          <button onClick={() => { setView('trayectoria'); setOpen(false); }} className={`w-full md:w-auto py-2 px-4 font-semibold rounded-lg m-1 md:m-0 ${view === 'trayectoria' ? 'bg-orange-500 text-white' : 'bg-cyan-100 text-cyan-900 hover:bg-orange-100'} transition`}>
            Trayectoria
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

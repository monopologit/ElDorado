# Frontend - Seguimiento de Vagonetas

## Descripción
Interfaz web en React para subir imágenes de vagonetas y consultar el historial de registros procesados.

## Instalación rápida (para desarrollo)

### Requisitos previos
- Node.js 16+
- npm (incluido con Node.js)
- Git

### 1. Clona el repositorio
```powershell
git clone <URL_DEL_REPOSITORIO>
cd app_imagenes/frontend
```

### 2. Instala las dependencias
```powershell
npm install
```

### 3. Configura la URL del backend (opcional)
Por defecto, el frontend espera que el backend esté en http://localhost:8000. Si usas otro puerto o dominio, edita la URL en los componentes React (`src/components/Upload.js`, `Historial.js`, `Trayectoria.js`).

### 4. Inicia la aplicación
```powershell
npm start
```

La app se abrirá en tu navegador en http://localhost:3000

## ¿Cómo probar?
- Sube imágenes de vagonetas usando el formulario.
- Consulta el historial y la trayectoria desde la interfaz.

## Componentes principales
- `Upload` — Formulario para subir imágenes
- `Historial` — Tabla para visualizar y filtrar registros
- `Trayectoria` — Consulta la trayectoria de una vagoneta específica

## Notas
- El frontend espera que el backend esté corriendo en http://localhost:8000
- Puedes cambiar la URL en los componentes si usas otro puerto o dominio.

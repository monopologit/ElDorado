# Frontend - Seguimiento de Vagonetas

## Descripción
Interfaz web en React para registrar, consultar y visualizar el historial y la trayectoria de vagonetas en una fábrica de ladrillos.

## Instalación rápida

### Requisitos previos
- Node.js 16+
- npm
- Git

### 1. Clona el repositorio
```bash
# Clona el repositorio y entra al frontend
 git clone <URL_DEL_REPOSITORIO>
 cd ElDorado/frontend
```

### 2. Instala las dependencias
```bash
npm install
```

### 3. Configura la URL del backend (opcional)
Por defecto, el frontend espera el backend en http://localhost:8000. Si usas otro puerto o dominio, edita la URL en los componentes React (`src/components/Upload.js`, `Historial.js`, `Trayectoria.js`).

### 4. Inicia la aplicación
```bash
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
- `CameraCapture` — Captura de imágenes en tiempo real desde cámara web

## Notas
- El frontend espera que el backend esté corriendo en http://localhost:8000
- Puedes cambiar la URL en los componentes si usas otro puerto o dominio.

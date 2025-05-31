# Frontend - Seguimiento de Vagonetas

## Descripción
Interfaz web en React para registrar, consultar y visualizar el historial y la trayectoria de vagonetas en una fábrica de ladrillos.

## ¿Qué hace?
Permite visualizar, capturar y registrar automáticamente el movimiento de vagonetas en la fábrica usando cámaras físicas y visión computacional.

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

## Funcionalidades principales
- **Cámara Tiempo Real:** Captura automática desde cámaras físicas. Es el flujo principal y recomendado.
- **Subir Imagen:** Permite cargar imágenes manualmente (solo para pruebas o casos excepcionales).
- **Historial:** Consulta de registros de vagonetas detectadas.
- **Trayectoria:** Visualiza el recorrido de una vagoneta específica
- `CameraCapture` — Captura de imágenes en tiempo real desde cámara web

## Notas importantes
- El sistema está diseñado para funcionar de forma automática con cámaras físicas. La carga manual es solo un complemento para pruebas.
- El backend debe estar corriendo y tener el modelo YOLOv8 entrenado en `backend/models/yolov8_vagonetas.pt`.

## Personalización
- Puedes modificar los estilos en `src/App.css` y los componentes en `src/components/`.
- El logo y colores pueden adaptarse a la identidad de tu empresa.

## Requisitos
- Node.js 16+
- Acceso al backend corriendo en http://localhost:8000

# Frontend - Interfaz Web para Seguimiento de Vagonetas

Este frontend permite a los usuarios interactuar con el sistema de visión computacional, subir imágenes y videos, y consultar el historial y trayectoria de vagonetas.

## Tecnologías Usadas y Para Qué Sirve Cada Una
- **React:** Construye la interfaz web interactiva.
- **Axios:** Permite la comunicación HTTP con el backend.
- **Tailwind CSS:** Facilita el diseño de interfaces modernas y responsivas.
- **react-scripts:** Scripts y utilidades para desarrollo y build de la app React.

## Flujo de Interacción
1. El usuario accede a la web y puede:
   - Subir imágenes o videos de vagonetas.
   - Consultar historial y trayectoria.
   - Visualizar mensajes de éxito, error o advertencia según el resultado de cada acción.
2. El frontend envía los archivos y datos al backend usando Axios.
3. El backend procesa y responde, y el frontend muestra la información al usuario.


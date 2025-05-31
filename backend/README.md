# Backend - Seguimiento de Vagonetas

Este backend implementa la lógica de procesamiento de imágenes y videos para identificar vagonetas, reconocer su número y clasificar el modelo de ladrillo, registrando toda la información relevante en MongoDB.

## ¿Para qué sirve?
Permite recibir imágenes de vagonetas, procesarlas con visión computacional y registrar automáticamente los datos clave de cada movimiento en la fábrica de ladrillos.

## Tecnologías Usadas y Para Qué Sirve Cada Una
- **FastAPI:** Define la API REST para recibir imágenes, videos y exponer endpoints de consulta.
- **Uvicorn:** Ejecuta la aplicación FastAPI.
- **MongoDB:** Almacena los registros de eventos, metadatos y rutas de imágenes.
- **PyMongo:** Permite la conexión y operaciones con MongoDB.
- **OpenCV:** Procesa imágenes y videos, detecta vagonetas y recorta regiones de interés.
- **Ultralytics YOLOv8:** Detecta automáticamente vagonetas y placas en imágenes/videos.
- **Tesseract OCR:** Extrae el número de chapa de las vagonetas.
- **python-dotenv:** Maneja variables de entorno para configuración flexible.
- **aiofiles:** Manipula archivos de forma asíncrona.
- **python-multipart:** Soporta formularios y archivos subidos vía HTTP.

## Flujo de Procesamiento
1. El usuario sube una imagen o video desde el frontend.
2. El backend procesa el archivo:
   - Detecta la vagoneta y recorta la placa.
   - Aplica OCR para extraer el número.
   - Clasifica el modelo de ladrillo (visión computacional).
   - Registra el evento en MongoDB.
3. El usuario puede consultar los registros desde el frontend.

## Instalación manual

### 1. Requisitos previos
- Python 3.9+ instalado y en PATH
- MongoDB Community Server instalado y corriendo
- Tesseract OCR instalado en C:\Program Files\Tesseract-OCR

### 2. Crear y activar entorno virtual
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate
```

### 3. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 4. Configurar MongoDB
```powershell
# Inicializar base de datos y crear índices
python init_db.py
```

### 5. Configurar variables de entorno (opcional)
Crea un archivo `.env` si necesitas personalizar la configuración:
```ini
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DB=vagonetas_db

# OCR Configuration
TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# Image Processing
MIN_CONFIDENCE=0.5
DETECTION_COOLDOWN=5
```

### 6. Ejecutar el servidor
```powershell
uvicorn main:app --reload
```

## Endpoints principales
- `POST /upload/` — Sube imagen, procesa y guarda metadatos
- `POST /upload-multiple/` — Sube varias imágenes en una sola petición
- `POST /cameras/start` — Inicia captura desde cámara
- `POST /cameras/stop/{camera_id}` — Detiene una cámara
- `GET /cameras/status` — Estado de cámaras activas
- `GET /vagonetas/` — Consulta historial, filtra por número y fecha
- `GET /trayectoria/{numero}` — Eventos de una vagoneta ordenados por fecha

## Estructura de archivos
```
backend/
├── main.py              # Punto de entrada y API
├── crud.py             # Operaciones de base de datos
├── database.py         # Configuración MongoDB
├── schemas.py          # Modelos de datos
├── init_db.py          # Inicialización de DB
├── requirements.txt    # Dependencias
└── utils/
    ├── camera_capture.py   # Manejo de cámaras
    ├── image_processing.py # Procesamiento de imágenes
    └── ocr.py             # OCR para números
```

## Base de datos
- MongoDB local en `mongodb://localhost:27017`
- Base de datos: `vagonetas_db`
- Colección principal: `vagonetas`

## Documentación
- Accede a la documentación interactiva en http://localhost:8000/docs
- Prueba los endpoints directamente desde la interfaz Swagger

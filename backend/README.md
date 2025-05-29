# Backend - Seguimiento de Vagonetas

## ¿Para qué sirve?
Permite recibir imágenes de vagonetas, procesarlas con visión computacional y registrar automáticamente los datos clave de cada movimiento en la fábrica de ladrillos.

## Instalación rápida

### Requisitos previos
- Python 3.9+
- MongoDB (local o en la nube)
- Git

### 1. Clona el repositorio
```bash
# Clona el repositorio y entra al backend
 git clone <URL_DEL_REPOSITORIO>
 cd ElDorado/backend
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura variables de entorno (opcional)
Crea un archivo `.env` si quieres personalizar la conexión a MongoDB:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=vagonetas_db
```

### 4. Coloca el modelo YOLOv8 entrenado
Copia tu modelo en `backend/models/yolov8_vagonetas.pt`.

### 5. Inicia MongoDB
Asegúrate de que el servicio de MongoDB esté corriendo.

### 6. Ejecuta el backend
```bash
uvicorn main:app --reload
```

El backend estará disponible en http://localhost:8000

## ¿Cómo probar?
- Accede a la documentación interactiva en http://localhost:8000/docs
- Usa el frontend o herramientas como Postman/curl para probar los endpoints.

## Endpoints principales
- `POST /upload/` — Sube imagen, procesa y guarda metadatos.
- `POST /upload-multiple/` — Sube varias imágenes en una sola petición.
- `GET /vagonetas/` — Consulta historial, filtra por número y fecha.
- `GET /trayectoria/{numero}` — Devuelve todos los eventos (ingreso/egreso) de una vagoneta, ordenados por fecha.
- `GET /uploads/{filename}` — Acceso a imágenes subidas.
- `GET /health` — Verifica que el backend está corriendo.

## Tecnologías utilizadas
- **FastAPI** — API REST en Python
- **MongoDB** — Base de datos NoSQL
- **OpenCV** — Procesamiento de imágenes
- **Ultralytics YOLOv8** — Detección automática de vagonetas y placas
- **Tesseract OCR** — Reconocimiento óptico de caracteres
- **React** — Interfaz web

## Cambios recientes (Mayo 2025)

- Ahora **solo se guarda la imagen y los datos si se detecta un número de vagoneta** en la imagen subida. Si no se detecta, la imagen se elimina automáticamente y se informa al usuario.
- El endpoint `/upload-multiple/` devuelve un listado indicando cuáles imágenes fueron ignoradas (`status: "ignored"`) y el motivo.
- El frontend muestra mensajes claros sobre imágenes exitosas, ignoradas y fallidas.
- **El flujo principal es la captura automática desde cámaras físicas.** La carga manual de imágenes es solo para pruebas o casos excepcionales.

## Notas
- El modelo YOLOv8 debe estar entrenado y ubicado en `backend/models/yolov8_vagonetas.pt`.
- Puedes ajustar el procesamiento en `backend/utils/image_processing.py` y `ocr.py`.
- Para producción, configura almacenamiento externo y variables de entorno.

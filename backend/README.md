# Backend - Seguimiento de Vagonetas

## ¿Para qué sirve?
Permite recibir imágenes de vagonetas, procesarlas con visión computacional y registrar automáticamente los datos clave de cada movimiento en la fábrica de ladrillos.

## Instalación rápida (para desarrollo)

### Requisitos previos
- Python 3.9+
- MongoDB (local o en la nube) EN DESAROLLO
- Git

### 1. Clona el repositorio
```powershell
git clone <URL_DEL_REPOSITORIO>
cd app_imagenes/backend
```

### 2. Instala las dependencias
```powershell
pip install -r requirements.txt
```

### 3. Configura variables de entorno (opcional) EN DESAROLLO
Crea un archivo `.env` si quieres personalizar la conexión a MongoDB:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=vagonetas_db
```

### 4. Coloca el modelo YOLOv8 entrenado EN DESAROLLO
Copia tu modelo en `backend/models/yolov8_vagonetas.pt`.

### 5. Inicia MongoDB EN DESAROLLO
Asegúrate de que el servicio de MongoDB esté corriendo.

### 6. Ejecuta el backend
```powershell
uvicorn main:app --reload
```

El backend estará disponible en http://localhost:8000

## ¿Cómo probar?
- Accede a la documentación interactiva en http://localhost:8000/docs
- Usa el frontend o herramientas como Postman/curl para probar los endpoints.

## Tecnologías utilizadas
- **FastAPI:** Framework web moderno y rápido para construir APIs en Python.
- **Uvicorn:** Servidor ASGI para correr aplicaciones FastAPI de forma eficiente.
- **Motor y PyMongo:** Conectores asíncronos y síncronos para trabajar con MongoDB desde Python. EN DESAROLLO
- **OpenCV:** Librería de visión computacional para manipulación y procesamiento de imágenes.
- **Ultralytics YOLOv8:** Modelo de inteligencia artificial para detección automática de objetos (vagonetas y placas numeradas). EN DESAROLLO
- **Tesseract OCR:** Motor de reconocimiento óptico de caracteres para leer los números calados en las placas. EN DESAROLLO
- **python-dotenv:** Permite cargar variables de entorno desde archivos .env para configuración flexible.

## Estructura de la base de datos (MongoDB) EN DESAROLLO
Cada registro de vagoneta contiene:
- `numero`: número detectado en la placa
- `imagen_path`: ruta de la imagen
- `timestamp`: fecha y hora del evento
- `tunel`: túnel/pasillo (opcional)
- `evento`: 'ingreso' o 'egreso'
- `modelo_ladrillo`: modelo de ladrillo (opcional)
- `merma`: porcentaje de merma/fisuración (opcional)

## Endpoints principales
- `POST /upload/` — Sube imagen, procesa y guarda metadatos.
- `POST /upload-multiple/` — Sube varias imágenes en una sola petición.
- `GET /vagonetas/` — Consulta historial, filtra por número y fecha.
- `GET /trayectoria/{numero}` — Devuelve todos los eventos (ingreso/egreso) de una vagoneta, ordenados por fecha.
- `GET /uploads/{filename}` — Acceso a imágenes subidas.
- `GET /health` — Verifica que el backend está corriendo.

## ¿Cómo funciona?
1. El usuario sube una o varias imágenes desde el frontend.
2. El backend guarda la(s) imagen(es) y procesa cada una con YOLOv8 y Tesseract OCR. EN DESAROLLO
3. Se detecta el número de vagoneta, se asocian los metadatos (evento, túnel, modelo, merma, timestamp) y se guarda todo en MongoDB. EN DESAROLLO
4. Los datos pueden ser consultados y filtrados desde la web.

## Notas
- Edita la URI de MongoDB en `database.py` si es necesario. EN DESAROLLO
- El modelo YOLOv8 debe estar en `models/yolov8_vagonetas.pt`. EN DESAROLLO
- Requiere MongoDB corriendo localmente o en la nube. EN DESAROLLO
- Para producción, usar almacenamiento externo para imágenes. EN DESAROLLO

# Sistema El Dorado - Detección de Números Calados

**Profesores a Cargo:**
- Nicolás Caballero
- Federico Magaldi
- Martín Mirabete
- Carlos Ghio

# Proyecto - Sistema de Detección de Números Calados en Vagonetas

Este proyecto integra visión computacional avanzada y aprendizaje profundo (YOLOv8) para automatizar la detección y reconocimiento de números calados en vagonetas de carga en tiempo real. El sistema utiliza inteligencia artificial para procesar video en vivo, detectar números automáticamente y registrar todas las detecciones en una base de datos MongoDB para análisis posterior.

## 🎯 Características Principales

- **🤖 Detección Automática con IA**: Modelo YOLOv8 entrenado específicamente para números calados
- **📹 Procesamiento de Video en Tiempo Real**: Análisis continuo de video con detección automática
- **🗄️ Base de Datos MongoDB**: Almacenamiento persistente de todas las detecciones
- **🌐 Interfaz Web Moderna**: Frontend React con video streaming en vivo
- **📊 Historial Completo**: Consulta y análisis de detecciones históricas
- **📚 Manual de Usuario Integrado**: Guía completa accesible desde la interfaz

## 📂 Estructura del Proyecto

```
ElDorado/
│   README.md                # Documentación general del proyecto
│
├── backend/                 # 🚀 Backend FastAPI con IA
│   ├── main.py              # Servidor principal con endpoints de video streaming
│   ├── crud.py              # Operaciones de base de datos
│   ├── database.py          # Configuración MongoDB
│   ├── schemas.py           # Modelos de datos
│   ├── requirements.txt     # Dependencias Python
│   ├── README.md            # Documentación del backend
│   ├── models/              # 🤖 Modelos de IA organizados
│   │   ├── numeros_calados/ # Modelo YOLOv8 para números calados
│   │   │   └── yolo_model/
│   │   │       ├── dataset/
│   │   │       │   └── CarroNcalados800.mp4  # Video de demostración
│   │   │       └── training/
│   │   │           └── best.pt              # Modelo entrenado
│   │   └── numeros_enteros/ # Modelo adicional para números enteros
│   └── utils/               # 🔧 Utilidades especializadas
│       ├── auto_capture_system.py    # Sistema de captura automática
│       ├── image_processing.py       # Procesamiento con YOLO
│       ├── camera_capture.py         # Manejo de cámaras/video
│       └── ocr.py                   # OCR complementario
│
├── frontend/                # 🌐 Frontend React moderno
│   ├── package.json         # Dependencias React
│   ├── tailwind.config.js   # Configuración Tailwind CSS
│   ├── README.md            # Documentación del frontend
│   ├── public/              # Archivos estáticos
│   │   ├── index.html       # HTML principal
│   │   └── logo.jpg         # Logo del proyecto
│   └── src/                 # 📱 Código fuente React
│       ├── App.js           # Aplicación principal
│       ├── index.js         # Punto de entrada
│       ├── components/      # Componentes especializados
│       │   ├── VideoPlayer.js           # Reproductor de video streaming
│       │   ├── VideoTrainingMonitor.js  # Monitor de detecciones IA
│       │   ├── ManualUsuario.js         # Manual integrado
│       │   ├── Historial.js             # Historial de detecciones
│       │   └── Navbar.js                # Navegación principal
│       └── config/
│           └── api.js       # Configuración de endpoints
```
│           ├── CameraCapture.css    # Estilos de cámara
│           ├── GuiaUsuario.js       # Guía de usuario integrada
│           ├── Historial.js         # Tabla de historial de registros
│           ├── Navbar.js            # Barra de navegación
│           ├── Spinner.js           # Indicador de carga
│           ├── Trayectoria.js       # Consulta de trayectoria de vagonetas
│           └── Upload.js            # Formulario para subir imágenes
├── NumerosCalados/

├── dataset/ # Dataset de entrenamiento

┃          ├── CarroNumCalados_v2.mp4 # Video original con números calados

┃          ┣ readme.dataset # Descripción del dataset

           ┣ training/ # Código de entrenamiento

┃          ┣ train.py # Script para entrenar YOLOv8

┃          ┣ data.yaml # Configuración del dataset

┃          ┣ best.pt # Modelo YOLOv8 entrenado

├── detection/ # Código de inferencia

┃          ┣ detect_video.py # Detección en videos

├── results/ # Datos generados tras la detección

┃          ┣ detecciones.json # Resultados en formato JSON

┃          ┣ video_prueba.mp4 # Video con detección aplicada

┣ readme.rpbpflow # Información sobre el dataset en Roboflow
...


## Visión y Objetivo General
Desarrollar un sistema de visión computacional que permita identificar y trazar los movimientos de producción en proceso, asegurando la trazabilidad de los ladrillos respecto a las condiciones de secado.

### Objetivos Particulares
- Identificar automáticamente las vagonetas cargadas de ladrillos que pasan por un punto de control.
- Identificar el modelo de ladrillos cargado en cada vagoneta.

## Instalación del Proyecto

### Requisitos Previos
1. **Python 3.9+**
   - Descarga e instala Python desde [python.org](https://python.org)
   - Asegúrate de marcar "Add Python to PATH" durante la instalación

2. **MongoDB Community Server**
   - Descarga MongoDB Community Server desde [mongodb.com](https://www.mongodb.com/try/download/community)
   - Durante la instalación, selecciona "Ejecutar como servicio de Windows"
   - La base de datos se ejecutará automáticamente al iniciar Windows

3. **Node.js**
   - Descarga e instala Node.js desde [nodejs.org](https://nodejs.org)
   - Se recomienda la versión LTS (Long Term Support)

4. **Tesseract OCR**
   - Descarga Tesseract desde [github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - Instala en la ruta por defecto (C:\Program Files\Tesseract-OCR)

### Instalación Rápida con Script Automático

**🚀 Nueva opción recomendada:**

1. Clona o descarga este repositorio desde GitHub.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el script de configuración automática:
   ```powershell
   python setup_sistema.py
   ```
4. El script configurará automáticamente:
   - Entorno virtual de Python
   - Dependencias del backend y frontend
   - Archivos de configuración
   - Scripts de inicio automático
5. Sigue las instrucciones en pantalla para completar la configuración.

### Instalación Manual (Método Tradicional)

1. Clona o descarga este repositorio desde GitHub.
2. Abre una terminal (PowerShell o CMD) y navega hasta la carpeta del proyecto.

#### Backend (FastAPI + Python)
1. Ve a la carpeta del backend:
   ```powershell
   cd backend
   ```
2. (Opcional pero recomendado) Crea y activa un entorno virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
3. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Inicia el backend:
   ```powershell
   uvicorn main:app --reload
   ```
   El backend estará disponible en http://localhost:8000

#### Frontend (React)
1. Abre otra terminal y navega a la carpeta del frontend:
   ```powershell
   cd frontend
   ```
2. Instala las dependencias:
   ```powershell
   npm install
   ```
3. Inicia el frontend:
   ```powershell
   npm start
   ```
   El frontend estará disponible en http://localhost:3000

#### Acceso a la aplicación
- Frontend: http://localhost:3000
- API Backend: http://localhost:8000

## Estado Actual
- ✅ **Modelo NumerosCalados Activo**: Sistema configurado para usar el modelo YOLOv8 entrenado específicamente para números calados
- ✅ **Interfaz web y backend funcionales**: Permiten subir imágenes, registrar eventos, consultar historial y trayectoria de vagonetas
- ✅ **Procesamiento de imágenes avanzado**: YOLOv8 + OCR optimizado para identificar vagonetas con números calados
- ✅ **Sistema de captura automática**: Detección de movimiento inteligente con filtros anti-ruido
- ✅ **Monitor en tiempo real**: Panel de estadísticas y monitoreo en vivo del sistema
- ✅ **Base de datos MongoDB**: Almacenamiento estructurado de metadatos y rutas de imágenes
- ✅ **Manual de Usuario Integrado**: Documentación educativa completa accesible desde la interfaz web
- 🔄 **Configuración automática**: Script de setup para instalación y configuración del sistema completo

### 📚 **Manual de Usuario Integrado**
El sistema ahora incluye un manual completo accesible directamente desde la interfaz web:

- **🔢 Sistema de Numeración**: Explicación detallada de números calados vs números enteros
- **🚀 Guía de Inicio Rápido**: Instrucciones paso a paso para comenzar a usar el sistema
- **📖 Casos de Uso**: Ejemplos prácticos de diferentes escenarios de detección
- **🔧 Resolución de Problemas**: Guía de troubleshooting para errores comunes
- **❓ Preguntas Frecuentes**: FAQ con respuestas a consultas habituales
- **⚙️ Especificaciones Técnicas**: Detalles sobre hardware, software y configuración

**Acceso**: Hacer clic en el botón "📚 Manual de Usuario" en la barra de navegación superior.

## Mejoras Recientes - Modelo NumerosCalados

### 🧠 **Optimización del Modelo de IA**
- **Modelo específico**: Migración de NumerosEnteros a **NumerosCalados** para mayor precisión
- **29 clases detectables**: Entrenado para reconocer números específicos (01, 010, 011, 012, 0123, 013, etc.)
- **Mayor precisión**: Optimizado específicamente para números calados en vagonetas
- **Confianza mejorada**: Sistema de scoring para validar la calidad de las detecciones

### 🤖 **Sistema de Captura Automática**
- **Detección de movimiento inteligente**: Algoritmo MOG2 con filtros anti-ruido
- **Buffer pre-captura**: Mantiene frames anteriores para mejor análisis
- **Cooldown inteligente**: Evita detecciones duplicadas en el mismo vehículo
- **Estadísticas en tiempo real**: Monitoreo de eficiencia y falsos positivos
- **Configuración flexible**: Ajuste de sensibilidad por cámara

### 📊 **Interfaz Mejorada**
- **Monitor en tiempo real**: Dashboard con estadísticas en vivo
- **Control automático**: Panel para iniciar/detener captura automática
- **Historial enriquecido**: Muestra confianza del modelo y origen de captura
- **Visualización mejorada**: Indicadores de estado y eficiencia del sistema

## Mejoras Futuras / Pendientes
- Integrar reconocimiento automático de modelo de ladrillo (visión computacional).
- Integrar datos termo-higrométricos y asociarlos a los registros de vagonetas.
- Mejorar la gestión de errores y validaciones.
- Agregar filtros avanzados y reportes personalizados.
- Documentar recomendaciones de hardware y almacenamiento.
- Mejorar la ayuda y documentación para usuarios finales.

## Requerimientos Funcionales (Alto Nivel)
- Detección e identificación automática de vagonetas en puntos de ingreso y egreso.
- Registro automático de fecha y hora de ingreso y egreso.
- Identificación del modelo de ladrillo cargado.
- Determinación del túnel/pasillo de salida y reconstrucción de la trayectoria.
- Almacenamiento estructurado de datos y rutas de imágenes en MongoDB.
- Generación de historial y reportes por vagoneta.
- Integración futura con sensores de temperatura y humedad.
- Registro de merma/fisuración para retroalimentar el sistema.

## Interfaces
- Interfaz web (React) para usuarios.
- API REST (FastAPI) para procesamiento y consulta de datos.
- Integración con MongoDB para metadatos y almacenamiento externo para imágenes.
- Futuro: integración con sistema de sensores de temperatura y humedad.

## Tecnologías Utilizadas y Dependencias

### Backend (Python)
- **fastapi**: Framework para construir APIs REST modernas y eficientes.
- **aiofiles**: Manejo asíncrono de archivos, útil para subir imágenes y videos.
- **python-dotenv**: Gestión de variables de entorno para configuración flexible.
- **python-multipart**: Soporte para formularios y archivos subidos vía HTTP en FastAPI.
- **pymongo**: Conector para interactuar con MongoDB desde Python.
- **opencv-python**: Procesamiento y manipulación de imágenes y videos.
- **ultralytics**: Implementación de modelos YOLO para detección automática de vagonetas y placas.
- **pytesseract**: Reconocimiento óptico de caracteres (OCR) para extraer números de chapa.

### Frontend (JavaScript/React)
- **react**: Biblioteca principal para construir la interfaz web.
- **react-dom**: Renderizado de componentes React en el DOM.
- **react-scripts**: Scripts y utilidades para desarrollo y build de la app React.
- **axios**: Cliente HTTP para comunicación frontend-backend.
- **tailwindcss**: Framework de utilidades CSS para diseño moderno y responsivo.
- **autoprefixer**: Añade automáticamente prefijos CSS para compatibilidad entre navegadores.
- **postcss**: Herramienta para transformar CSS con plugins.
- **@tailwindcss/postcss**: Integración de Tailwind con PostCSS.

## ¿Cómo Funciona la App?
1. El usuario sube una o varias imágenes (o videos) de vagonetas desde la web.
2. El backend procesa cada imagen/video, detecta el número de vagoneta y el modelo de ladrillo usando modelos de visión computacional y OCR, y guarda los datos en MongoDB.
3. El usuario puede consultar el historial, filtrar por número, fecha, evento, modelo o merma, y ver la trayectoria completa de cada vagoneta desde el frontend.

## Uso Típico
- Subir imágenes o videos de vagonetas indicando evento, túnel, modelo y merma.
- Consultar historial y trayectoria de cada vagoneta.
- Analizar la trazabilidad y calidad del proceso productivo.

## Notas
- El modelo YOLOv8 debe estar entrenado y ubicado en `backend/models/yolov8_vagonetas.pt`.
- Puedes ajustar el procesamiento en `backend/utils/image_processing.py` y `ocr.py`.
- Para producción, configura almacenamiento externo y variables de entorno.
- La documentación de la API está disponible en `/docs` del backend.

---

## Requerimientos Cubiertos

**1. Detección e identificación automática de vagonetas**
- ✔️ Subida de imágenes y detección automática del número de placa con YOLOv8 + Tesseract OCR.

**2. Registro de fecha y hora de ingreso y egreso**
- ✔️ Registro automático de fecha y hora en cada evento.

**3. Determinación de trayectoria y túnel**
- ✔️ El usuario indica el túnel/pasillo y la trayectoria se reconstruye en la vista correspondiente.

**4. Almacenamiento estructurado de datos**
- ✔️ Metadatos en MongoDB y rutas de imágenes en disco.

**5. Interfaz de usuario web**
- ✔️ Frontend en React para subir imágenes, consultar historial y ver trayectoria.

**6. Registro de modelo de ladrillo y merma**
- ✔️ Registro manual de modelo y merma al subir la imagen.

**7. Escalabilidad y tecnologías recomendadas**
- ✔️ Python (FastAPI) para backend, React para frontend y MongoDB como base de datos.

---

## Pendientes y Opcionales

**1. Captura automática desde cámaras**
- ❌ El sistema espera imágenes ya capturadas. No incluye (aún) la captura automática desde cámaras de video. Puede lograrse con scripts adicionales usando OpenCV. Se requiere información sobre las cámaras.

**2. Reconocimiento automático del modelo de ladrillo**
- ⚠️ Actualmente el modelo de ladrillo se ingresa manualmente. La identificación automática es una mejora futura.

**3. Integración de datos termo-higrométricos**
- ⚠️ No está implementada la integración automática de datos de temperatura y humedad. Es un alcance futuro.

**4. Filtros avanzados y reportes personalizados**
- ⚠️ Se pueden agregar filtros avanzados y reportes a medida.

**5. Mejoras en validaciones y manejo de errores**
- ⚠️ Se puede robustecer la validación de datos y el manejo de errores en backend y frontend.

**6. Automatización de la retroalimentación de merma/fisuración**
- ⚠️ El registro es manual. Puede mejorarse para análisis y optimización futura.

**7. Documentación de hardware y recomendaciones de almacenamiento**
- ⚠️ Se recomienda agregar una sección sobre cámaras, servidores y almacenamiento externo.

---

## Cambios recientes 

- El backend ahora **solo guarda imágenes y registros cuando se detecta un número de vagoneta** en la imagen. Si no se detecta, la imagen se elimina automáticamente y no se almacena en la base de datos.
- El endpoint `/upload-multiple/` informa en la respuesta cuántas imágenes fueron ignoradas por no contener vagoneta identificable (`status: "ignored"`).
- El frontend muestra mensajes claros al usuario sobre imágenes exitosas, ignoradas y fallidas.

---


# Prácticas Profesionalizantes 2

**Profesores a Cargo:**
- Nicolás Caballero
- Federico Magaldi
- Martín Mirabete
- Carlos Ghio

# Proyecto - Reconocimiento de Ladrillos y/o Bloques

Este proyecto integra visión computacional y aprendizaje profundo para automatizar la identificación y trazabilidad de vagonetas y modelos de ladrillos en una línea de producción de fábrica. El sistema permite registrar, consultar y analizar los movimientos de cada vagoneta, asociando eventos de ingreso y egreso, modelo de ladrillo, merma y trayectoria, facilitando la optimización y control de calidad del proceso productivo.

## 📂 Estructura del Repositorio

```
ElDorado/
│   README.md                # Documentación general, visión, requerimientos y guía de uso
│
├── backend/                 # Backend: API, procesamiento de imágenes, conexión a MongoDB
│   ├── main.py              # Punto de entrada FastAPI, define los endpoints principales
│   ├── crud.py              # Funciones CRUD para la base de datos
│   ├── database.py          # Configuración y conexión a MongoDB
│   ├── schemas.py           # Modelos de datos (Pydantic)
│   ├── requirements.txt     # Dependencias Python necesarias
│   ├── README.md            # Documentación específica del backend
│   └── utils/               # Utilidades para procesamiento de imágenes
│       ├── image_processing.py  # Detección de vagonetas y placas con YOLOv8
│       └── ocr.py               # Reconocimiento de caracteres (OCR) en placas
│
├── frontend/                # Frontend: interfaz web en React
│   ├── package.json         # Dependencias y scripts de React
│   ├── README.md            # Documentación específica del frontend
│   ├── public/              # Archivos públicos y estáticos
│   │   ├── logo.jpg         # Logo de la empresa
│   │   ├── index.html       # HTML principal
│   │   └── ...              # Otros recursos estáticos
│   └── src/                 # Código fuente de React
│       ├── App.js           # Componente principal de la app
│       ├── App.css          # Estilos globales
│       ├── index.js         # Punto de entrada de React
│       └── components/      # Componentes reutilizables
│           ├── Upload.js        # Formulario para subir imágenes
│           ├── Historial.js     # Tabla de historial de registros
│           └── Trayectoria.js   # Consulta de trayectoria de vagonetas
```

## Visión y Objetivo General
Desarrollar un sistema de visión computacional que permita identificar y trazar los movimientos de producción en proceso, asegurando la trazabilidad de los ladrillos respecto a las condiciones de secado.

### Objetivos Particulares
- Identificar automáticamente las vagonetas cargadas de ladrillos que pasan por un punto de control.
- Identificar el modelo de ladrillos cargado en cada vagoneta.

## Instalación del Proyecto
Para instalar y ejecutar el sistema, sigue los pasos detallados en los archivos `README.md` de las carpetas `backend/` y `frontend/`.
- El backend (API y procesamiento) está en `backend/README.md`.
- El frontend (interfaz web) está en `frontend/README.md`.

## Estado Actual
- Interfaz web y backend funcionales: permiten subir imágenes, registrar eventos, consultar historial y trayectoria de vagonetas.
- Procesamiento de imágenes con YOLOv8 y OCR para identificar vagonetas y registrar metadatos.
- Estructura de base de datos y almacenamiento de imágenes implementados.

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

## Tecnologías Utilizadas
- **FastAPI:** API REST moderna y eficiente en Python.
- **Uvicorn:** Servidor ASGI para FastAPI.
- **MongoDB:** Base de datos NoSQL para metadatos y registros.
- **Motor/PyMongo:** Conectores para interactuar con MongoDB.
- **OpenCV:** Procesamiento y manipulación de imágenes.
- **Ultralytics YOLOv8:** Detección automática de vagonetas y placas numeradas.
- **Tesseract OCR:** Reconocimiento óptico de caracteres en placas.
- **React:** Interfaz web interactiva y moderna.
- **Axios:** Cliente HTTP para comunicación frontend-backend.
- **python-dotenv:** Manejo flexible de variables de entorno.

## ¿Cómo Funciona la App?
1. El usuario sube una o varias imágenes de vagonetas desde la web.
2. El backend procesa cada imagen, detecta el número de vagoneta, asocia los datos (evento, túnel, modelo, merma, timestamp) y guarda todo en MongoDB.
3. El usuario puede consultar el historial, filtrar por número, fecha, evento, modelo o merma, y ver la trayectoria completa de cada vagoneta.

## Uso Típico
- Subir imágenes de vagonetas indicando evento, túnel, modelo y merma.
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

**6. API REST documentada**
- ✔️ Endpoints REST documentados y accesibles desde `/docs`.

**7. Registro de modelo de ladrillo y merma**
- ✔️ Registro manual de modelo y merma al subir la imagen.

**8. Escalabilidad y tecnologías recomendadas**
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


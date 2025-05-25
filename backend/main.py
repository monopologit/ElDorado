# main.py - Backend principal de la app de seguimiento de vagonetas
# Autor: [Tu nombre o equipo]
# Descripción: API REST para subir, procesar y consultar registros de vagonetas usando visión computacional.

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Query, Form
from pathlib import Path
import shutil
import os
from datetime import datetime
from . import crud, schemas
import asyncio
from utils.image_processing import detectar_vagoneta_y_placa
from utils.ocr import ocr_placa_img
import cv2
import numpy as np
from typing import List

# Inicializa la app FastAPI
app = FastAPI()

# Habilita CORS para permitir peticiones desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta donde se guardan las imágenes subidas
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Sirve las imágenes subidas como archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- ENDPOINTS PRINCIPALES ---

@app.post("/upload/", summary="Subir imagen de vagoneta", description="Sube una imagen, detecta el número de vagoneta y guarda los metadatos. Requiere campo 'evento' (ingreso/egreso) y opcional 'tunel', 'modelo_ladrillo', 'merma'.")
async def upload_image(
    file: UploadFile = File(...),
    tunel: str = Form(None),
    evento: str = Form(...),
    modelo_ladrillo: str = Form(None),
    merma: float = Form(None)
):
    """
    Sube una imagen de vagoneta, la procesa con visión computacional y guarda los metadatos en MongoDB.
    - file: imagen de la vagoneta
    - tunel: túnel/pasillo (opcional)
    - evento: 'ingreso' o 'egreso' (obligatorio)
    - modelo_ladrillo: modelo de ladrillo (opcional)
    - merma: porcentaje de merma/fisuración (opcional)
    """
    # Guarda la imagen en disco
    file_ext = file.filename.split(".")[-1]
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    save_path = UPLOAD_DIR / f"{timestamp}_{file.filename}"
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Procesa la imagen con YOLOv8 y OCR para detectar el número de vagoneta
    cropped_placa_img, bbox_vagoneta, bbox_placa = detectar_vagoneta_y_placa(str(save_path))
    numero_detectado = None
    if cropped_placa_img is not None:
        numero_detectado = ocr_placa_img(cropped_placa_img)
    # Guarda los metadatos en MongoDB
    vagoneta = schemas.VagonetaCreate(
        numero=numero_detectado,
        imagen_path=f"uploads/{save_path.name}",
        timestamp=datetime.utcnow(),
        tunel=tunel,
        evento=evento,
        modelo_ladrillo=modelo_ladrillo,
        merma=merma
    )
    await crud.create_vagoneta_record(vagoneta)
    return JSONResponse({"message": "Imagen subida", "numero_detectado": numero_detectado, "evento": evento, "modelo_ladrillo": modelo_ladrillo, "merma": merma, "path": str(save_path)})

@app.post("/upload-multiple/", summary="Subir múltiples imágenes de vagonetas", description="Sube varias imágenes en una sola petición. Requiere campo 'evento' (ingreso/egreso) y opcional 'tunel', 'modelo_ladrillo', 'merma'.")
async def upload_images(
    files: List[UploadFile] = File(...),
    tunel: str = Form(None),
    evento: str = Form(...),
    modelo_ladrillo: str = Form(None),
    merma: float = Form(None)
):
    """
    Sube varias imágenes de vagonetas, las procesa y guarda los metadatos en MongoDB.
    - files: lista de imágenes
    - tunel: túnel/pasillo (opcional)
    - evento: 'ingreso' o 'egreso' (obligatorio)
    - modelo_ladrillo: modelo de ladrillo (opcional)
    - merma: porcentaje de merma/fisuración (opcional)
    """
    results = []
    for file in files:
        try:
            file_ext = file.filename.split(".")[-1]
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            save_path = UPLOAD_DIR / f"{timestamp}_{file.filename}"
            with save_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            # Procesa la imagen con YOLOv8 y OCR
            cropped_placa_img, bbox_vagoneta, bbox_placa = detectar_vagoneta_y_placa(str(save_path))
            numero_detectado = None
            if cropped_placa_img is not None:
                numero_detectado = ocr_placa_img(cropped_placa_img)
            vagoneta = schemas.VagonetaCreate(
                numero=numero_detectado,
                imagen_path=f"uploads/{save_path.name}",
                timestamp=datetime.utcnow(),
                tunel=tunel,
                evento=evento,
                modelo_ladrillo=modelo_ladrillo,
                merma=merma
            )
            await crud.create_vagoneta_record(vagoneta)
            results.append({"filename": file.filename, "status": "ok", "numero_detectado": numero_detectado, "evento": evento, "modelo_ladrillo": modelo_ladrillo, "merma": merma})
        except Exception as e:
            results.append({"filename": file.filename, "status": "error", "error": str(e)})
    return {"results": results}

@app.get("/vagonetas/", response_model=list[schemas.VagonetaInDB], summary="Consultar historial de vagonetas", description="Consulta el historial de registros de vagonetas. Permite filtrar por número y fecha.")
async def get_vagonetas(numero: str = Query(None, description="Número de vagoneta"), fecha: str = Query(None, description="Fecha en formato YYYY-MM-DD")):
    """
    Devuelve el historial de registros de vagonetas, con opción de filtrar por número o fecha.
    """
    registros = await crud.get_vagonetas_historial(numero=numero, fecha=fecha)
    return registros

@app.get("/trayectoria/{numero}", response_model=list[schemas.VagonetaInDB], summary="Trayectoria de una vagoneta", description="Devuelve todos los eventos (ingreso/egreso) de una vagoneta, ordenados por fecha.")
async def trayectoria_vagoneta(numero: str):
    """
    Devuelve la trayectoria completa (ingresos y egresos) de una vagoneta, ordenada por fecha.
    """
    registros = await crud.get_vagonetas_historial(numero=numero)
    registros.sort(key=lambda r: r["timestamp"])
    return registros

@app.get("/health", summary="Healthcheck", description="Verifica que el backend está corriendo.")
def health():
    """Endpoint de salud para monitoreo."""
    return {"status": "ok"}

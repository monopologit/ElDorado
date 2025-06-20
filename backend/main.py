# main.py - Backend principal de la app de seguimiento de vagonetas
# Autor: [Tu nombre o equipo]
# Descripción: API REST para subir, procesar y consultar registros de vagonetas usando visión computacional.

import asyncio 
import shutil
import os
import uuid
import json
import traceback
import cv2 
import time

from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query, Form, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime, timezone # MODIFIED: Added timezone
from typing import List, Dict, Optional, Any

import crud 
from utils.image_processing import run_detection_on_path, run_detection_on_frame
from utils.auto_capture_system import AutoCaptureManager, load_cameras_config 
from database import connect_to_mongo, close_mongo_connection, get_database 
from collections import Counter # Keep if used elsewhere, not in provided snippets
from schemas import VagonetaCreate, VagonetaInDB, HistorialResponse, RegistroHistorialDisplay
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔌 WebSocket conectado: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"🔌❌ WebSocket desconectado: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_json_to_connection(self, data: dict, websocket: WebSocket):
        """Enviar mensaje JSON a una conexión específica"""
        try:
            await websocket.send_json(data)
        except Exception as e:
            print(f"❌ Error enviando mensaje JSON a {websocket.client}: {e}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

    async def broadcast_json(self, data: dict):
        print(f"📡 Broadcasting a {len(self.active_connections)} conexiones: {data.get('type', 'unknown')}")
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
                print(f"✅ Mensaje enviado a {connection.client}")
            except Exception as e:
                print(f"❌ Error enviando a {connection.client}: {e}")
                disconnected.append(connection)
        
        # Remover conexiones rotas
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

manager = ConnectionManager()

async def procesar_video_mp4_streamable(video_path: str, upload_dir: Path):
    yield {"type": "status", "stage": "initialization", "message": f"Iniciando procesamiento de video: {Path(video_path).name}"}
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        yield {"type": "error", "stage": "initialization", "message": f"Error al abrir el video: {video_path}"}
        return

    detections = {}  # Para agrupar por número: {numero: [lista de detecciones]}
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    yield {"type": "progress", "stage": "setup", "message": "Video abierto y listo para procesar.", "total_frames": total_frames, "current_frame": 0}

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                yield {"type": "status", "stage": "frame_processing", "message": "Fin de los frames o error al leer."}
                break
            
            frame_count += 1
            if frame_count % 5 != 0:  # Procesar cada N frames
                if frame_count % 100 == 0: 
                    yield {"type": "progress", "stage": "frame_processing", "message": f"Avanzando video...", "current_frame": frame_count, "total_frames": total_frames}
                continue

            yield {"type": "progress", "stage": "frame_processing", "message": f"Procesando frame {frame_count}/{total_frames}", "current_frame": frame_count, "total_frames": total_frames}

            if frame is None or frame.size == 0:
                yield {"type": "warning", "stage": "frame_processing", "message": f"Frame {frame_count} es None o está vacío."}
                continue

            try:
                # --- NUEVA LÓGICA DE DETECCIÓN UNIFICADA ---
                detection_results = run_detection_on_frame(frame)
                numero_detectado = detection_results.get('numero_detectado')
                confianza_numero = detection_results.get('confianza_numero')
                modelo_ladrillo = detection_results.get('modelo_ladrillo')
                # --- FIN DE LA NUEVA LÓGICA ---
                
                if numero_detectado and confianza_numero is not None:
                    confianza_float = 0.0
                    try:
                        confianza_float = float(confianza_numero)
                    except (ValueError, TypeError):
                        pass # Keep confianza_float as 0.0 or log warning

                    yield {
                        "type": "detection_update", 
                        "stage": "frame_processing",
                        "frame": frame_count, 
                        "numero": numero_detectado, 
                        "confianza": confianza_float,
                        "modelo": modelo_ladrillo
                    }
                    
                    # Guardar TODAS las detecciones significativas (no solo la mejor)
                    if confianza_float >= 0.5:  # Solo detecciones con confianza >= 50%
                        if numero_detectado not in detections:
                            detections[numero_detectado] = []
                        
                        # Guardar frame como imagen para esta detección
                        frame_filename = f"frame_{frame_count}_{numero_detectado}_{confianza_float:.3f}.jpg"
                        frame_path = upload_dir / frame_filename
                        cv2.imwrite(str(frame_path), frame)
                        
                        detections[numero_detectado].append({
                            'confianza': confianza_float,
                            'frame': frame_count,
                            'imagen_path': f"uploads/{frame_filename}",
                            'modelo_ladrillo': modelo_ladrillo
                        })
            except Exception as e_detect:
                yield {"type": "warning", "stage": "frame_processing", "message": f"Error detectando en frame {frame_count}: {str(e_detect)}"}
    except Exception as e_video:
        yield {"type": "error", "stage": "video_processing_error", "message": f"Error mayor durante el procesamiento del video: {str(e_video)}"}
        traceback.print_exc()
        return 
    finally:
        cap.release()
        yield {"type": "status", "stage": "cleanup", "message": f"Video {Path(video_path).name} procesado. Total frames leídos: {frame_count}."}

    if not detections:
        yield {"type": "final_result", "stage": "completion", "data": None, "message": "No se detectaron números en el video."}
    else:
        # Convertir a formato que mantenga todas las detecciones
        final_detections_serializable = {}
        for numero, lista_detecciones in detections.items():
            final_detections_serializable[numero] = lista_detecciones
        yield {"type": "final_result", "stage": "completion", "data": final_detections_serializable, "message": "Detecciones finales recopiladas."}

def parse_merma(merma_str: Optional[str]) -> Optional[float]:
    if not merma_str or merma_str.strip() == "":
        return None
    try:
        return float(merma_str)
    except (ValueError, TypeError):
        return None

live_frames: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    print("INFO:     Iniciando aplicación...")
    connect_to_mongo()
    app_instance.state.pending_video_processing = {} 
    print("INFO:     Aplicación iniciada y base de datos conectada.")
    yield
    print("INFO:     Cerrando aplicación...")
    if auto_capture_manager and auto_capture_manager.is_running():
        print("INFO:     Deteniendo sistema de captura automática...")
        await auto_capture_manager.stop_system()
    close_mongo_connection()
    print("INFO:     Aplicación apagada y conexión a base de datos cerrada.")

app = FastAPI(
    title="API de Seguimiento de Vagonetas",
    description="Sistema de trazabilidad y seguimiento de vagonetas con visión computacional",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
TEMP_CHUNK_DIR = UPLOAD_DIR / "temp_chunks"
TEMP_CHUNK_DIR.mkdir(exist_ok=True)

# Variables globales para monitoreo en vivo
monitor_tasks = {}  # Diccionario para manejar tareas de monitoreo activas

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads") # Ensure directory is string

@app.post("/upload-chunk/")
async def upload_chunk(
    fileId: str = Form(...),
    chunkIndex: int = Form(...),
    chunk: UploadFile = File(...)
):
    chunk_dir = TEMP_CHUNK_DIR / fileId
    chunk_dir.mkdir(parents=True, exist_ok=True)  # Ensure parent dirs and fileId dir exist

    chunk_filename = f"chunk_{chunkIndex}"
    save_path = chunk_dir / chunk_filename

    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(chunk.file, buffer)
        # Optional: print statement for server log
        # print(f"💾 Chunk {chunkIndex} para {fileId} guardado en {save_path}")
        return {"message": f"Chunk {chunkIndex} for {fileId} received and saved.", "status": "ok"}
    except Exception as e:
        # Optional: print statement for server log
        # print(f"❌ Error guardando chunk {chunkIndex} para {fileId}: {e}\\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error saving chunk {chunkIndex} for {fileId}: {str(e)}")

auto_capture_manager: Optional[AutoCaptureManager] = None 
auto_capture_task: Optional[asyncio.Task] = None 
CAMERAS_CONFIG = load_cameras_config() 

def sanitize_filename(filename: str) -> str:
    return "".join(c if c.isalnum() or c in ('.', '_', '-') else '_' for c in filename)

@app.post("/upload/", response_model=Dict)
async def upload_image(
    file: UploadFile = File(...),
    tunel: Optional[str] = Form(None),
    evento: str = Form(...),
    merma: Optional[str] = Form(None), 
    metadata_str: Optional[str] = Form(None) 
):
    parsed_metadata: Optional[Dict] = None
    if metadata_str:
        try:
            parsed_metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            print(f"Warning: Invalid metadata JSON string in /upload/: {metadata_str}")
            # Not raising HTTPException to allow processing if metadata is optional/auxiliary

    timestamp_obj = datetime.now(timezone.utc)
    filename_ts_str = timestamp_obj.strftime("%Y%m%d%H%M%S%f")
    sane_original_filename = sanitize_filename(Path(file.filename).name)
    save_path = UPLOAD_DIR / f"{filename_ts_str}_{sane_original_filename}"
    
    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # --- NUEVA LÓGICA DE DETECCIÓN UNIFICADA ---
        detection_results = run_detection_on_path(str(save_path))
        numero_detectado = detection_results.get('numero_detectado')
        modelo_ladrillo = detection_results.get('modelo_ladrillo')
        confianza_numero = detection_results.get('confianza_numero')
        # --- FIN DE LA NUEVA LÓGICA ---
        
        if not numero_detectado:
            try: os.remove(save_path)
            except Exception: pass
            return JSONResponse(
                {"message": "No se detectó vagoneta con número", "status": "ignored", "filename": file.filename},
                status_code=200
            )
        
        vagoneta_create_obj = VagonetaCreate(
            numero=str(numero_detectado),
            imagen_path=f"uploads/{save_path.name}",
            timestamp=timestamp_obj,
            tunel=tunel,
            evento=evento,
            modelo_ladrillo=modelo_ladrillo,
            merma=parse_merma(merma),
            metadata=parsed_metadata,
            confianza=float(confianza_numero) if confianza_numero is not None else None,
            origen_deteccion="image_upload"
        )
        record_id = crud.create_vagoneta_record(vagoneta_create_obj)
        
        db_record_dict = vagoneta_create_obj.dict()
        db_record_dict["_id"] = str(record_id)
        db_record_dict["id"] = str(record_id)
        if isinstance(db_record_dict.get("timestamp"), datetime):
            db_record_dict["timestamp"] = db_record_dict["timestamp"].isoformat()
        
        broadcast_message = {"type": "new_detection", "data": db_record_dict}
        asyncio.create_task(manager.broadcast_json(broadcast_message))

        return {
            "message": "Registro creado exitosamente", "status": "ok", "record_id": str(record_id),
            "numero_detectado": numero_detectado, "modelo_ladrillo": modelo_ladrillo,
            "confianza": confianza_numero, "filename": file.filename
        }

    except Exception as e:
        if save_path.exists():
            try: os.remove(save_path)
            except Exception: pass
        print(f"Error in /upload/ for {file.filename}: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error procesando imagen '{file.filename}': {str(e)}")

@app.post("/upload-multiple/")
async def upload_files(
    files: List[UploadFile] = File(...),
    tunel: Optional[str] = Form(None),
    evento: str = Form(...),
    merma: Optional[str] = Form(None),
    metadata_str: Optional[str] = Form(None)
):
    results = []
    parsed_metadata: Optional[Dict] = None
    if metadata_str:
        try:
            parsed_metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            print(f"Warning: Invalid metadata JSON string in /upload-multiple/: {metadata_str}")
            # Not raising, will proceed with metadata as None for records

    for file in files:
        current_file_save_path: Optional[Path] = None
        try:
            is_image = file.content_type and file.content_type.startswith('image/')
            # More specific video type check
            is_video = file.content_type and file.content_type.startswith('video/') and \
                       any(ct_suffix in file.content_type for ct_suffix in ['mp4', 'avi', 'mov', 'quicktime', 'mkv'])


            if not (is_image or is_video):
                results.append({
                    "filename": file.filename, "status": "error",
                    "error": f"Tipo de archivo no soportado: {file.content_type}."
                })
                continue
            
            timestamp_obj = datetime.now(timezone.utc)
            filename_ts_str = timestamp_obj.strftime("%Y%m%d%H%M%S%f")
            sane_original_filename = sanitize_filename(Path(file.filename).name)
            current_file_save_path = UPLOAD_DIR / f"{filename_ts_str}_{sane_original_filename}"
            
            with current_file_save_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            if is_video: # Videos are not processed by this endpoint directly
                results.append({
                    "filename": file.filename, "status": "video_not_processed",
                    "message": "Video subido. Usar subida individual con chunks para procesamiento.",
                    "path": f"uploads/{current_file_save_path.name}" # Provide path if needed later
                })
                # Do not remove the video, it's uploaded. User might use /finalize-upload if it was chunked,
                # or it's just stored. This endpoint is ambiguous for non-chunked videos.
                # For now, assume it's just uploaded and not processed.
                continue

            # Process if it's an image
            # --- NUEVA LÓGICA DE DETECCIÓN UNIFICADA ---
            detection_results = run_detection_on_path(str(current_file_save_path))
            numero_detectado = detection_results.get('numero_detectado')
            modelo_ladrillo = detection_results.get('modelo_ladrillo')
            confianza_numero = detection_results.get('confianza_numero')
            # --- FIN DE LA NUEVA LÓGICA ---
            
            if not numero_detectado:
                if current_file_save_path.exists(): os.remove(current_file_save_path)
                results.append({
                    "filename": file.filename, "status": "ignored",
                    "message": "No se detectó vagoneta con número"
                })
                continue
            
            vagoneta_create_obj = VagonetaCreate(
                numero=str(numero_detectado),
                imagen_path=f"uploads/{current_file_save_path.name}",
                timestamp=timestamp_obj,
                tunel=tunel,
                evento=evento,
                modelo_ladrillo=modelo_ladrillo,
                merma=parse_merma(merma),
                metadata=parsed_metadata,
                confianza=float(confianza_numero) if confianza_numero is not None else None,
                origen_deteccion="image_upload_multiple"
            )
            record_id = crud.create_vagoneta_record(vagoneta_create_obj)
            
            db_record_dict = vagoneta_create_obj.dict()
            db_record_dict["_id"] = str(record_id)
            db_record_dict["id"] = str(record_id)
            if isinstance(db_record_dict.get("timestamp"), datetime):
                db_record_dict["timestamp"] = db_record_dict["timestamp"].isoformat()
            broadcast_message = {"type": "new_detection", "data": db_record_dict}
            asyncio.create_task(manager.broadcast_json(broadcast_message))
            
            results.append({
                "filename": file.filename, "status": "ok", "record_id": str(record_id),
                "numero_detectado": numero_detectado, "modelo_ladrillo": modelo_ladrillo,
                "confianza": confianza_numero
            })
            
        except Exception as e:
            if current_file_save_path and current_file_save_path.exists():
                try: os.remove(current_file_save_path)
                except Exception: pass # Ignore cleanup error
            print(f"Error procesando archivo {file.filename} en /upload-multiple/: {e}\n{traceback.format_exc()}")
            results.append({
                "filename": file.filename, "status": "error", "error": str(e)
            })
    return {"results": results}

@app.post("/finalize-upload/")
async def finalize_upload(
    fileId: str = Form(...),
    originalFilename: str = Form(...),
    totalChunks: int = Form(...),
    tunel: Optional[str] = Form(None),
    evento: str = Form(...),
    merma: Optional[str] = Form(None),
    metadata_str: Optional[str] = Form(None)
):
    metadata: Optional[Dict] = None
    if metadata_str:
        try:
            metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid metadata JSON string")

    chunk_dir = TEMP_CHUNK_DIR / fileId
    if not chunk_dir.exists():
        raise HTTPException(status_code=404, detail=f"No chunks found for file ID: {fileId}")

    # Verify all chunks are present before assembly
    for i in range(totalChunks):
        chunk_path = chunk_dir / f"chunk_{i}"
        if not chunk_path.exists():
            shutil.rmtree(chunk_dir, ignore_errors=True) # Clean up partial upload
            raise HTTPException(status_code=400, detail=f"Missing chunk {i+1}/{totalChunks} for file ID: {fileId}")

    final_timestamp_obj = datetime.now(timezone.utc)
    filename_ts_str = final_timestamp_obj.strftime("%Y%m%d%H%M%S%f")
    sane_original_filename = sanitize_filename(Path(originalFilename).name)
    final_save_path = UPLOAD_DIR / f"{filename_ts_str}_{sane_original_filename}"
    
    print(f"🧩 Ensamblando archivo: {final_save_path} desde {totalChunks} chunks (ID: {fileId})")
    try:
        with open(final_save_path, "wb") as final_file:
            for i in range(totalChunks):
                chunk_path = chunk_dir / f"chunk_{i}"
                with open(chunk_path, "rb") as chunk_file:
                    final_file.write(chunk_file.read())
        print(f"✅ Archivo {originalFilename} ensamblado exitosamente en {final_save_path}")
        shutil.rmtree(chunk_dir) # Clean up chunks after successful assembly
        print(f"🧹 Chunks temporales para {fileId} eliminados.")
    except Exception as e:
        print(f"❌ Error ensamblando archivo {originalFilename} (ID: {fileId}): {e}\n{traceback.format_exc()}")
        if chunk_dir.exists(): shutil.rmtree(chunk_dir, ignore_errors=True)
        if final_save_path.exists():
            try: os.remove(final_save_path)
            except OSError: pass
        raise HTTPException(status_code=500, detail=f"Error assembling file: {str(e)}")

    file_ext = Path(originalFilename).suffix.lower()
    is_image = file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    is_video = file_ext in ['.mp4', '.avi', '.mov', '.mkv']

    if is_image:
        try:
            print(f"🖼️  Procesando imagen ensamblada: {final_save_path}")
            # --- NUEVA LÓGICA DE DETECCIÓN UNIFICADA ---
            detection_results = run_detection_on_path(str(final_save_path))
            numero_detectado = detection_results.get('numero_detectado')
            modelo_ladrillo = detection_results.get('modelo_ladrillo')
            confianza_numero = detection_results.get('confianza_numero')
            # --- FIN DE LA NUEVA LÓGICA ---
            
            if not numero_detectado:
                if final_save_path.exists(): os.remove(final_save_path)
                return JSONResponse(
                    content={"message": f"No se detectó vagoneta con número en {originalFilename}", "status": "ignored", "filename": originalFilename},
                    status_code=200
                )

            vagoneta_data = VagonetaCreate(
                numero=str(numero_detectado),
                imagen_path=f"uploads/{final_save_path.name}",
                timestamp=final_timestamp_obj,
                tunel=tunel,
                evento=evento,
                modelo_ladrillo=modelo_ladrillo,
                merma=parse_merma(merma),
                metadata=metadata,
                confianza=float(confianza_numero) if confianza_numero is not None else None,
                origen_deteccion="image_chunk_upload"
            )
            record_id = crud.create_vagoneta_record(vagoneta_data)
            
            db_record_dict = vagoneta_data.dict()
            db_record_dict["_id"] = str(record_id)
            db_record_dict["id"] = str(record_id)
            if isinstance(db_record_dict.get("timestamp"), datetime):
                db_record_dict["timestamp"] = db_record_dict["timestamp"].isoformat()
            broadcast_message = {"type": "new_detection", "data": db_record_dict}
            asyncio.create_task(manager.broadcast_json(broadcast_message))

            response_data = {
                "filename": originalFilename, "status": "ok", "record_id": str(record_id),
                "numero_detectado": numero_detectado, "modelo_ladrillo": modelo_ladrillo,
                "confianza": confianza_numero, "message": f"File {originalFilename} processed and record created successfully."
            }
            return JSONResponse(content=response_data)
        except Exception as e:
            if final_save_path.exists():
                try: os.remove(final_save_path)
                except OSError: pass
            print(f"❌ Error procesando imagen ensamblada {originalFilename}: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Error processing assembled image: {str(e)}")

    elif is_video:
        processing_id = str(uuid.uuid4())
        app.state.pending_video_processing[processing_id] = {
            "video_path": str(final_save_path), # This is the assembled video path
            "original_filename": originalFilename,
            "upload_dir": str(UPLOAD_DIR), # For consistency, though procesar_video_mp4_streamable might not use it
            "tunel": tunel,
            "evento": evento,
            "merma_str": merma,
            "metadata": metadata,
            "timestamp": final_timestamp_obj # Timestamp of when the video processing task was created
        }
        print(f"📹 Video {originalFilename} (ID: {fileId}) ensamblado y listo para procesamiento en segundo plano. Task ID: {processing_id}")
        return JSONResponse(content={
            "status": "video_processing_pending", "processing_id": processing_id,
            "filename": originalFilename,
            "message": "El video está siendo procesado. Conéctese al stream para ver el progreso."
        })
    else:
        if final_save_path.exists():
            try: os.remove(final_save_path)
            except OSError: pass
        raise HTTPException(status_code=400, detail=f"Unsupported file type after assembly: {file_ext} for {originalFilename}")

@app.get("/stream-video-processing/{processing_id}")
async def stream_video_processing(processing_id: str):
    if processing_id not in app.state.pending_video_processing:
        raise HTTPException(status_code=404, detail=f"Video processing ID '{processing_id}' not found or already processed.")

    task_info = app.state.pending_video_processing[processing_id]
    
    async def event_generator():
        final_detection_data = None
        processing_error_occurred = False
        error_message_detail = "Unknown error during video processing."
        db_record_id_created = None # To store the ID of the created record

        try:
            yield f"data: {json.dumps({'type': 'status', 'stage': 'stream_init', 'message': 'Conectado al stream de procesamiento de video.'})}\n\n"
            
            video_path_to_process = task_info["video_path"]
            upload_dir_for_streamer = Path(task_info["upload_dir"])

            async for update in procesar_video_mp4_streamable(video_path_to_process, upload_dir_for_streamer):
                yield f"data: {json.dumps(update)}\n\n"
                if update.get("type") == "final_result":
                    final_detection_data = update.get("data")
                elif update.get("type") == "error": 
                    processing_error_occurred = True
                    error_message_detail = update.get("message", error_message_detail)
            
            if not processing_error_occurred and final_detection_data:
                if isinstance(final_detection_data, dict) and final_detection_data:
                    # Procesar TODAS las detecciones (no solo la mejor)
                    registros_creados = []
                    
                    for numero_str, lista_detecciones in final_detection_data.items():
                        if isinstance(lista_detecciones, list):
                            # Nueva estructura: lista de detecciones por número
                            for deteccion in lista_detecciones:
                                confianza_val = deteccion.get('confianza', 0.0)
                                frame_num = deteccion.get('frame', 0)
                                imagen_path = deteccion.get('imagen_path', f"uploads/{Path(task_info['video_path']).name}")
                                
                                # Validar confianza
                                if confianza_val > 1.0:
                                    print(f"Warning (VID:{processing_id}): Confianza {confianza_val} > 1.0 para N°{numero_str} frame {frame_num}. Capada a 1.0.")
                                    confianza_val = 1.0
                                elif confianza_val < 0.0:
                                    print(f"Warning (VID:{processing_id}): Confianza {confianza_val} < 0.0 para N°{numero_str} frame {frame_num}. Capada a 0.0.")
                                    confianza_val = 0.0

                                # Crear registro individual
                                record_timestamp = task_info.get("timestamp", datetime.now(timezone.utc))
                                if not isinstance(record_timestamp, datetime): 
                                    record_timestamp = datetime.now(timezone.utc)
                                if record_timestamp.tzinfo is None: 
                                    record_timestamp = record_timestamp.replace(tzinfo=timezone.utc)

                                vagoneta_data = VagonetaCreate(
                                    numero=str(numero_str),
                                    imagen_path=imagen_path,
                                    timestamp=record_timestamp,
                                    tunel=task_info.get("tunel"),
                                    evento=task_info.get("evento"),
                                    modelo_ladrillo=None,
                                    merma=parse_merma(task_info.get("merma_str")),                                    metadata={
                                        **(task_info.get("metadata") or {}),
                                        "frame_number": frame_num,
                                        "video_source": Path(task_info['video_path']).name
                                    },
                                    confianza=confianza_val,
                                    origen_deteccion="video_processing"
                                )
                                
                                record_id = crud.create_vagoneta_record(vagoneta_data)
                                registros_creados.append({
                                    "id": str(record_id),
                                    "numero": numero_str,
                                    "confianza": confianza_val,
                                    "frame": frame_num
                                })

                                db_record_dict = vagoneta_data.dict()
                                db_record_dict["_id"] = str(record_id)
                                db_record_dict["id"] = str(record_id)
                                if isinstance(db_record_dict.get("timestamp"), datetime):
                                    db_record_dict["timestamp"] = db_record_dict["timestamp"].isoformat()

                                yield f"data: {json.dumps({'type': 'db_record_created', 'data': db_record_dict})}\n\n"
                                print(f"✅ Registro creado para video {task_info['original_filename']} (Task:{processing_id}), N°: {numero_str}, Frame: {frame_num}, Conf: {confianza_val:.3f}, DB_ID: {record_id}")
                                
                                # Broadcast via WebSocket
                                broadcast_message = {"type": "new_detection", "data": db_record_dict}
                                asyncio.create_task(manager.broadcast_json(broadcast_message))
                        
                        else:
                            # Estructura antigua: compatibilidad hacia atrás
                            confianza_val = float(lista_detecciones) if lista_detecciones else 0.0
                            
                            if confianza_val > 1.0:
                                confianza_val = 1.0
                            elif confianza_val < 0.0:
                                confianza_val = 0.0

                            record_timestamp = task_info.get("timestamp", datetime.now(timezone.utc))
                            if not isinstance(record_timestamp, datetime): 
                                record_timestamp = datetime.now(timezone.utc)
                            if record_timestamp.tzinfo is None: 
                                record_timestamp = record_timestamp.replace(tzinfo=timezone.utc)

                            vagoneta_data = VagonetaCreate(
                                numero=str(numero_str),
                                imagen_path=f"uploads/{Path(task_info['video_path']).name}",
                                timestamp=record_timestamp,
                                tunel=task_info.get("tunel"),
                                evento=task_info.get("evento"),
                                modelo_ladrillo=None,
                                merma=parse_merma(task_info.get("merma_str")),
                                metadata=task_info.get("metadata") or {},
                                confianza=confianza_val,
                                origen_deteccion="video_processing"
                            )
                            
                            record_id = crud.create_vagoneta_record(vagoneta_data)
                            registros_creados.append({
                                "id": str(record_id),
                                "numero": numero_str,
                                "confianza": confianza_val
                            })

                    print(f"📊 Total de {len(registros_creados)} registros creados para video {task_info['original_filename']}")
                    yield f"data: {json.dumps({'type': 'processing_complete', 'total_records': len(registros_creados), 'records': registros_creados})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'status', 'stage': 'completion', 'message': 'Video procesado, pero no se identificó un número de vagoneta claro.'})}\n\n"
                    print(f"ℹ️ Video {task_info['original_filename']} (Task:{processing_id}) procesado. No se identificó un número principal. Detecciones: {final_detection_data}")
                    # processing_error_occurred remains False, but no record is created.
                    
            elif processing_error_occurred:
                yield f"data: {json.dumps({'type': 'error', 'stage': 'finalization', 'message': f'Error final durante el procesamiento: {error_message_detail}'})}\n\n"
                print(f"❌ Error final durante el procesamiento del video {task_info['original_filename']} (Task:{processing_id}): {error_message_detail}")
            
            elif not final_detection_data : # and not processing_error_occurred implicitly
                yield f"data: {json.dumps({'type': 'status', 'stage': 'completion', 'message': 'Video procesado pero no se encontraron detecciones.'})}\n\n"
                print(f"ℹ️ Video {task_info['original_filename']} (Task:{processing_id}) procesado, pero no se encontraron detecciones.")
        
        except Exception as e_stream:
            processing_error_occurred = True # Mark error
            error_message_detail = f'Excepción en el stream principal: {str(e_stream)}'
            yield f"data: {json.dumps({'type': 'error', 'stage': 'stream_exception', 'message': error_message_detail})}\n\n"
            print(f"💥 Excepción en stream_video_processing para {processing_id} ({task_info.get('original_filename', 'N/A')}): {e_stream}\n{traceback.format_exc()}")
        
        finally:
            # Send stream_end event
            final_message = error_message_detail if processing_error_occurred else \
                            f"Proceso completado para {task_info.get('original_filename', 'video')}. " + \
                            (f"Registro DB ID: {db_record_id_created}" if db_record_id_created else "No se creó registro.")
            
            yield f"data: {json.dumps({'type': 'stream_end', 'error_occurred': processing_error_occurred, 'message': final_message, 'processing_id': processing_id})}\n\n"
            print(f"INFO: Stream para {processing_id} ({task_info.get('original_filename', 'N/A')}) finalizando. Error ocurrido: {processing_error_occurred}")
            
            # Clean up pending task
            if processing_id in app.state.pending_video_processing:
                del app.state.pending_video_processing[processing_id]
                print(f"INFO: Tarea {processing_id} eliminada de pendientes.")
            else:
                # This case might happen if cleanup occurs due to an early exit or another mechanism
                print(f"WARN: Tarea {processing_id} ya no estaba en pendientes al finalizar stream (posiblemente ya eliminada o error previo).")

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/historial/", response_model=HistorialResponse)
async def get_historial_registros(
    skip: int = 0, 
    limit: int = 100,
    sort_by: Optional[str] = Query("timestamp", enum=["timestamp", "numero", "confianza", "origen_deteccion"]),
    sort_order: Optional[int] = Query(-1, enum=[-1, 1]),
    filtro: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db = Depends(get_database)
):
    if fecha_fin and fecha_fin.hour == 0 and fecha_fin.minute == 0 and fecha_fin.second == 0:
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59, microsecond=999999)

    registros_from_db, total_registros = crud.get_vagonetas_historial_with_filters(
        db=db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        filtro=filtro,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    registros_list = []
    for r_doc in registros_from_db:
        try:
            doc_data = dict(r_doc)

            if "_id" in doc_data and isinstance(doc_data["_id"], ObjectId):
                doc_data["id"] = str(doc_data["_id"])

            ts = doc_data.get('timestamp')
            if not isinstance(ts, datetime):
                if isinstance(ts, str):
                    try:
                        ts = datetime.fromisoformat(ts)
                    except ValueError:
                        ts = datetime.now(timezone.utc)
                else:
                    ts = datetime.now(timezone.utc)
            
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            doc_data['timestamp'] = ts

            doc_data['numero_detectado'] = str(doc_data.get('numero', 'N/A'))

            try:
                doc_data['confianza'] = float(doc_data.get('confianza', 0.0))
            except (ValueError, TypeError):
                doc_data['confianza'] = 0.0

            doc_data['origen_deteccion'] = str(doc_data.get('origen_deteccion', 'historico'))
            doc_data['evento'] = str(doc_data.get('evento', 'desconocido'))
            doc_data['tunel'] = str(doc_data.get('tunel')) if doc_data.get('tunel') is not None else None
            doc_data['merma'] = str(doc_data.get('merma')) if doc_data.get('merma') is not None else None

            doc_data['imagen_path'] = doc_data.get('imagen_path')
            doc_data['modelo_ladrillo'] = doc_data.get('modelo_ladrillo')
            
            registro_display = RegistroHistorialDisplay(**doc_data)
            registros_list.append(registro_display)
        except Exception as e:
            print(f"Error al procesar el documento: {r_doc}")
            print(f"Error: {e}")

    return HistorialResponse(
        registros=registros_list,
        total=total_registros,
        skip=skip,
        limit=limit,
        has_more=(skip + len(registros_list) < total_registros)
    )

@app.post("/auto-capture/start")
async def start_auto_capture():
    global auto_capture_manager, auto_capture_task, CAMERAS_CONFIG, UPLOAD_DIR, manager
    if auto_capture_manager and auto_capture_manager.is_running():
        raise HTTPException(status_code=400, detail="La captura automática ya está en ejecución.")
    
    print("INFO: Iniciando sistema de captura automática...")
    auto_capture_manager = AutoCaptureManager(CAMERAS_CONFIG, UPLOAD_DIR, manager) 
    auto_capture_task = asyncio.create_task(auto_capture_manager.start_system())
    return {"message": "Sistema de captura automática iniciado."}

@app.post("/auto-capture/stop")
async def stop_auto_capture():
    global auto_capture_manager, auto_capture_task
    if not auto_capture_manager or not auto_capture_manager.is_running():
        raise HTTPException(status_code=400, detail="La captura automática no está en ejecución.")
    
    print("INFO: Deteniendo sistema de captura automática...")
    await auto_capture_manager.stop_system()
    # auto_capture_manager = None # Keep manager instance for potential restart or status check?
    # auto_capture_task = None # Task should be awaited/cancelled in stop_system
    if auto_capture_task and not auto_capture_task.done():
        auto_capture_task.cancel() # Ensure task is cancelled if not done by stop_system
    return {"message": "Sistema de captura automática detenido."}

@app.get("/auto-capture/status")
async def auto_capture_status():
    global auto_capture_manager
    if auto_capture_manager: # Check if manager exists
        return auto_capture_manager.get_status() # get_status should return a dict
    return {"manager_running": False, "cameras": [], "message": "El sistema de captura automática no ha sido inicializado."}

@app.websocket("/ws/detections")
async def websocket_endpoint(websocket: WebSocket):
    print(f"🔌 Nueva conexión WebSocket desde {websocket.client}")
    await manager.connect(websocket)
    try:
        # Enviar mensaje de bienvenida
        welcome_message = {
            "type": "connection_established",
            "message": "Conectado al WebSocket de detecciones",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await manager.send_json_to_connection(welcome_message, websocket)
        print(f"✅ WebSocket conectado: {websocket.client}")
        
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            print(f"📩 Mensaje recibido del cliente: {data}")
            # Echo back para confirmar comunicación
            echo_response = {
                "type": "echo",
                "original_message": data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            await manager.send_json_to_connection(echo_response, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"🔌❌ Cliente {websocket.client} desconectado del WebSocket")
    except Exception as e:
        print(f"❌ Error en WebSocket para {websocket.client}: {e}")
        manager.disconnect(websocket)

# Example model info endpoint (if processor object exists and has details)
# from utils.image_processing import processor # Assuming processor is initialized here or globally
@app.get("/model/info")
async def get_model_info():
    # This depends on how 'processor' is defined and what attributes it has.
    # Placeholder if 'processor' is not readily available or its structure is unknown.
    # if 'processor' in globals() and hasattr(processor, 'get_model_details'):
    #     return processor.get_model_details()
    return {"message": "Información del modelo no disponible en esta configuración."}

# Endpoints para Monitor en Vivo

@app.get("/cameras/list")
async def get_cameras_list():
    """Obtener lista de cámaras disponibles para el monitor en vivo"""
    try:
        cameras_info = []
        for camera in CAMERAS_CONFIG:
            cameras_info.append({
                "camera_id": camera["camera_id"],
                "tunel": camera.get("tunel", "Sin nombre"),
                "evento": camera.get("evento", "desconocido"),
                "source_type": camera.get("source_type", "camera"),
                "demo_mode": camera.get("demo_mode", False)
            })
        return {"cameras": cameras_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo lista de cámaras: {str(e)}")

@app.post("/monitor/start/{camera_id}")
async def start_camera_monitoring(camera_id: str):
    """Iniciar monitoreo en vivo de una cámara específica"""
    global monitor_tasks
    
    # Para la webcam, usar configuración predeterminada
    if camera_id == "webcam":
        camera_config = {
            "camera_id": "webcam",
            "camera_url": 0,
            "source_type": "camera",
            "evento": "ingreso",
            "tunel": "Túnel Principal",
            "motion_sensitivity": 0.3,
            "min_motion_area": 8000,
            "detection_cooldown": 5,
            "demo_mode": False
        }
    else:
        # Buscar en la configuración de cámaras
        camera_config = next((cam for cam in CAMERAS_CONFIG if cam["camera_id"] == camera_id), None)
        
    if not camera_config:
        raise HTTPException(status_code=404, detail=f"Cámara {camera_id} no encontrada")
      # Verificar si ya está en ejecución
    if camera_id in monitor_tasks:
        raise HTTPException(status_code=400, detail=f"El monitoreo de la cámara {camera_id} ya está activo")
    
    # Crear tarea de monitoreo
    task = asyncio.create_task(monitor_camera_live(camera_id, camera_config))
    monitor_tasks[camera_id] = task
    
    print(f"INFO: Monitoreo iniciado para cámara {camera_id}")
    return {
        "status": "started",
        "message": f"Monitoreo iniciado para cámara {camera_id}", 
        "camera_id": camera_id
    }

@app.post("/monitor/stop/{camera_id}")
async def stop_camera_monitoring(camera_id: str):
    """Detener monitoreo en vivo de una cámara específica"""
    global monitor_tasks
    
    if camera_id not in monitor_tasks:
        raise HTTPException(status_code=404, detail=f"No hay monitoreo activo para la cámara {camera_id}")
    
    # Cancelar la tarea
    monitor_tasks[camera_id].cancel()
    del monitor_tasks[camera_id]
    
    print(f"INFO: Monitoreo detenido para cámara {camera_id}")
    return {
        "status": "stopped",
        "message": f"Monitoreo detenido para cámara {camera_id}", 
        "camera_id": camera_id
    }

@app.get("/monitor/status")
async def get_monitor_status():
    """Obtener estado actual del monitoreo"""
    global monitor_tasks
    
    active_monitors = []
    for camera_id, task in monitor_tasks.items():
        if not task.done():
            active_monitors.append({
                "camera_id": camera_id,
                "status": "running"
            })
    
    return {
        "active_monitors": active_monitors,
        "total_active": len(active_monitors)
    }

async def monitor_camera_live(camera_id: str, camera_config: dict):
    """Función para monitorear una cámara en tiempo real"""
    cap = None
    try:
        camera_url = camera_config["camera_url"]
        print(f"🎥 Iniciando monitoreo para cámara {camera_id} (URL: {camera_url})")

        if isinstance(camera_url, (int, str)) and str(camera_url).isdigit():
            cap = cv2.VideoCapture(int(camera_url), cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(str(camera_url))

        if not cap.isOpened():
            raise Exception(f"No se pudo abrir la cámara {camera_id}")

        # Configurar propiedades
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 15)

        # Verificar lectura
        ret, frame = cap.read()
        if not ret or frame is None:
            raise Exception(f"No se pueden leer frames de la cámara {camera_id}")

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = 0
        last_time = time.time()
        fps = 0
        print(f"✅ Cámara conectada (Resolución: {frame_width}x{frame_height})")
        
        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    await asyncio.sleep(0.1)
                    continue
                
                frame_count += 1
                current_time = time.time()
                elapsed = current_time - last_time

                if elapsed >= 1.0:
                    fps = frame_count / elapsed
                    frame_count = 0
                    last_time = current_time
                    await manager.broadcast_json({
                        "type": "debug_info",
                        "data": {
                            "camera_id": camera_id,
                            "fps": round(fps, 1),
                            "resolution": f"{frame_width}x{frame_height}",
                            "timestamp": datetime.now().isoformat()
                        }
                    })

                # Realizar detección en algunos frames (cada 30 frames, aproximadamente 1-2 segundos)
                if frame_count % 30 == 0:
                    # Procesar el frame para detección
                    try:
                        # --- NUEVA LÓGICA DE DETECCIÓN UNIFICADA ---
                        detection_results = run_detection_on_frame(frame)
                        numero_detectado = detection_results.get('numero_detectado')
                        modelo_ladrillo = detection_results.get('modelo_ladrillo')
                        confianza_numero = detection_results.get('confianza_numero')
                        # --- FIN DE LA NUEVA LÓGICA ---
                        
                        if numero_detectado and confianza_numero is not None:
                            if confianza_numero >= 0.5:
                                # Guardar imagen del frame
                                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                                frame_filename = f"detection_frame_{camera_id}_{timestamp_str}.jpg"
                                frame_path = UPLOAD_DIR / frame_filename
                                cv2.imwrite(str(frame_path), frame)
                                
                                # Crear registro en base de datos
                                vagoneta_create_obj = VagonetaCreate(
                                    numero=str(numero_detectado),
                                    imagen_path=f"uploads/{frame_filename}",
                                    timestamp=datetime.now(timezone.utc),
                                    tunel=camera_config.get("tunel"),
                                    evento="deteccion_automatica",
                                    modelo_ladrillo=modelo_ladrillo,
                                    merma=None,
                                    metadata={"camera_id": camera_id, "fps": fps},
                                    confianza=float(confianza_numero),
                                    origen_deteccion="live_camera"
                                )
                                record_id = crud.create_vagoneta_record(vagoneta_create_obj)
                                
                                # Notificar a los clientes WebSocket
                                db_record_dict = vagoneta_create_obj.dict()
                                db_record_dict["_id"] = str(record_id)
                                db_record_dict["id"] = str(record_id)
                                db_record_dict["timestamp"] = db_record_dict["timestamp"].isoformat()
                                
                                await manager.broadcast_json({
                                    "type": "new_detection",
                                    "data": db_record_dict
                                })
                    except Exception as e:
                        print(f"Error en detección de cámara {camera_id}: {e}")                
                # Almacenar frame para streaming
                live_frames[camera_id] = frame
                
                await asyncio.sleep(0.05)  # Control de FPS
                
            except Exception as e:
                print(f"Error en loop de monitoreo para cámara {camera_id}: {e}")
                await asyncio.sleep(1)
                
    except Exception as e:
        print(f"💥 Error crítico en monitor de cámara {camera_id}: {e}")
    finally:
        if cap:
            cap.release()
        print(f"🔌 Liberando recursos de cámara {camera_id}")

# ====================
# INICIALIZACIÓN DEL SERVIDOR
# ====================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor FastAPI...")
    print("📡 Backend disponible en: http://localhost:8000")
    print("📚 Documentación API en: http://localhost:8000/docs")
    print("🔌 WebSocket en: ws://localhost:8000/ws/detections")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # No reload para producción
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        import traceback
        traceback.print_exc()

import cv2
from ultralytics import YOLO
from pathlib import Path

# Cargar el modelo YOLOv8 (debe estar entrenado para vagonetas y placas numeradas)
# Cambia el path al modelo según corresponda
yolo_model_path = Path("models/yolov8_vagonetas.pt")
model = YOLO(str(yolo_model_path))

def detectar_vagoneta_y_placa(image_path):
    """
    Procesa la imagen y retorna la región de la placa numerada y la predicción de la vagoneta.
    Retorna: (cropped_placa_img, bbox_vagoneta, bbox_placa, numero_detectado)
    Si no se detecta placa, numero_detectado será None.
    """
    img = cv2.imread(str(image_path))
    results = model(img)
    bbox_vagoneta = None
    bbox_placa = None
    numero_detectado = None
    for r in results[0].boxes:
        if int(r.cls[0]) == 0:
            bbox_vagoneta = r.xyxy[0].cpu().numpy().astype(int)
        elif int(r.cls[0]) == 1:
            bbox_placa = r.xyxy[0].cpu().numpy().astype(int)
    cropped_placa_img = None
    if bbox_placa is not None:
        x1, y1, x2, y2 = bbox_placa
        cropped_placa_img = img[y1:y2, x1:x2]
        # Intentar OCR solo si hay placa
        from .ocr import ocr_placa_img
        numero_detectado = ocr_placa_img(cropped_placa_img)
    return cropped_placa_img, bbox_vagoneta, bbox_placa, numero_detectado

# Suponiendo que tienes un modelo YOLOv8 entrenado para detectar modelos de ladrillo
modelo_ladrillo_model_path = Path("models/yolov8_modelo_ladrillo.pt")
modelo_ladrillo_model = None
if modelo_ladrillo_model_path.exists():
    modelo_ladrillo_model = YOLO(str(modelo_ladrillo_model_path))

def detectar_modelo_ladrillo(image_path):
    """
    Detecta el modelo de ladrillo en la imagen usando un modelo YOLOv8 entrenado para eso.
    Retorna el nombre/clase del modelo detectado o None si no se detecta.
    """
    if modelo_ladrillo_model is None:
        return None
    img = cv2.imread(str(image_path))
    results = modelo_ladrillo_model(img)
    # Suponiendo que la clase 0, 1, 2... corresponden a diferentes modelos
    if len(results[0].boxes) > 0:
        # Tomar la clase con mayor confianza
        best = max(results[0].boxes, key=lambda b: b.conf[0])
        clase = int(best.cls[0])
        # Aquí deberías mapear la clase a un nombre de modelo
        modelos = {0: "Hueco", 1: "Macizo", 2: "Otro"}
        return modelos.get(clase, f"Modelo_{clase}")
    return None

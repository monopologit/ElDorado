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

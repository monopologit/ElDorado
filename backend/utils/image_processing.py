import cv2
import numpy as np
from ultralytics import YOLO
from .ocr import extract_number_from_image
from typing import Dict, Optional, Any, Tuple

class ImageProcessor:
    def __init__(self, model_path: str = "models/yolov8_vagonetas.pt"):
        """Inicializa el procesador de imágenes con YOLOv8"""
        self.model = YOLO(model_path)
        self.last_detection = None
        self.min_confidence = 0.5

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocesa la imagen para mejorar la detección"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Mejorar contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        # Volver a BGR para YOLO
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    def detect_objects(self, image: np.ndarray) -> Dict[str, Any]:
        """Detecta vagoneta, placa y modelo de ladrillo en la imagen"""
        # Preprocesar imagen
        processed_image = self.preprocess_image(image)
        
        # Realizar detección con YOLOv8
        results = self.model(processed_image)[0]
        detections = {
            'vagoneta': None,
            'placa': None,
            'ladrillo': None
        }

        # Procesar resultados
        for box in results.boxes:
            confidence = float(box.conf[0])
            if confidence < self.min_confidence:
                continue

            class_id = int(box.cls[0])
            class_name = results.names[class_id]
            bbox = box.xyxy[0].cpu().numpy()

            if class_name == 'vagoneta':
                detections['vagoneta'] = bbox
            elif class_name == 'placa':
                detections['placa'] = bbox
            elif 'ladrillo' in class_name:
                detections['ladrillo'] = {
                    'bbox': bbox,
                    'tipo': class_name
                }

        return detections

    def process_frame(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """Procesa un frame y retorna la información detectada"""
        # Detectar objetos
        detections = self.detect_objects(frame)
        
        if not detections['placa']:
            return None

        # Extraer y procesar número de placa
        placa_bbox = detections['placa']
        placa_image = frame[
            int(placa_bbox[1]):int(placa_bbox[3]),
            int(placa_bbox[0]):int(placa_bbox[2])
        ]
        numero = extract_number_from_image(placa_image)

        if not numero:
            return None

        # Preparar resultado
        result = {
            'numero': numero,
            'confidence': float(detections['placa'][4]) if len(detections['placa']) > 4 else 0.0,
            'bbox': detections['placa'].tolist(),
        }

        # Agregar información del modelo de ladrillo si se detectó
        if detections['ladrillo']:
            result['modelo_ladrillo'] = detections['ladrillo']['tipo']

        self.last_detection = result
        return result

    def get_last_detection(self) -> Optional[Dict[str, Any]]:
        """Retorna la última detección exitosa"""
        return self.last_detection

# Inicializar el procesador como singleton
processor = ImageProcessor()

def process_image(image: np.ndarray) -> Optional[Dict[str, Any]]:
    """Función auxiliar para procesar una imagen"""
    return processor.process_frame(image)

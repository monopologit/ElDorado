import cv2
import pytesseract
import numpy as np
from typing import Optional

def ocr_placa_img(placa_img: np.ndarray) -> Optional[str]:
    """
    Recibe una imagen (numpy array) de la placa y retorna el texto detectado (número de vagoneta).
    """
    if placa_img is None:
        return None
    # Preprocesamiento básico para mejorar OCR
    gray = cv2.cvtColor(placa_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Puedes ajustar el preprocesamiento según tus imágenes
    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    texto = pytesseract.image_to_string(thresh, config=config)
    # Limpiar el resultado
    texto = ''.join(filter(str.isdigit, texto))
    return texto if texto else None

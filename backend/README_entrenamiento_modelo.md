# Guía paso a paso para entrenar tu modelo YOLOv8 para vagonetas y ladrillos

## 1. Requisitos previos

- Python 3.9+
- pip
- Git
- MongoDB instalado y corriendo (puede ser local)
- El backend y frontend de este proyecto ya instalados y funcionando

## 2. Instala Ultralytics YOLOv8 y dependencias para entrenamiento

Abre una terminal y ejecuta:

```powershell
pip install ultralytics opencv-python
```

## 3. Prepara tus datos (imágenes y etiquetas)

### ¿Qué imágenes necesitas?
- Fotos o capturas de video donde se vean claramente:
  - La vagoneta
  - Los ladrillos cargados
  - La chapa/placa con el número de la vagoneta
- **Sí, lo ideal es tener videos o muchas fotos de vagonetas reales con ladrillos y su chapa visible.**
- Puedes extraer frames de videos usando herramientas como VLC, ffmpeg o Python/OpenCV.

### ¿Cómo etiquetar?
1. Usa una herramienta como [Roboflow](https://roboflow.com/), [LabelImg](https://github.com/tzutalin/labelImg) o [makesense.ai](https://makesense.ai/).
2. Marca en cada imagen:
   - Un bounding box para la vagoneta (clase: `vagoneta`)
   - Un bounding box para la placa/número (clase: `placa`)
   - Un bounding box para el ladrillo o el "modelo de ladrillo" (puedes usar varias clases si tienes distintos modelos)
3. Exporta las anotaciones en formato YOLO (cada imagen tendrá un `.txt` con las etiquetas).

### Estructura de carpetas recomendada
```
datasets/
  ladrillos/
    images/
      train/
      val/
    labels/
      train/
      val/
    data.yaml
```

- Pon imágenes de entrenamiento en `images/train/` y de validación en `images/val/`.
- Los archivos `.txt` de etiquetas van en `labels/train/` y `labels/val/`.

### Ejemplo de archivo `data.yaml`
```yaml
train: datasets/ladrillos/images/train
val: datasets/ladrillos/images/val

nc: 3
names: ['vagoneta', 'placa', 'ladrillo_tipo_X']
```
Ajusta `nc` y `names` según tus clases reales.

## 4. Entrena el modelo

En la terminal, ejecuta:

```powershell
yolo detect train data=datasets/ladrillos/data.yaml model=yolov8n.pt epochs=100 imgsz=640
```
- Puedes usar `yolov8n.pt` (más rápido, menos preciso) o `yolov8s.pt`, etc.
- Cambia `epochs` según la cantidad de datos.

Al finalizar, el modelo entrenado estará en:
```
runs/detect/train/weights/best.pt
```

## 5. Usa el modelo entrenado en tu backend

1. Copia el archivo `best.pt` a la carpeta `backend/models/` y renómbralo si quieres (ej: `yolov8_vagonetas.pt`).
2. Asegúrate de que el backend apunte a ese archivo en el código.

## 6. ¿Cómo funciona la detección?
- El modelo detecta la posición y clase de cada objeto en la imagen.
- Para la placa, recorta la región y pásala a OCR para leer el número.
- Para el ladrillo, toma la clase detectada y guárdala como `modelo_ladrillo`.

## 7. ¿Necesito videos o fotos?
- **Sí, necesitas imágenes o frames de video donde se vean claramente la vagoneta, los ladrillos y la chapa de identificación.**
- Cuantas más imágenes y variedad (distintas condiciones de luz, ángulos, etc.), mejor será el modelo.

## 8. ¿Y el frontend y la base de datos?
- El frontend ya está listo para enviar imágenes al backend.
- La base de datos MongoDB se configura automáticamente al iniciar el backend (ver README principal).

## 9. Resumen rápido
1. Instala ultralytics y dependencias.
2. Consigue imágenes/videos de vagonetas reales con ladrillos y chapa visible.
3. Etiqueta las imágenes (vagoneta, placa, ladrillo/modelo).
4. Organiza carpetas y crea `data.yaml`.
5. Entrena con `yolo detect train ...`.
6. Copia el modelo entrenado al backend.
7. ¡Listo! El sistema reconocerá automáticamente vagoneta, número y modelo de ladrillo.

---

¿Dudas? Puedes buscar ejemplos de datasets YOLO en Google o pedirme ayuda para un paso específico.

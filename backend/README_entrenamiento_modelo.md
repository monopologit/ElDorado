# Guía  simple para entrenar el modelo YOLOv8 (vagonetas y bloques)

## 1. Antes de empezar
- Instala Python 3.9+, pip y Git.
- Instala MongoDB y asegúrate de que funcione.
- Ten este proyecto (backend y frontend) ya instalado.

## 2. Instalar lo necesario para entrenar
Abre una terminal y ejecuta:
```powershell
pip install ultralytics opencv-python
```

## 3. Conseguir imágenes
- Saca fotos o graba videos donde se vea:
  - La vagoneta
  - Los ladrillos
  - La chapa/número de la vagoneta
- Lo ideal: muchas imágenes/videos reales.
- Se puede extraer imágenes de videos con VLC, ffmpeg o Python/OpenCV.

## 4. Etiqueta las imágenes
- Usa [Roboflow](https://roboflow.com/), [LabelImg](https://github.com/tzutalin/labelImg) o [makesense.ai](https://makesense.ai/).
- Dibuja cajas para:
  - vagoneta
  - placa
  - ladrillo/modelo
- Exporta en formato YOLO (cada imagen tendrá un `.txt`).

## 5. Se puede Organizar las carpetas así
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

## 6. Ejemplo de data.yaml
```yaml
train: datasets/ladrillos/images/train
val: datasets/ladrillos/images/val
nc: 3
names: ['vagoneta', 'placa', 'ladrillo_tipo_X']
```

## 7. Entrenar el modelo
En la terminal:
```powershell
yolo detect train data=datasets/ladrillos/data.yaml model=yolov8n.pt epochs=100 imgsz=640
```
- El modelo entrenado estará en:
```
runs/detect/train/weights/best.pt
```

## 8. Usar el modelo entrenado
- Copia `best.pt` a `backend/models/` (se puede renombrar).
- El backend ya está listo para usarlo.

## 9. ¿Capturas manuales?
- **NO son necesarias.** El sistema funciona automático con cámaras físicas. La carga manual es solo para pruebas.


from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import json
from typing import Optional, Dict, Any

router = APIRouter(prefix="/visualization", tags=["Visualización"])

def draw_detection_boxes(image_np: np.ndarray, analysis: Dict[str, Any]) -> np.ndarray:
    """
    Dibuja recuadros de detección en la imagen
    """
    height, width = image_np.shape[:2]
    result_image = image_np.copy()
    
    # Colores para diferentes tipos de detección
    colors = {
        'clothing': (0, 255, 0),      # Verde para vestimenta
        'color': (0, 165, 255),       # Naranja para color
        'accessory': (255, 0, 255),   # Magenta para accesorios
        'face': (255, 0, 0)          # Rojo para cara
    }
    
    # Dibujar recuadro de vestimenta superior
    if analysis.get('clothing_item') and analysis.get('clothing_item') != 'desconocido':
        # Simular posición de la vestimenta (parte superior del cuerpo)
        x1, y1 = int(width * 0.2), int(height * 0.2)
        x2, y2 = int(width * 0.8), int(height * 0.6)
        
        cv2.rectangle(result_image, (x1, y1), (x2, y2), colors['clothing'], 3)
        
        # Etiqueta de vestimenta
        label = f"👕 {analysis.get('clothing_item', 'Prenda')}"
        confidence = analysis.get('detection_confidence', 0)
        label_text = f"{label} ({confidence:.0%})"
        
        # Fondo para el texto
        (text_width, text_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(result_image, (x1, y1-30), (x1+text_width+10, y1), colors['clothing'], -1)
        cv2.putText(result_image, label_text, (x1+5, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Dibujar recuadro de color detectado
    if analysis.get('primary_color') and analysis.get('primary_color') != 'desconocido':
        # Posición para el análisis de color (área central)
        x1, y1 = int(width * 0.3), int(height * 0.3)
        x2, y2 = int(width * 0.7), int(height * 0.7)
        
        cv2.rectangle(result_image, (x1, y1), (x2, y2), colors['color'], 3)
        
        # Etiqueta de color
        color_label = f"🎨 {analysis.get('primary_color', 'Color')}"
        if analysis.get('secondary_color'):
            color_label += f" + {analysis.get('secondary_color')}"
        
        # Fondo para el texto
        (text_width, text_height), _ = cv2.getTextSize(color_label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(result_image, (x1, y2+5), (x1+text_width+10, y2+35), colors['color'], -1)
        cv2.putText(result_image, color_label, (x1+5, y2+25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Dibujar recuadro de accesorio
    if analysis.get('head_accessory') and analysis.get('head_accessory') != 'desconocido':
        # Posición para accesorios de cabeza
        x1, y1 = int(width * 0.4), int(height * 0.1)
        x2, y2 = int(width * 0.6), int(height * 0.3)
        
        cv2.rectangle(result_image, (x1, y1), (x2, y2), colors['accessory'], 3)
        
        # Etiqueta de accesorio
        accessory_label = f"👓 {analysis.get('head_accessory', 'Accesorio')}"
        confidence = analysis.get('accessory_confidence', 0)
        accessory_text = f"{accessory_label} ({confidence:.0%})"
        
        # Fondo para el texto
        (text_width, text_height), _ = cv2.getTextSize(accessory_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(result_image, (x1, y1-25), (x1+text_width+10, y1), colors['accessory'], -1)
        cv2.putText(result_image, accessory_text, (x1+5, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Dibujar recuadro de cara
    if analysis.get('person_detected'):
        # Posición para la cara
        x1, y1 = int(width * 0.35), int(height * 0.15)
        x2, y2 = int(width * 0.65), int(height * 0.4)
        
        cv2.rectangle(result_image, (x1, y1), (x2, y2), colors['face'], 3)
        
        # Etiqueta de cara
        face_label = f"👤 Cara detectada"
        age = analysis.get('age_range', '')
        if age:
            face_label += f" ({age})"
        
        # Fondo para el texto
        (text_width, text_height), _ = cv2.getTextSize(face_label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(result_image, (x1, y1-25), (x1+text_width+10, y1), colors['face'], -1)
        cv2.putText(result_image, face_label, (x1+5, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return result_image

@router.post("/analyze-image")
async def analyze_image_with_visualization(
    image_data: str = Query(..., description="Imagen en base64"),
    analysis_data: str = Query(..., description="Datos de análisis en JSON")
):
    """
    Analiza una imagen y devuelve la imagen con las detecciones marcadas
    """
    try:
        # Decodificar imagen
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_np is None:
            raise HTTPException(status_code=400, detail="No se pudo decodificar la imagen")
        
        # Parsear datos de análisis
        analysis = json.loads(analysis_data)
        
        # Dibujar recuadros de detección
        result_image = draw_detection_boxes(image_np, analysis)
        
        # Codificar imagen resultante
        _, buffer = cv2.imencode('.jpg', result_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        result_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "annotated_image": result_base64,
            "analysis": analysis,
            "detections": {
                "clothing_detected": analysis.get('clothing_item') != 'desconocido',
                "color_detected": analysis.get('primary_color') != 'desconocido',
                "accessory_detected": analysis.get('head_accessory') != 'desconocido',
                "face_detected": analysis.get('person_detected', False)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando imagen: {str(e)}")

@router.get("/detection-info")
async def get_detection_info():
    """
    Devuelve información sobre los tipos de detección disponibles
    """
    return {
        "detection_types": {
            "clothing": {
                "name": "Vestimenta Superior",
                "color": "green",
                "description": "Detecta prendas como camisetas, chaquetas, etc."
            },
            "color": {
                "name": "Análisis de Color",
                "color": "orange", 
                "description": "Identifica colores principales y secundarios"
            },
            "accessory": {
                "name": "Accesorios",
                "color": "magenta",
                "description": "Detecta gorros, gafas, etc."
            },
            "face": {
                "name": "Análisis Facial",
                "color": "red",
                "description": "Detecta cara y estima edad"
            }
        },
        "colors": {
            "clothing": [0, 255, 0],      # Verde
            "color": [0, 165, 255],       # Naranja
            "accessory": [255, 0, 255],   # Magenta
            "face": [255, 0, 0]          # Rojo
        }
    }




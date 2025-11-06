import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import base64
from collections import Counter
from sklearn.cluster import KMeans
from typing import Dict, Any, Optional

# Inicializar MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyze_real_clothing(image_np: np.ndarray) -> dict:
    """
    Análisis REAL de prendas usando MediaPipe y OpenCV.
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "person_detected": False,
        "face_detected": False,
        "pose_detected": False,
        "age_range": "desconocido",
        "clothing_style": "casual",
        "primary_color": "desconocido",
        "secondary_color": None,
        "clothing_item": "desconocido",
        "detection_confidence": 0.0,
        "details": {}
    }

    # Convertir la imagen a RGB para MediaPipe
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    height, width, _ = image_np.shape

    # Detección facial para estimar edad
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        face_results = face_detection.process(image_rgb)
        if face_results.detections:
            results["person_detected"] = True
            results["face_detected"] = True
            results["detection_confidence"] = max([detection.score for detection in face_results.detections])
            
            # Estimación básica de edad basada en características faciales
            for detection in face_results.detections:
                bbox = detection.location_data.relative_bounding_box
                face_width = bbox.width
                face_height = bbox.height
                
                # Heurística simple para estimar edad basada en proporciones faciales
                if face_width > 0.15 and face_height > 0.15:  # Cara grande = adulto
                    results["age_range"] = "36-45"
                elif face_width > 0.12 and face_height > 0.12:  # Cara mediana = adulto joven
                    results["age_range"] = "26-35"
                else:  # Cara pequeña = joven
                    results["age_range"] = "18-25"
            
            results["details"]["face_detections"] = len(face_results.detections)

    # Detección de pose para identificar tipo de prenda
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        pose_results = pose.process(image_rgb)
        if pose_results.pose_landmarks:
            results["person_detected"] = True
            results["pose_detected"] = True
            
            # Analizar landmarks para determinar tipo de prenda
            landmarks = pose_results.pose_landmarks.landmark
            
            # Detectar tipo de prenda usando múltiples características
            left_shoulder = landmarks[11]  # LEFT_SHOULDER
            right_shoulder = landmarks[12]  # RIGHT_SHOULDER
            left_hip = landmarks[23]  # LEFT_HIP
            right_hip = landmarks[24]  # RIGHT_HIP
            left_elbow = landmarks[13]  # LEFT_ELBOW
            
            # Calcular múltiples métricas para mejor precisión
            shoulder_distance = abs(left_shoulder.x - right_shoulder.x)
            hip_distance = abs(left_hip.x - right_hip.x)
            torso_length = abs((left_shoulder.y + right_shoulder.y) / 2 - (left_hip.y + right_hip.y) / 2)
            arm_coverage = abs(left_elbow.y - left_shoulder.y)
            
            # Análisis multi-criterio para identificar prenda
            # Chaqueta: hombros MUY anchos + torso MUY largo + brazos MUY cubiertos
            if shoulder_distance > 0.25 and torso_length > 0.4 and arm_coverage > 0.22:
                results["clothing_item"] = "chaqueta"
                results["clothing_style"] = "formal"
            # Sudadera: hombros anchos + brazos cubiertos
            elif shoulder_distance > 0.20 and arm_coverage > 0.16:
                results["clothing_item"] = "sudadera"
                results["clothing_style"] = "deportivo"
            # Camiseta manga larga: brazos cubiertos
            elif arm_coverage > 0.15:
                results["clothing_item"] = "camiseta_manga_larga"
                results["clothing_style"] = "casual"
            # Camiseta normal (default) - incluye camisetas deportivas
            else:
                results["clothing_item"] = "camiseta"
                results["clothing_style"] = "casual"
            
            results["details"]["pose_landmarks_count"] = len(landmarks)

    # Análisis de colores dominantes usando K-means
    try:
        # Redimensionar imagen para análisis más rápido
        small_image = cv2.resize(image_np, (150, 150))
        pixels = small_image.reshape(-1, 3)
        
        # Aplicar K-means para encontrar colores dominantes
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Obtener colores dominantes
        colors = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_
        
        # Contar frecuencia de cada color
        label_counts = Counter(labels)
        
        # Convertir colores BGR a nombres
        color_names = []
        for color in colors:
            b, g, r = color
            color_name = get_color_name(r, g, b)
            color_names.append(color_name)
        
        # Asignar colores principales
        if len(color_names) > 0:
            results["primary_color"] = color_names[0]
        if len(color_names) > 1:
            results["secondary_color"] = color_names[1]
        
        results["details"]["dominant_colors"] = color_names
        results["details"]["color_counts"] = dict(label_counts)
        
    except Exception as e:
        print(f"Error en análisis de colores: {e}")
        results["primary_color"] = "desconocido"

    return results

def get_color_name(r: int, g: int, b: int) -> str:
    """
    Convierte valores RGB a nombres de colores aproximados.
    """
    # Definir rangos de colores expandidos
    color_ranges = {
        "rojo": [(150, 0, 0), (255, 100, 100)],
        "rojo oscuro": [(100, 0, 0), (150, 50, 50)],
        "rojo claro": [(255, 100, 100), (255, 200, 200)],
        "azul": [(0, 0, 150), (100, 100, 255)],
        "azul marino": [(0, 0, 100), (50, 50, 150)],
        "azul cielo": [(150, 200, 255), (200, 220, 255)],
        "verde": [(0, 150, 0), (100, 255, 100)],
        "verde oscuro": [(0, 100, 0), (50, 150, 50)],
        "verde lima": [(150, 255, 0), (200, 255, 100)],
        "amarillo": [(200, 200, 0), (255, 255, 100)],
        "amarillo dorado": [(200, 180, 0), (255, 220, 50)],
        "naranja": [(255, 150, 0), (255, 200, 100)],
        "naranja oscuro": [(200, 100, 0), (255, 150, 50)],
        "negro": [(0, 0, 0), (30, 30, 30)],
        "gris oscuro": [(30, 30, 30), (80, 80, 80)],
        "gris": [(80, 80, 80), (150, 150, 150)],
        "blanco": [(150, 150, 150), (200, 200, 200)],
        "marron": [(100, 50, 0), (200, 150, 100)],
        "marron claro": [(150, 100, 50), (200, 150, 100)],
        "marron oscuro": [(50, 25, 0), (100, 75, 50)],
        "rosa": [(200, 100, 150), (255, 150, 200)],
        "rosa claro": [(255, 150, 200), (255, 200, 220)],
        "rosa oscuro": [(150, 50, 100), (200, 100, 150)],
        "morado": [(100, 0, 200), (200, 100, 255)],
        "morado oscuro": [(50, 0, 100), (100, 50, 200)],
        "morado claro": [(200, 100, 255), (220, 150, 255)],
        "turquesa": [(0, 200, 200), (100, 255, 255)],
        "coral": [(255, 100, 100), (255, 150, 150)],
        "salmon": [(255, 150, 120), (255, 180, 150)],
        "beige": [(200, 180, 150), (255, 220, 180)],
        "crema": [(240, 230, 200), (255, 250, 220)],
        "violeta": [(150, 50, 200), (200, 100, 255)],
        "indigo": [(50, 0, 150), (100, 50, 200)],
        "magenta": [(200, 0, 200), (255, 100, 255)],
        "cian": [(0, 200, 200), (100, 255, 255)],
        "oliva": [(100, 100, 0), (150, 150, 50)],
        "caqui": [(150, 150, 100), (200, 200, 150)],
        "granate": [(100, 0, 50), (150, 50, 100)],
        "burdeos": [(100, 0, 0), (150, 50, 50)],
        "oro": [(200, 180, 0), (255, 220, 50)],
        "plata": [(180, 180, 200), (220, 220, 240)]
    }
    
    # Priorizar blanco si los valores RGB son altos
    if r >= 220 and g >= 220 and b >= 220:
        return "blanco"
    
    # Priorizar negro si los valores RGB son muy bajos
    if r <= 30 and g <= 30 and b <= 30:
        return "negro"
    
    for color_name, (min_rgb, max_rgb) in color_ranges.items():
        if (min_rgb[0] <= r <= max_rgb[0] and 
            min_rgb[1] <= g <= max_rgb[1] and 
            min_rgb[2] <= b <= max_rgb[2]):
            return color_name
    
    return "desconocido"

def draw_detections_on_image(image: np.ndarray, analysis: dict, pose_landmarks=None) -> np.ndarray:
    """
    Dibuja las detecciones sobre la imagen original usando posiciones DINÁMICAS.
    
    Args:
        image: Imagen original en formato numpy
        analysis: Resultados del análisis
        pose_landmarks: Landmarks de MediaPipe para posiciones dinámicas
    
    Returns:
        Imagen anotada con las detecciones visuales
    """
    annotated = image.copy()
    height, width = annotated.shape[:2]
    
    # Colores para diferentes tipos de detección
    COLOR_FACE = (0, 255, 0)  # Verde para cara
    COLOR_CLOTHING = (255, 165, 0)  # Naranja para ropa
    COLOR_ACCESSORY = (255, 0, 255)  # Magenta para accesorios
    COLOR_TEXT_BG = (0, 0, 0)  # Fondo negro para texto
    COLOR_TEXT = (255, 255, 255)  # Texto blanco
    
    # Dibujar si se detectó persona
    if analysis.get('person_detected', False):
        # RECUADRO DE CARA/PERSONA DINÁMICO
        if pose_landmarks:
            # Usar landmarks para posicionar dinámicamente
            nose = pose_landmarks.landmark[0]
            left_eye = pose_landmarks.landmark[2]
            right_eye = pose_landmarks.landmark[5]
            left_ear = pose_landmarks.landmark[7]
            right_ear = pose_landmarks.landmark[8]
            left_shoulder = pose_landmarks.landmark[11]
            right_shoulder = pose_landmarks.landmark[12]
            
            # Calcular bounding box de la cara
            face_center_x = int((left_ear.x + right_ear.x) / 2 * width)
            face_center_y = int((nose.y + left_eye.y) / 2 * height)
            face_width = abs(left_ear.x - right_ear.x) * width
            
            # Recuadro de cara con margen
            margin_face = face_width * 0.5
            face_x1 = max(0, int(face_center_x - face_width/2 - margin_face))
            face_y1 = max(0, int(face_center_y - face_width * 0.8))
            face_x2 = min(width, int(face_center_x + face_width/2 + margin_face))
            face_y2 = min(height, int(face_center_y + face_width * 0.6))
        else:
            # Fallback a posición estática
            face_x1 = int(width * 0.15)
            face_y1 = int(height * 0.05)
            face_x2 = int(width * 0.85)
            face_y2 = int(height * 0.5)
        
        cv2.rectangle(annotated, (face_x1, face_y1), (face_x2, face_y2), COLOR_FACE, 3)
        
        # Etiqueta de edad EN POSICIÓN FIJA (esquina superior izquierda)
        age_text = f"Edad: {analysis.get('age_range', 'N/A')}"
        confidence = analysis.get('detection_confidence', 0)
        conf_text = f"Conf: {int(confidence * 100)}%"
        
        # POSICIÓN FIJA en esquina superior izquierda para evitar superposición
        person_label_x = 10
        person_label_y = 10
        person_label_width = 280
        person_label_height = 70
        
        cv2.rectangle(annotated, (person_label_x, person_label_y), 
                     (person_label_x + person_label_width, person_label_y + person_label_height), 
                     COLOR_TEXT_BG, -1)
        cv2.putText(annotated, "PERSONA DETECTADA", (person_label_x + 5, person_label_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_TEXT, 2)
        cv2.putText(annotated, age_text, (person_label_x + 5, person_label_y + 45), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        cv2.putText(annotated, conf_text, (person_label_x + 5, person_label_y + 62), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        
        # RECUADRO DE ROPA DINÁMICO (AMPLIADO para captar toda la vestimenta)
        if pose_landmarks:
            # Usar landmarks para el torso COMPLETO + brazos
            left_shoulder = pose_landmarks.landmark[11]
            right_shoulder = pose_landmarks.landmark[12]
            left_hip = pose_landmarks.landmark[23]
            right_hip = pose_landmarks.landmark[24]
            left_elbow = pose_landmarks.landmark[13]
            right_elbow = pose_landmarks.landmark[14]
            left_wrist = pose_landmarks.landmark[15]
            right_wrist = pose_landmarks.landmark[16]
            left_knee = pose_landmarks.landmark[25]  # Rodilla izquierda (para pantalones)
            right_knee = pose_landmarks.landmark[26]  # Rodilla derecha
            
            # Calcular bounding box AMPLIO que incluya:
            # - Todo el torso (hombros a caderas)
            # - Brazos completos (hasta muñecas)
            # - Parte superior de piernas (hasta rodillas)
            
            # Encontrar los puntos extremos en X (más a izquierda y derecha)
            min_x = min(left_shoulder.x, left_hip.x, left_elbow.x, left_wrist.x)
            max_x = max(right_shoulder.x, right_hip.x, right_elbow.x, right_wrist.x)
            
            # Encontrar los puntos extremos en Y (más arriba y abajo)
            min_y = min(left_shoulder.y, right_shoulder.y)
            max_y = max(left_hip.y, right_hip.y, left_knee.y, right_knee.y)
            
            # Agregar MÁRGENES GENEROSOS (25% horizontal, 10% vertical)
            horizontal_margin = (max_x - min_x) * 0.25
            vertical_margin_top = 0.08  # 8% arriba (cuello)
            vertical_margin_bottom = 0.15  # 15% abajo (más piernas)
            
            clothing_x1 = max(0, int((min_x - horizontal_margin) * width))
            clothing_y1 = max(0, int((min_y - vertical_margin_top) * height))
            clothing_x2 = min(width, int((max_x + horizontal_margin) * width))
            clothing_y2 = min(height, int((max_y + vertical_margin_bottom) * height))
        else:
            # Fallback a posición estática AMPLIA
            clothing_x1 = int(width * 0.05)  # Más ancho
            clothing_y1 = int(height * 0.2)   # Más arriba
            clothing_x2 = int(width * 0.95)   # Más ancho
            clothing_y2 = int(height * 0.85)  # Más abajo
        
        cv2.rectangle(annotated, (clothing_x1, clothing_y1), (clothing_x2, clothing_y2), COLOR_CLOTHING, 3)
        
        # Etiqueta de ropa
        clothing_item = analysis.get('clothing_item', 'desconocido')
        clothing_style = analysis.get('clothing_style', 'casual')
        color_principal = analysis.get('primary_color', 'desconocido')
        
        # Fondo para texto (ajustado a posición dinámica)
        label_y_cloth = max(85, clothing_y1)
        cv2.rectangle(annotated, (clothing_x1, label_y_cloth - 85), (clothing_x1 + 300, label_y_cloth), COLOR_TEXT_BG, -1)
        cv2.putText(annotated, "VESTIMENTA", (clothing_x1 + 5, label_y_cloth - 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)
        cv2.putText(annotated, f"Prenda: {clothing_item}", (clothing_x1 + 5, label_y_cloth - 45), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        cv2.putText(annotated, f"Estilo: {clothing_style}", (clothing_x1 + 5, label_y_cloth - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        cv2.putText(annotated, f"Color: {color_principal}", (clothing_x1 + 5, label_y_cloth - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        
        # Recuadro de accesorios si se detectaron (DINÁMICO basado en landmarks)
        head_accessory = analysis.get('head_accessory')
        if head_accessory and head_accessory != 'desconocido' and head_accessory is not None:
            # Usar landmarks dinámicos si están disponibles
            if pose_landmarks:
                # Obtener posiciones de nariz, orejas y ojos (puntos de referencia para cabeza)
                nose = pose_landmarks.landmark[0]  # Nariz
                left_eye = pose_landmarks.landmark[2]  # Ojo izquierdo
                right_eye = pose_landmarks.landmark[5]  # Ojo derecho
                left_ear = pose_landmarks.landmark[7]  # Oreja izquierda
                right_ear = pose_landmarks.landmark[8]  # Oreja derecha
                
                # Calcular centro de la cabeza
                center_x = int((left_ear.x + right_ear.x) / 2 * width)
                center_y = int((nose.y + left_eye.y) / 2 * height)
                
                # Calcular ancho de la cabeza basado en distancia entre orejas
                head_width = abs(left_ear.x - right_ear.x) * width
                
                # Expandir el recuadro para cubrir accesorios (gorro/gafas)
                margin = head_width * 0.4  # 40% de margen extra
                acc_x1 = max(0, int(center_x - head_width/2 - margin))
                acc_y1 = max(0, int(center_y - head_width * 0.7))  # Arriba de la cara
                acc_x2 = min(width, int(center_x + head_width/2 + margin))
                acc_y2 = min(height, int(center_y + head_width * 0.3))  # Hasta la barbilla
            else:
                # Fallback a posiciones estáticas si no hay landmarks
                acc_x1 = int(width * 0.2)
                acc_y1 = int(height * 0.02)
                acc_x2 = int(width * 0.8)
                acc_y2 = int(height * 0.35)
            
            cv2.rectangle(annotated, (acc_x1, acc_y1), (acc_x2, acc_y2), COLOR_ACCESSORY, 4)
            
            # Etiqueta de accesorios (más prominente)
            label_height = 50
            label_width = 350
            label_x = max(0, min(acc_x1, width - label_width))  # No salirse de la imagen
            label_y = max(label_height, acc_y1)  # No salirse por arriba
            
            cv2.rectangle(annotated, (label_x, label_y - label_height), (label_x + label_width, label_y), COLOR_TEXT_BG, -1)
            cv2.putText(annotated, "ACCESORIOS DETECTADOS", (label_x + 5, label_y - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_ACCESSORY, 2)
            cv2.putText(annotated, f"{head_accessory}", (label_x + 5, label_y - 8), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)
        
        # Recuadro de CARTERAS/BOLSOS si se detectaron (DINÁMICO)
        bag_accessory = analysis.get('bag_accessory')
        if bag_accessory and bag_accessory is not None:
            # Color cian para bolsos/carteras
            COLOR_BAG = (255, 255, 0)  # Cian
            
            if pose_landmarks:
                # Usar landmarks para posición dinámica del bolso
                left_shoulder = pose_landmarks.landmark[11]
                right_shoulder = pose_landmarks.landmark[12]
                left_hip = pose_landmarks.landmark[23]
                right_hip = pose_landmarks.landmark[24]
                left_wrist = pose_landmarks.landmark[15]  # Muñeca izquierda
                right_wrist = pose_landmarks.landmark[16]  # Muñeca derecha
                
                # Determinar posición según tipo de bolso
                if bag_accessory == "mochila":
                    # Mochila: zona de la espalda/hombros (centrada)
                    center_x = int((left_shoulder.x + right_shoulder.x) / 2 * width)
                    center_y = int((left_shoulder.y + right_shoulder.y) / 2 * height)
                    bag_width = abs(left_shoulder.x - right_shoulder.x) * width * 1.2
                    bag_height = bag_width * 1.1
                    
                    bag_x1 = max(0, int(center_x - bag_width/2))
                    bag_y1 = max(0, int(center_y - bag_height * 0.3))
                    bag_x2 = min(width, int(center_x + bag_width/2))
                    bag_y2 = min(height, int(center_y + bag_height * 0.7))
                    
                elif bag_accessory == "bolso_cruzado":
                    # Bolso cruzado: lateral del torso
                    # Detectar lado más bajo (donde está el bolso)
                    if left_wrist.y > right_wrist.y:
                        # Lado izquierdo
                        center_x = int(left_hip.x * width)
                        center_y = int((left_shoulder.y + left_hip.y) / 2 * height)
                    else:
                        # Lado derecho
                        center_x = int(right_hip.x * width)
                        center_y = int((right_shoulder.y + right_hip.y) / 2 * height)
                    
                    bag_width = abs(left_shoulder.x - right_shoulder.x) * width * 0.5
                    bag_height = bag_width * 1.3
                    
                    bag_x1 = max(0, int(center_x - bag_width/2))
                    bag_y1 = max(0, int(center_y - bag_height/2))
                    bag_x2 = min(width, int(center_x + bag_width/2))
                    bag_y2 = min(height, int(center_y + bag_height/2))
                    
                else:  # cartera o default
                    # Cartera: zona baja lateral (cerca de cadera/mano)
                    # Buscar la mano más baja
                    if left_wrist.y > right_wrist.y:
                        center_x = int(left_wrist.x * width)
                        center_y = int(left_wrist.y * height)
                    else:
                        center_x = int(right_wrist.x * width)
                        center_y = int(right_wrist.y * height)
                    
                    bag_width = abs(left_shoulder.x - right_shoulder.x) * width * 0.3
                    bag_height = bag_width * 0.8
                    
                    bag_x1 = max(0, int(center_x - bag_width/2))
                    bag_y1 = max(0, int(center_y - bag_height/2))
                    bag_x2 = min(width, int(center_x + bag_width/2))
                    bag_y2 = min(height, int(center_y + bag_height/2))
            else:
                # Fallback a posición estática
                bag_x1 = int(width * 0.05)
                bag_y1 = int(height * 0.4)
                bag_x2 = int(width * 0.45)
                bag_y2 = int(height * 0.75)
            
            cv2.rectangle(annotated, (bag_x1, bag_y1), (bag_x2, bag_y2), COLOR_BAG, 4)
            
            # Etiqueta de cartera/bolso (ajustada a posición dinámica)
            label_height = 50
            label_width = 280
            label_x = max(0, min(bag_x1, width - label_width))
            label_y = max(label_height, bag_y1)
            
            cv2.rectangle(annotated, (label_x, label_y - label_height), (label_x + label_width, label_y), COLOR_TEXT_BG, -1)
            cv2.putText(annotated, "CARTERA/BOLSO", (label_x + 5, label_y - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_BAG, 2)
            cv2.putText(annotated, f"{bag_accessory}", (label_x + 5, label_y - 8), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)
    else:
        # No hay persona detectada
        text = "NO SE DETECTA PERSONA"
        cv2.rectangle(annotated, (10, 10), (400, 60), COLOR_TEXT_BG, -1)
        cv2.putText(annotated, text, (15, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Timestamp en la esquina inferior derecha
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.rectangle(annotated, (width - 220, height - 40), (width - 10, height - 10), COLOR_TEXT_BG, -1)
    cv2.putText(annotated, timestamp, (width - 215, height - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
    
    # Marca de agua
    cv2.putText(annotated, "NeoTotem AI", (10, height - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    return annotated

def analyze_realtime_stream_real(image_data_base64: str, return_annotated: bool = False) -> dict:
    """
    Análisis REAL de imagen usando MediaPipe y OpenCV.
    Versión simplificada para evitar problemas de serialización JSON.
    
    Args:
        image_data_base64: Imagen en base64
        return_annotated: Si True, incluye la imagen anotada en base64
    """
    if not image_data_base64:
        return {
            "person_detected": False,
            "face_detected": False,
            "pose_detected": False,
            "age_range": "unknown",
            "clothing_style": "unknown",
            "primary_color": "unknown",
            "secondary_color": None,
            "clothing_item": "unknown",
            "detection_confidence": 0.0,
            "recommendations": {
                "target_categories": [],
                "color_preference": "unknown",
                "style_suggestion": "unknown",
                "age_appropriate": False,
                "interaction_tips": ["Esperando imagen de cámara..."]
            }
        }
    
    try:
        # Decodificar la imagen base64
        img_bytes = base64.b64decode(image_data_base64)
        img_np = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("No se pudo decodificar la imagen base64.")
        
        # OPTIMIZACIÓN: Redimensionar imagen si es muy grande (reducir carga de procesamiento)
        height, width = image.shape[:2]
        max_dimension = 800  # Máximo 800px en cualquier dimensión
        
        if height > max_dimension or width > max_dimension:
            # Calcular escala manteniendo aspect ratio
            scale = max_dimension / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            print(f"⚡ Imagen redimensionada: {width}x{height} → {new_width}x{new_height} (optimización)")

        # Análisis simplificado para evitar problemas de serialización
        analysis = analyze_real_clothing_simple(image)
        
        # Si se solicita, añadir imagen anotada
        if return_annotated:
            # Pasar landmarks para bounding boxes dinámicos
            pose_landmarks = analysis.get('_pose_landmarks')
            annotated_image = draw_detections_on_image(image, analysis, pose_landmarks)
            
            # Redimensionar imagen anotada si es muy grande (optimización adicional)
            h_ann, w_ann = annotated_image.shape[:2]
            max_display = 640  # Máximo para visualización
            if h_ann > max_display or w_ann > max_display:
                scale = max_display / max(h_ann, w_ann)
                new_w = int(w_ann * scale)
                new_h = int(h_ann * scale)
                annotated_image = cv2.resize(annotated_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            # Reducir calidad para optimizar transmisión (60% para balance)
            _, buffer = cv2.imencode('.jpg', annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 60])
            annotated_base64 = base64.b64encode(buffer).decode('utf-8')
            analysis['annotated_image'] = annotated_base64
        
        # Limpiar landmarks internos antes de enviar (no serializable en JSON)
        if '_pose_landmarks' in analysis:
            del analysis['_pose_landmarks']
        
        return analysis
        
    except Exception as e:
        print(f"Error en análisis real: {e}")
        return {
            "person_detected": False,
            "face_detected": False,
            "pose_detected": False,
            "age_range": "error",
            "clothing_style": "error",
            "primary_color": "error",
            "secondary_color": None,
            "clothing_item": "error",
            "detection_confidence": 0.0,
            "recommendations": {
                "target_categories": [],
                "color_preference": "error",
                "style_suggestion": "error",
                "age_appropriate": False,
                "interaction_tips": [f"Error en análisis: {str(e)}"]
            }
        }

def analyze_real_clothing_simple(image_np: np.ndarray) -> dict:
    """
    Análisis simplificado de prendas que evita problemas de serialización JSON.
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "person_detected": False,
        "face_detected": False,
        "pose_detected": False,
        "age_range": "desconocido",
        "clothing_style": "casual",
        "primary_color": "desconocido",
        "secondary_color": None,
        "clothing_item": "desconocido",
        "detection_confidence": 0.0,
        "recommendations": {
            "target_categories": ["casual", "elegante", "clasico"],
            "color_preference": "desconocido",
            "style_suggestion": "casual",
            "age_appropriate": True,
            "interaction_tips": ["Análisis básico completado"]
        },
        "_pose_landmarks": None  # Para uso interno en dibujo de bounding boxes
    }

    try:
        # Convertir la imagen a RGB para MediaPipe
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        height, width, _ = image_np.shape

        # Detección facial simplificada
        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            face_results = face_detection.process(image_rgb)
            if face_results.detections:
                results["person_detected"] = True
                results["face_detected"] = True
                results["detection_confidence"] = float(face_results.detections[0].score[0])
                
                # Estimación básica de edad
                bbox = face_results.detections[0].location_data.relative_bounding_box
                face_width = bbox.width
                face_height = bbox.height
                
                if face_width > 0.15 and face_height > 0.15:
                    results["age_range"] = "36-45"
                elif face_width > 0.12 and face_height > 0.12:
                    results["age_range"] = "26-35"
                else:
                    results["age_range"] = "18-25"

        # Detección de pose simplificada
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            pose_results = pose.process(image_rgb)
            if pose_results.pose_landmarks:
                results["person_detected"] = True
                results["pose_detected"] = True
                results["_pose_landmarks"] = pose_results.pose_landmarks  # Guardar para bounding boxes dinámicos
                
                # Análisis MEJORADO de prendas usando múltiples características
                landmarks = pose_results.pose_landmarks.landmark
                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]
                left_elbow = landmarks[13]
                right_elbow = landmarks[15]
                left_hip = landmarks[23]
                right_hip = landmarks[24]
                
                # Calcular múltiples métricas
                shoulder_distance = abs(left_shoulder.x - right_shoulder.x)
                torso_height = abs((left_shoulder.y + right_shoulder.y) / 2 - (left_hip.y + right_hip.y) / 2)
                arm_coverage = abs(left_elbow.y - left_shoulder.y)
                
                # Debug: imprimir métricas calculadas
                print(f"🔍 DEBUG - Métricas de detección:")
                print(f"  Distancia hombros: {shoulder_distance:.3f}")
                print(f"  Altura torso: {torso_height:.3f}")
                print(f"  Cobertura brazos: {arm_coverage:.3f}")
                
                # Extraer región del torso para análisis de color/textura
                torso_x1 = int(min(left_shoulder.x, right_shoulder.x) * width)
                torso_y1 = int(min(left_shoulder.y, right_shoulder.y) * height)
                torso_x2 = int(max(left_shoulder.x, right_shoulder.x) * width)
                torso_y2 = int((left_hip.y + right_hip.y) / 2 * height)
                
                # Asegurar coordenadas válidas
                torso_x1 = max(0, torso_x1)
                torso_y1 = max(0, torso_y1)
                torso_x2 = min(width, torso_x2)
                torso_y2 = min(height, torso_y2)
                
                # Analizar características de la prenda
                clothing_detected = "camiseta"  # Default
                style_detected = "casual"
                
                # Primero extraer región del torso para análisis de color temporal
                torso_region_temp = image_rgb[torso_y1:torso_y2, torso_x1:torso_x2]
                temp_color = "unknown"
                
                if torso_region_temp.size > 0:
                    # Análisis rápido de color dominante en el torso
                    try:
                        avg_color = np.mean(torso_region_temp, axis=(0, 1))
                        r, g, b = avg_color.astype(int)
                        temp_color = get_color_name(r, g, b)
                        print(f"  🎨 Color temporal del torso: {temp_color} (RGB: {r},{g},{b})")
                    except:
                        temp_color = "unknown"
                
                # Criterios EXTREMADAMENTE ESTRICTOS para chaqueta (solo prendas MUY voluminosas)
                # Requiere: hombros EXTREMADAMENTE anchos + torso MUY largo + brazos MUY cubiertos
                # Solo detectar chaqueta si hay evidencia MUY clara de prenda voluminosa
                if shoulder_distance > 0.35 and torso_height > 0.50 and arm_coverage > 0.30:
                    clothing_detected = "chaqueta"
                    
                    # Determinar si es deportiva o formal por el COLOR
                    deportive_colors = ["azul", "rojo", "verde", "amarillo", "naranja", "rosa", "morado"]
                    if temp_color in deportive_colors:
                        style_detected = "deportivo"
                    else:
                        style_detected = "formal"
                    
                # Criterios para hoodie/sudadera (manga larga deportiva) - MÁS ESTRICTOS
                elif shoulder_distance > 0.25 and arm_coverage > 0.20:
                    clothing_detected = "sudadera"
                    style_detected = "deportivo"
                # Criterios para camiseta manga larga - MÁS ESTRICTOS
                elif arm_coverage > 0.19:
                    clothing_detected = "camiseta_manga_larga"
                    style_detected = "casual"
                # Default: camiseta (más común) - incluye camisetas deportivas
                else:
                    clothing_detected = "camiseta"
                    # Determinar estilo por color para camisetas
                    deportive_colors = ["azul", "rojo", "verde", "amarillo", "naranja", "rosa", "morado"]
                    if temp_color in deportive_colors:
                        style_detected = "deportivo"
                    else:
                        style_detected = "casual"
                
                results["clothing_item"] = clothing_detected
                results["clothing_style"] = style_detected
                
                # Debug: imprimir detección final
                print(f"  ✅ DETECTADO: {clothing_detected} {style_detected} ({temp_color})")
                print(f"  Criterios chaqueta: S={shoulder_distance > 0.35} ({shoulder_distance:.3f}>0.35), T={torso_height > 0.50} ({torso_height:.3f}>0.50), A={arm_coverage > 0.30} ({arm_coverage:.3f}>0.30)")
                print(f"  Criterios sudadera: S={shoulder_distance > 0.25} ({shoulder_distance:.3f}>0.25), A={arm_coverage > 0.20} ({arm_coverage:.3f}>0.20)")
                print(f"  Criterios manga larga: A={arm_coverage > 0.19} ({arm_coverage:.3f}>0.19)")

        # Detección MEJORADA de accesorios de cabeza
        # Ahora detecta múltiples accesorios simultáneamente
        try:
            accessories_detected = _detect_head_accessories_improved(image_rgb, results.get("face_detected", False))
            if accessories_detected:
                results["head_accessory"] = accessories_detected
                results["accessory_confidence"] = 1.0  # 100% confianza cuando se detecta
                print(f"🎩 Accesorios de cabeza: {accessories_detected} (confianza: 100%)")
            else:
                results["head_accessory"] = None
                results["accessory_confidence"] = 0.0
        except Exception as e:
            print(f"Error detectando accesorios de cabeza: {e}")
            results["head_accessory"] = None
            results["accessory_confidence"] = 0.0
        
        # Detección de RELOJES (muñecas)
        try:
            watch_detected = _detect_watches(image_rgb, results.get("pose_detected", False))
            if watch_detected:
                results["watch_detected"] = watch_detected
                results["watch_confidence"] = 0.9  # 90% confianza cuando se detecta
                print(f"⌚ Reloj detectado: {watch_detected} (confianza: 90%)")
            else:
                results["watch_detected"] = None
                results["watch_confidence"] = 0.0
        except Exception as e:
            print(f"Error detectando relojes: {e}")
            results["watch_detected"] = None
            results["watch_confidence"] = 0.0
        
        # Detección de CARTERAS/BOLSOS (región media-baja del cuerpo)
        try:
            bag_detected = _detect_bags_and_purses(image_rgb, results.get("pose_detected", False))
            if bag_detected:
                results["bag_accessory"] = bag_detected
                print(f"👜 Cartera/Bolso detectado: {bag_detected}")
            else:
                results["bag_accessory"] = None
        except Exception as e:
            print(f"Error detectando carteras/bolsos: {e}")
            results["bag_accessory"] = None

        # Análisis de colores MEJORADO - enfocado en el TORSO
        try:
            # Si detectamos pose, usamos el color ya calculado en temp_color
            if results.get("pose_detected", False):
                # Ya calculamos el color del torso más arriba (temp_color)
                # Simplemente usar ese valor directamente
                if '_pose_landmarks' in results and results['_pose_landmarks']:
                    # Pose detectada, extraer región del torso nuevamente
                    landmarks = results['_pose_landmarks'].landmark
                    left_shoulder = landmarks[11]
                    right_shoulder = landmarks[12]
                    left_hip = landmarks[23]
                    right_hip = landmarks[24]
                    
                    torso_x1_final = int(min(left_shoulder.x, right_shoulder.x) * width)
                    torso_y1_final = int(min(left_shoulder.y, right_shoulder.y) * height)
                    torso_x2_final = int(max(left_shoulder.x, right_shoulder.x) * width)
                    torso_y2_final = int((left_hip.y + right_hip.y) / 2 * height)
                    
                    # Asegurar coordenadas válidas
                    torso_x1_final = max(0, torso_x1_final)
                    torso_y1_final = max(0, torso_y1_final)
                    torso_x2_final = min(width, torso_x2_final)
                    torso_y2_final = min(height, torso_y2_final)
                    
                    # Extraer región del torso
                    torso_region = image_rgb[torso_y1_final:torso_y2_final, torso_x1_final:torso_x2_final]
                    
                    if torso_region.size > 0:
                        # Análisis de color del torso
                        avg_color = np.mean(torso_region, axis=(0, 1))
                        r, g, b = avg_color.astype(int)
                        detected_color = get_color_name(r, g, b)
                        results["primary_color"] = detected_color
                        print(f"🎨 Color final del torso: {detected_color} (RGB: {r},{g},{b})")
                    else:
                        print(f"⚠️ Región del torso vacía")
                        results["primary_color"] = "desconocido"
                else:
                    # Fallback: usar imagen completa
                    small_image = cv2.resize(image_np, (100, 100))
                    avg_color = np.mean(small_image, axis=(0, 1))
                    b, g, r = avg_color.astype(int)
                    detected_color = get_color_name(r, g, b)
                    results["primary_color"] = detected_color
                    print(f"🎨 Color (imagen completa): {detected_color} (RGB: {r},{g},{b})")
            else:
                # Si no hay pose, usar imagen completa
                small_image = cv2.resize(image_np, (100, 100))
                avg_color = np.mean(small_image, axis=(0, 1))
                b, g, r = avg_color.astype(int)
                detected_color = get_color_name(r, g, b)
                results["primary_color"] = detected_color
                print(f"🎨 Color (sin pose): {detected_color} (RGB: {r},{g},{b})")
            
        except Exception as e:
            print(f"Error en análisis de colores: {e}")
            import traceback
            traceback.print_exc()
            results["primary_color"] = "desconocido"

        return results
        
    except Exception as e:
        print(f"Error en análisis simplificado: {e}")
        return results

def _detect_head_accessories_improved(image_rgb: np.ndarray, face_detected: bool) -> Optional[str]:
    """
    Detecta accesorios (gorros, gafas) usando análisis visual ULTRA CONSERVADOR.
    VERSIÓN ULTRA ESTRICTA: Solo detecta cuando hay evidencia MUY clara para evitar falsos positivos.
    """
    try:
        # Si no hay cara detectada, no buscar accesorios
        if not face_detected:
            print(f"  ℹ️ No hay cara detectada, omitiendo detección de accesorios")
            return None
            
        height, width = image_rgb.shape[:2]
        accessories = []
        
        print(f"  🔍 Iniciando detección ULTRA CONSERVADORA de accesorios...")
        
        # PRIORIDAD 1: DETECCIÓN DE GAFAS (región de los ojos) - ULTRA ESTRICTA
        glasses_detected = False
        if face_detected:
            print(f"  🔍 Buscando gafas con criterios ULTRA ESTRICTOS...")
            
            # Región específica para ojos (más pequeña para evitar falsos positivos)
            eye_region = image_rgb[int(height * 0.25):int(height * 0.45), int(width * 0.25):int(width * 0.75)]
            gray_eyes = cv2.cvtColor(eye_region, cv2.COLOR_RGB2GRAY)
            
            # Mejorar contraste
            gray_eyes = cv2.equalizeHist(gray_eyes)
            
            # Blur más fuerte para reducir ruido
            gray_eyes = cv2.GaussianBlur(gray_eyes, (5, 5), 0)
            
            # Detectar bordes con umbrales MUY ESTRICTOS
            edges = cv2.Canny(gray_eyes, 100, 200)  # Umbrales altos para reducir ruido
            
            # Buscar líneas con parámetros ULTRA ESTRICTOS
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=5)
            
            if lines is not None and len(lines) >= 5:  # Mínimo 5 líneas (muy estricto)
                # Analizar líneas horizontales (marcos de gafas)
                horizontal_lines = 0
                vertical_lines = 0
                line_positions = []
                line_lengths = []
                
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
                    line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    
                    # Líneas horizontales (±15°) - muy estricto
                    if angle < 15 or angle > 165:
                        horizontal_lines += 1
                        line_positions.append((y1 + y2) / 2)
                        line_lengths.append(line_length)
                    # Líneas verticales (±15°) - patillas de gafas
                    elif 75 < angle < 105:
                        vertical_lines += 1
                
                # Criterios ULTRA ESTRICTOS para detectar gafas
                if len(line_positions) >= 3:  # Al menos 3 líneas horizontales
                    line_positions.sort()
                    max_separation = line_positions[-1] - line_positions[0]
                    avg_length = np.mean(line_lengths) if line_lengths else 0
                    
                    # Detectar gafas con criterios ULTRA ESTRICTOS
                    has_good_distribution = max_separation > eye_region.shape[0] * 0.3  # 30% de altura
                    has_long_lines = avg_length > 25  # Líneas de al menos 25px
                    has_enough_horizontal = horizontal_lines >= 3  # Mínimo 3 horizontales
                    
                    # Detección ULTRA ESTRICTA de gafas
                    if (has_enough_horizontal and 
                        has_good_distribution and 
                        has_long_lines and
                        len(lines) >= 5):  # Mínimo 5 líneas totales
                        glasses_detected = True
                        accessories.append("gafas")
                        print(f"  👓 Gafas detectadas (h:{horizontal_lines}, v:{vertical_lines}, sep:{max_separation:.1f}px, long:{avg_length:.1f}px)")
                    else:
                        print(f"  👤 NO gafas (h:{horizontal_lines}/{3}, dist:{has_good_distribution}, long:{has_long_lines}, longitud:{avg_length:.1f}px, total:{len(lines)}/{5})")
                else:
                    print(f"  👤 NO gafas (líneas horizontales insuficientes: {len(line_positions)}/{3})")
            else:
                print(f"  👤 NO gafas (líneas insuficientes: {len(lines) if lines is not None else 0}, mínimo: 5)")
        
        # PRIORIDAD 2: DETECCIÓN DE GORRO/GORRA (solo si NO hay gafas)
        # Criterios EXTREMADAMENTE ESTRICTOS para evitar falsos positivos
        if not glasses_detected:
            print(f"  🔍 Buscando gorros/gorras con criterios EXTREMADAMENTE ESTRICTOS...")
            
            # Región MUY pequeña y específica para gorros (solo parte superior)
            head_top_region = image_rgb[0:int(height * 0.2), int(width * 0.25):int(width * 0.75)]
            
            # Convertir a escala de grises
            gray_top = cv2.cvtColor(head_top_region, cv2.COLOR_RGB2GRAY)
            
            # Threshold adaptativo EXTREMADAMENTE ESTRICTO
            thresh = cv2.adaptiveThreshold(gray_top, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY_INV, 9, 1)
            
            # Morfología MUY agresiva para eliminar ruido
            kernel = np.ones((7, 7), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Umbral EXTREMADAMENTE ESTRICTO para gorros
            large_contours = [c for c in contours if cv2.contourArea(c) > 5000]  # Extremadamente estricto
            
            if len(large_contours) > 0:
                # Analizar el contorno más grande
                largest_contour = max(large_contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                x, y, w, h = cv2.boundingRect(largest_contour)
                aspect_ratio = w / h if h > 0 else 0
                extent = area / (w * h) if (w * h) > 0 else 0
                
                # Calcular posición relativa (gorros están en la parte superior)
                relative_y = y / head_top_region.shape[0]
                
                # CRITERIOS EXTREMADAMENTE ESTRICTOS para gorro/gorra
                # Solo detectar si hay evidencia MUY MUY clara
                if (area > 6000 and                    # Área extremadamente grande
                    extent > 0.8 and                   # Forma muy compacta
                    relative_y < 0.3 and                # Muy arriba en la imagen
                    aspect_ratio > 0.9 and aspect_ratio < 1.8):  # Forma muy específica
                    
                    # Gorra: ancha y en la parte superior
                    if aspect_ratio > 1.4 and w > head_top_region.shape[1] * 0.5:
                        accessories.append("gorra")
                        print(f"  🧢 Gorra detectada (área: {area:.0f}, ratio: {aspect_ratio:.2f}, y: {relative_y:.2f})")
                    # Gorro: más circular/cuadrado
                    elif 0.9 < aspect_ratio < 1.4 and w > head_top_region.shape[1] * 0.4:
                        accessories.append("gorro")
                        print(f"  🧣 Gorro detectado (área: {area:.0f}, ratio: {aspect_ratio:.2f}, y: {relative_y:.2f})")
                    else:
                        print(f"  ⚠️ Objeto detectado pero forma incorrecta (ratio: {aspect_ratio:.2f}, w: {w}, y: {relative_y:.2f})")
                else:
                    print(f"  ℹ️ Contorno no cumple criterios extremadamente estrictos (área: {area:.0f}, extent: {extent:.2f}, y: {relative_y:.2f})")
            else:
                print(f"  ✅ No se detectaron contornos grandes en región superior")
        else:
            print(f"  ℹ️ Gafas detectadas, omitiendo búsqueda de gorros")
        
        # Retornar accesorios detectados
        if len(accessories) > 0:
            print(f"  ✅ Accesorios detectados: {', '.join(accessories)}")
            return ", ".join(accessories)
        else:
            print(f"  ✅ NO se detectaron accesorios de cabeza (modo ultra conservador)")
            return None
        
    except Exception as e:
        print(f"Error detectando accesorios: {e}")
        return None

def _detect_backpack_straps(image_rgb: np.ndarray) -> bool:
    """
    Detecta TIRAS DE MOCHILA: dos tiras verticales/diagonales oscuras sobre los hombros.
    Esta es la señal MÁS CLARA de que hay una mochila.
    """
    try:
        height, width = image_rgb.shape[:2]
        
        # Región de hombros/pecho (15%-50% altura)
        shoulder_region = image_rgb[int(height * 0.15):int(height * 0.50), :]
        gray_shoulder = cv2.cvtColor(shoulder_region, cv2.COLOR_RGB2GRAY)
        
        # Threshold adaptativo para detectar objetos oscuros (tiras)
        thresh = cv2.adaptiveThreshold(gray_shoulder, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 15, 5)
        
        # Morfología para conectar tiras
        kernel_vertical = np.ones((15, 3), np.uint8)  # Kernel vertical para tiras
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_vertical)
        
        # Encontrar contornos (tiras potenciales)
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Buscar tiras: objetos alargados, verticales/diagonales, oscuros
        strap_candidates = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 800 or area > 8000:  # Tiras tienen área moderada
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calcular características
            aspect_ratio = h / w if w > 0 else 0  # Alto/ancho (tiras son verticales)
            center_x = x + w/2
            relative_x = center_x / shoulder_region.shape[1]
            
            # Criterios para TIRA DE MOCHILA:
            # 1. Alargada verticalmente (h > w)
            # 2. Aspect ratio > 2 (al menos el doble de alto que ancho)
            # 3. No demasiado ancha (< 15% del ancho de imagen)
            # 4. Posición lateral o central (no extremos)
            if (aspect_ratio > 2.0 and
                w < shoulder_region.shape[1] * 0.15 and
                0.15 < relative_x < 0.85):
                
                # Verificar que es OSCURO (mochila típicamente negra)
                contour_mask = np.zeros(gray_shoulder.shape, dtype=np.uint8)
                cv2.drawContours(contour_mask, [contour], -1, 255, -1)
                mean_val = cv2.mean(gray_shoulder, mask=contour_mask)[0]
                
                if mean_val < 100:  # Oscuro
                    strap_candidates.append({
                        'x': relative_x,
                        'y': y,
                        'area': area,
                        'ratio': aspect_ratio,
                        'darkness': mean_val
                    })
        
        # DETECTAR MOCHILA: Buscar DOS tiras simétricas (una a cada lado)
        if len(strap_candidates) >= 2:
            # Ordenar por posición X
            strap_candidates.sort(key=lambda s: s['x'])
            
            # Buscar par de tiras: una izquierda (< 0.5) y una derecha (> 0.5)
            left_straps = [s for s in strap_candidates if s['x'] < 0.45]
            right_straps = [s for s in strap_candidates if s['x'] > 0.55]
            
            if left_straps and right_straps:
                # Tomar la mejor tira de cada lado
                left = left_straps[0]
                right = right_straps[0]
                
                # Verificar simetría aproximada
                x_separation = abs(right['x'] - left['x'])
                
                # Si hay buena separación (tiras en lados opuestos)
                if x_separation > 0.3:  # Al menos 30% de ancho de separación
                    print(f"  🎒 TIRAS DE MOCHILA detectadas: izq={left['x']:.2f}, der={right['x']:.2f}, sep={x_separation:.2f}")
                    return True
        
        return False
        
    except Exception as e:
        print(f"Error detectando tiras de mochila: {e}")
        return False

def _detect_bags_and_purses(image_rgb: np.ndarray, pose_detected: bool) -> Optional[str]:
    """
    Detecta carteras, bolsos y mochilas usando análisis ULTRA CONSERVADOR.
    VERSIÓN ULTRA ESTRICTA: Solo detecta cuando hay evidencia MUY clara para evitar falsos positivos.
    """
    try:
        # Si no hay persona detectada, no buscar bolsos
        if not pose_detected:
            print(f"  ℹ️ No hay pose detectada, omitiendo detección de bolsos")
            return None
        
        print(f"  🔍 Iniciando detección ULTRA CONSERVADORA de bolsos/mochilas...")
        
        # PRIORIDAD 1: Detectar TIRAS DE MOCHILA (método más confiable)
        print(f"  🔍 Buscando tiras de mochila...")
        if _detect_backpack_straps(image_rgb):
            print(f"  ✅ Tiras de mochila detectadas")
            return "mochila"
        else:
            print(f"  ℹ️ No se detectaron tiras de mochila")
            
        height, width = image_rgb.shape[:2]
        bags_detected = []
        
        # Región MÁS PEQUEÑA del cuerpo para evitar falsos positivos
        # Solo analizar región central del torso (30%-70% altura)
        body_region = image_rgb[int(height * 0.3):int(height * 0.7), :]
        
        # Convertir a escala de grises
        gray_body = cv2.cvtColor(body_region, cv2.COLOR_RGB2GRAY)
        
        # Threshold adaptativo MÁS ESTRICTO
        thresh = cv2.adaptiveThreshold(gray_body, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morfología MÁS AGRESIVA para eliminar ruido
        kernel = np.ones((7, 7), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos por tamaño ULTRA ESTRICTO
        # Solo objetos MUY grandes para evitar falsos positivos
        large_contours = [c for c in contours if cv2.contourArea(c) > 8000]  # Muy estricto
        
        print(f"  📊 Contornos grandes encontrados: {len(large_contours)}")
        
        # PRIMERA PASADA: Buscar MOCHILA con criterios ULTRA ESTRICTOS
        mochila_detected = False
        for contour in large_contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calcular características
            aspect_ratio = w / h if h > 0 else 0
            extent = area / (w * h) if (w * h) > 0 else 0
            
            # Calcular posición relativa
            center_x = x + w/2
            relative_x = center_x / body_region.shape[1]
            relative_y = (y + h/2) / body_region.shape[0]
            
            # MOCHILA ULTRA ESTRICTA: Solo detectar si hay evidencia MUY clara
            if (area > 10000 and                    # Área MUY grande (antes 3000)
                0.3 < relative_x < 0.7 and         # Más centrado (antes 0.25-0.75)
                aspect_ratio > 0.7 and aspect_ratio < 1.5 and  # Forma más específica (antes 0.5-2.0)
                extent > 0.6 and                   # Forma muy compacta (antes 0.45)
                relative_y < 0.4):                 # Solo parte superior (antes 0.50)
                
                contour_region = body_region[y:y+h, x:x+w]
                if contour_region.size > 0:
                    region_std = np.std(contour_region)
                    region_mean = np.mean(contour_region)
                    is_dark = region_mean < 100    # MUY oscuro (antes 140)
                    
                    # Contraste MUY alto: std > 30 (antes 15)
                    if region_std > 30 and is_dark:
                        mochila_detected = True
                        bags_detected.append("mochila")
                        print(f"  🎒 Mochila detectada (área: {area:.0f}, ratio: {aspect_ratio:.2f}, y: {relative_y:.2f}, std: {region_std:.1f}, mean: {region_mean:.1f})")
                        break  # STOP: Mochila encontrada
                    else:
                        print(f"  ⚠️ Candidato a mochila rechazado: std={region_std:.1f} (min:30), mean={region_mean:.1f} (max:100)")
                else:
                    print(f"  ⚠️ Candidato a mochila rechazado: región vacía")
            else:
                print(f"  ℹ️ Contorno no cumple criterios ultra estrictos (área: {area:.0f}, ratio: {aspect_ratio:.2f}, y: {relative_y:.2f})")
        
        # SEGUNDA PASADA: Si NO hay mochila, buscar otros tipos con criterios ULTRA ESTRICTOS
        if not mochila_detected:
            print(f"  🔍 Buscando otros tipos de bolsos con criterios ultra estrictos...")
            
            # Usar contornos más grandes para otros tipos también
            very_large_contours = [c for c in contours if cv2.contourArea(c) > 12000]  # Aún más estricto
            
            for contour in very_large_contours:
                area = cv2.contourArea(contour)
                x, y, w, h = cv2.boundingRect(contour)
                
                aspect_ratio = w / h if h > 0 else 0
                extent = area / (w * h) if (w * h) > 0 else 0
                
                center_x = x + w/2
                relative_x = center_x / body_region.shape[1]
                relative_y = (y + h/2) / body_region.shape[0]
                
                # BOLSO CRUZADO ULTRA ESTRICTO: Solo si hay evidencia MUY clara
                if (area > 15000 and                    # Área MUY grande (antes 4000)
                    (relative_x < 0.2 or relative_x > 0.8) and  # MUY lateral (antes 0.25/0.75)
                    aspect_ratio > 2.5 and             # MUY alargado (antes 1.8)
                    extent > 0.5 and                  # Forma sólida (antes 0.4)
                    0.2 < relative_y < 0.6):          # Rango restringido (antes 0.25-0.75)
                    
                    # Verificación CRÍTICA: Debe ser MUY OSCURO y tener MUY ALTO CONTRASTE
                    contour_region = body_region[y:y+h, x:x+w]
                    if contour_region.size > 0:
                        region_std = np.std(contour_region)
                        region_mean = np.mean(contour_region)
                        is_dark = region_mean < 80     # MUY oscuro (antes 100)
                        has_contrast = region_std > 40  # MUY alto contraste (antes 25)
                        
                        # SOLO detectar si es MUY OSCURO Y tiene MUY ALTO CONTRASTE
                        if is_dark and has_contrast:
                            bags_detected.append("bolso_cruzado")
                            print(f"  👜 Bolso cruzado detectado (área: {area:.0f}, pos: {relative_x:.2f}, ratio: {aspect_ratio:.2f}, std: {region_std:.1f}, mean: {region_mean:.1f})")
                            break  # Solo un bolso
                        else:
                            print(f"  ⚠️ Candidato a bolso descartado: dark={is_dark} (mean:{region_mean:.1f}/80), contrast={has_contrast} (std:{region_std:.1f}/40)")
                    else:
                        print(f"  ⚠️ Candidato a bolso descartado: región vacía")
                
                # CARTERA ULTRA ESTRICTA: Solo si hay evidencia MUY clara
                elif (area > 8000 and area < 15000 and    # Rango específico
                      relative_y > 0.7 and               # MUY baja (antes 0.6)
                      (relative_x < 0.15 or relative_x > 0.85) and  # MUY lateral (antes 0.2/0.8)
                      extent > 0.6):                     # Forma muy compacta (antes 0.5)
                    
                    # Verificación adicional de oscuridad
                    contour_region = body_region[y:y+h, x:x+w]
                    if contour_region.size > 0:
                        region_mean = np.mean(contour_region)
                        is_dark = region_mean < 90  # MUY oscuro
                        
                        if is_dark:
                            bags_detected.append("cartera")
                            print(f"  👛 Cartera detectada (área: {area:.0f}, pos: {relative_x:.2f}, y: {relative_y:.2f}, mean: {region_mean:.1f})")
                            break  # Solo una cartera
                        else:
                            print(f"  ⚠️ Candidato a cartera descartado: mean={region_mean:.1f} (max:90)")
                    else:
                        print(f"  ⚠️ Candidato a cartera descartado: región vacía")
        
        # Eliminar duplicados pero mantener el orden
        if bags_detected:
            # Priorizar tipo más específico detectado
            if "mochila" in bags_detected:
                print(f"  ✅ Resultado final: mochila")
                return "mochila"
            elif "bolso_cruzado" in bags_detected:
                print(f"  ✅ Resultado final: bolso_cruzado")
                return "bolso_cruzado"
            elif "cartera" in bags_detected:
                print(f"  ✅ Resultado final: cartera")
                return "cartera"
        
        # Debug: indicar que no se detectó nada
        print(f"  ✅ NO se detectaron bolsos/carteras (modo ultra conservador)")
        return None
        
    except Exception as e:
        print(f"Error detectando carteras/bolsos: {e}")
        return None

def _detect_head_accessories_smart(image_rgb: np.ndarray) -> Optional[str]:
    """
    FUNCIÓN LEGACY - Mantener por compatibilidad
    """
    return _detect_head_accessories_improved(image_rgb, False)

def generate_real_recommendations(analysis: dict) -> dict:
    """
    Genera recomendaciones basadas en análisis real.
    """
    age_range = analysis.get("age_range", "desconocido")
    clothing_style = analysis.get("clothing_style", "casual")
    primary_color = analysis.get("primary_color", "desconocido")
    clothing_item = analysis.get("clothing_item", "desconocido")
    
    # Recomendaciones basadas en edad real detectada
    if age_range in ["18-25", "26-35"]:
        target_categories = ["moda_joven", "casual", "deportivo"]
    elif age_range in ["36-45", "46-55"]:
        target_categories = ["profesional", "elegante", "casual"]
    else:
        target_categories = ["clasico", "comodo", "elegante"]
    
    # Recomendaciones basadas en estilo detectado
    if clothing_style == "formal":
        target_categories.extend(["profesional", "elegante"])
    elif clothing_style == "juvenil":
        target_categories.extend(["moda_joven", "deportivo"])
    
    # Eliminar duplicados
    target_categories = list(set(target_categories))
    
    interaction_tips = [
        f"Cliente {age_range} años detectado",
        f"Estilo {clothing_style} identificado",
        f"Color principal: {primary_color}",
        f"Prenda detectada: {clothing_item}",
        f"Recomendar: {', '.join(target_categories[:3])}"
    ]
    
    return {
        "target_categories": target_categories,
        "color_preference": primary_color,
        "style_suggestion": clothing_style,
        "age_appropriate": True,
        "interaction_tips": interaction_tips
    }

def _detect_watches(image_rgb: np.ndarray, pose_detected: bool) -> Optional[str]:
    """
    Detecta relojes en las muñecas usando análisis visual estricto.
    VERSIÓN MUY CONSERVADORA: Solo detecta cuando hay evidencia clara de reloj.
    """
    try:
        # Si no hay pose detectada, no buscar relojes
        if not pose_detected:
            return None
            
        height, width = image_rgb.shape[:2]
        
        # Regiones de muñecas (aproximadamente 60-80% de altura, 20-40% y 60-80% de ancho)
        left_wrist_region = image_rgb[int(height * 0.6):int(height * 0.8), int(width * 0.2):int(width * 0.4)]
        right_wrist_region = image_rgb[int(height * 0.6):int(height * 0.8), int(width * 0.6):int(width * 0.8)]
        
        watches_detected = []
        
        # Analizar muñeca izquierda
        left_watch = _analyze_wrist_region(left_wrist_region, "izquierda")
        if left_watch:
            watches_detected.append(left_watch)
            
        # Analizar muñeca derecha
        right_watch = _analyze_wrist_region(right_wrist_region, "derecha")
        if right_watch:
            watches_detected.append(right_watch)
        
        if watches_detected:
            return ", ".join(watches_detected)
        else:
            print(f"  ✅ NO se detectaron relojes en las muñecas")
            return None
            
    except Exception as e:
        print(f"Error detectando relojes: {e}")
        return None

def _analyze_wrist_region(wrist_region: np.ndarray, side: str) -> Optional[str]:
    """
    Analiza una región de muñeca para detectar relojes.
    CRITERIOS MUY ESTRICTOS para evitar falsos positivos.
    """
    try:
        if wrist_region.size == 0:
            return None
            
        # Convertir a escala de grises
        gray_wrist = cv2.cvtColor(wrist_region, cv2.COLOR_RGB2GRAY)
        
        # Aplicar blur para reducir ruido
        gray_wrist = cv2.GaussianBlur(gray_wrist, (5, 5), 0)
        
        # Detectar bordes con umbrales MUY ESTRICTOS
        edges = cv2.Canny(gray_wrist, 150, 250)
        
        # Buscar contornos circulares/rectangulares (forma de reloj)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos por tamaño y forma (ajustado para relojes reales)
        watch_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100 or area > 3000:  # Tamaño ajustado para relojes reales
                continue
                
            # Verificar forma circular/rectangular
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
                
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0
            
            # CRITERIOS AJUSTADOS para relojes reales
            if (0.5 < aspect_ratio < 2.0 and  # Forma más flexible
                circularity > 0.2 and        # Forma menos estricta
                area > 150 and               # Tamaño mínimo ajustado
                w > 10 and h > 10):          # Dimensiones mínimas ajustadas
                
                watch_contours.append({
                    'contour': contour,
                    'area': area,
                    'circularity': circularity,
                    'aspect_ratio': aspect_ratio
                })
        
        # Si encontramos contornos que parecen relojes
        if len(watch_contours) > 0:
            # Analizar el mejor candidato
            best_watch = max(watch_contours, key=lambda x: x['area'])
            
            # Verificar que el contorno esté en el centro de la región (muñeca)
            x, y, w, h = cv2.boundingRect(best_watch['contour'])
            center_x = x + w // 2
            center_y = y + h // 2
            
            # El reloj debe estar en el centro de la muñeca
            region_center_x = wrist_region.shape[1] // 2
            region_center_y = wrist_region.shape[0] // 2
            
            distance_from_center = np.sqrt((center_x - region_center_x)**2 + (center_y - region_center_y)**2)
            max_distance = min(wrist_region.shape[0], wrist_region.shape[1]) // 3
            
            if distance_from_center < max_distance:
                print(f"  ⌚ Reloj detectado en muñeca {side} (área: {best_watch['area']:.0f}, circularidad: {best_watch['circularity']:.2f})")
                return f"reloj_{side}"
            else:
                print(f"  ⚠️ Objeto detectado pero no en posición de reloj (distancia: {distance_from_center:.1f})")
        else:
            print(f"  ✅ No se detectaron objetos con forma de reloj en muñeca {side}")
            
        return None
        
    except Exception as e:
        print(f"Error analizando muñeca {side}: {e}")
        return None

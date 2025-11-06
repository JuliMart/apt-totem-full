#!/usr/bin/env python3
"""
Script para probar la visualización de detecciones
"""
import requests
import json
import base64
import cv2
import numpy as np

def test_visualization():
    """Probar el endpoint de visualización"""
    
    # URL del backend
    base_url = "http://localhost:8001"
    
    print("🧪 Probando visualización de detecciones...")
    
    # 1. Verificar que el backend esté corriendo
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Backend conectado: {response.status_code}")
    except:
        print("❌ Backend no disponible. Asegúrate de que esté corriendo en puerto 8001")
        return
    
    # 2. Crear una imagen de prueba
    print("📸 Creando imagen de prueba...")
    test_image = np.zeros((400, 600, 3), dtype=np.uint8)
    test_image[:] = (200, 200, 200)  # Fondo gris
    
    # Dibujar una figura simple
    cv2.rectangle(test_image, (100, 100), (500, 350), (255, 255, 255), -1)  # Cuerpo blanco
    cv2.circle(test_image, (300, 80), 40, (255, 200, 200), -1)  # Cabeza
    cv2.rectangle(test_image, (150, 200), (450, 300), (0, 100, 200), -1)  # Camisa azul
    
    # Codificar imagen
    _, buffer = cv2.imencode('.jpg', test_image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # 3. Datos de análisis simulados
    analysis_data = {
        "person_detected": True,
        "age_range": "26-35",
        "clothing_item": "camiseta",
        "clothing_style": "casual",
        "primary_color": "azul",
        "secondary_color": "blanco",
        "head_accessory": "gafas",
        "detection_confidence": 0.85,
        "accessory_confidence": 0.75
    }
    
    print("🔍 Enviando análisis a visualización...")
    
    # 4. Llamar al endpoint de visualización
    try:
        response = requests.post(
            f"{base_url}/visualization/analyze-image",
            params={
                "image_data": image_base64,
                "analysis_data": json.dumps(analysis_data)
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Análisis completado")
            print(f"📊 Detecciones:")
            print(f"   - Vestimenta: {result['detections']['clothing_detected']}")
            print(f"   - Color: {result['detections']['color_detected']}")
            print(f"   - Accesorio: {result['detections']['accessory_detected']}")
            print(f"   - Cara: {result['detections']['face_detected']}")
            
            # Guardar imagen anotada
            annotated_bytes = base64.b64decode(result['annotated_image'])
            with open('test_annotated.jpg', 'wb') as f:
                f.write(annotated_bytes)
            print("💾 Imagen anotada guardada como 'test_annotated.jpg'")
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
    
    # 5. Información sobre detecciones
    try:
        response = requests.get(f"{base_url}/visualization/detection-info")
        if response.status_code == 200:
            info = response.json()
            print("\n📋 Tipos de detección disponibles:")
            for detection_type, details in info['detection_types'].items():
                print(f"   - {details['name']}: {details['description']}")
    except Exception as e:
        print(f"❌ Error obteniendo información: {e}")

if __name__ == "__main__":
    test_visualization()




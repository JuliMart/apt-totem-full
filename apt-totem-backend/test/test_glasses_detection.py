#!/usr/bin/env python3
"""
Script para probar la detección de gafas mejorada
"""
import cv2
import numpy as np
from services.ai.real_detection import _detect_head_accessories_improved

def test_glasses_detection():
    """Probar la detección de gafas con una imagen de prueba"""
    
    # Crear una imagen de prueba simulada con gafas
    height, width = 480, 640
    image_rgb = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Simular una persona con gafas
    # Cuerpo (azul)
    cv2.rectangle(image_rgb, (200, 200), (440, 450), (100, 150, 200), -1)
    
    # Cabeza (color piel)
    cv2.circle(image_rgb, (320, 180), 60, (220, 180, 150), -1)
    
    # Gafas (rectángulos negros)
    cv2.rectangle(image_rgb, (280, 160), (360, 200), (0, 0, 0), 3)  # Marco de gafas
    cv2.rectangle(image_rgb, (290, 170), (300, 190), (0, 0, 0), -1)  # Lente izquierdo
    cv2.rectangle(image_rgb, (340, 170), (350, 190), (0, 0, 0), -1)  # Lente derecho
    
    print("🧪 Probando detección de gafas...")
    print(f"Imagen de prueba: {height}x{width}")
    
    # Probar detección
    result = _detect_head_accessories_improved(image_rgb, face_detected=True)
    
    if result:
        print(f"✅ Accesorio detectado: {result}")
        if "gafas" in result:
            print("🎉 ¡Gafas detectadas correctamente!")
            return True
        else:
            print(f"⚠️ Se detectó {result} en lugar de gafas")
            return False
    else:
        print("❌ No se detectó ningún accesorio")
        return False

if __name__ == "__main__":
    success = test_glasses_detection()
    if success:
        print("🎉 ¡Detección de gafas funcionando!")
    else:
        print("⚠️ La detección de gafas necesita más ajustes")


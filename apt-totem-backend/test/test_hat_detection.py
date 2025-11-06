#!/usr/bin/env python3
"""
Script para probar la detección de gorros mejorada
"""
import cv2
import numpy as np
from services.ai.real_detection import _detect_head_accessories_improved

def test_hat_detection():
    """Probar la detección de gorros con una imagen de prueba"""
    
    # Crear una imagen de prueba simulada con un gorro
    height, width = 480, 640
    image_rgb = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Simular una persona con gorro
    # Cuerpo (azul)
    cv2.rectangle(image_rgb, (200, 200), (440, 450), (100, 150, 200), -1)
    
    # Cabeza (color piel)
    cv2.circle(image_rgb, (320, 180), 60, (220, 180, 150), -1)
    
    # Gorro (color marrón)
    cv2.ellipse(image_rgb, (320, 160), (80, 40), 0, 0, 360, (139, 69, 19), -1)
    
    print("🧪 Probando detección de gorros...")
    print(f"Imagen de prueba: {height}x{width}")
    
    # Probar detección
    result = _detect_head_accessories_improved(image_rgb, face_detected=True)
    
    if result:
        print(f"✅ Gorro detectado: {result}")
    else:
        print("❌ No se detectó gorro")
        
    return result is not None

if __name__ == "__main__":
    success = test_hat_detection()
    if success:
        print("🎉 ¡Detección de gorros funcionando!")
    else:
        print("⚠️ La detección necesita más ajustes")


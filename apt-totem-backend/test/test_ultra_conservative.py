#!/usr/bin/env python3
"""
Script para probar la detección ULTRA CONSERVADORA de accesorios.
"""

import sys
import os
import numpy as np

# Agregar el directorio del backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai.real_detection import _detect_head_accessories_improved

def test_ultra_conservative_logic():
    """
    Prueba la lógica ULTRA CONSERVADORA de detección de accesorios.
    """
    print("🧪 PRUEBA DE LÓGICA ULTRA CONSERVADORA")
    print("=" * 50)
    
    # Crear una imagen simulada (array de numpy)
    # Simulamos una imagen de 480x640 con 3 canales RGB
    height, width = 480, 640
    test_image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    
    print(f"📊 Imagen simulada: {test_image.shape}")
    
    # Probar con cara detectada = True
    print(f"\n🔍 Probando con cara detectada (modo ultra conservador)...")
    result_with_face = _detect_head_accessories_improved(test_image, face_detected=True)
    print(f"   Resultado: {result_with_face}")
    
    # Probar con cara detectada = False
    print(f"\n🔍 Probando sin cara detectada...")
    result_without_face = _detect_head_accessories_improved(test_image, face_detected=False)
    print(f"   Resultado: {result_without_face}")
    
    print(f"\n✅ Prueba de lógica ultra conservadora completada")
    print(f"\n📝 MEJORAS IMPLEMENTADAS:")
    print(f"   🔹 Modo ULTRA CONSERVADOR activado")
    print(f"   🔹 Criterios EXTREMADAMENTE ESTRICTOS para gorros")
    print(f"   🔹 Área mínima para gorros: 6000px (antes 4000px)")
    print(f"   🔹 Región más pequeña para gorros: 20% altura (antes 25%)")
    print(f"   🔹 Líneas mínimas para gafas: 5 (antes 3)")
    print(f"   🔹 Umbrales Canny más altos: 100-200 (antes 80-160)")
    print(f"   🔹 Solo detecta si hay evidencia MUY MUY clara")
    print(f"\n🎯 RESULTADO ESPERADO:")
    print(f"   ✅ NO debería detectar 'gorro' cuando no hay gafas")
    print(f"   ✅ Solo detectará accesorios con evidencia muy clara")

if __name__ == "__main__":
    test_ultra_conservative_logic()


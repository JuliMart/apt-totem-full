#!/usr/bin/env python3
"""
Script para probar la detección ULTRA CONSERVADORA de bolsos/mochilas.
"""

import sys
import os
import numpy as np

# Agregar el directorio del backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai.real_detection import _detect_bags_and_purses

def test_ultra_conservative_bag_detection():
    """
    Prueba la lógica ULTRA CONSERVADORA de detección de bolsos/mochilas.
    """
    print("🧪 PRUEBA DE DETECCIÓN ULTRA CONSERVADORA DE BOLSOS/MOCHILAS")
    print("=" * 60)
    
    # Crear una imagen simulada (array de numpy)
    # Simulamos una imagen de 480x640 con 3 canales RGB
    height, width = 480, 640
    test_image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    
    print(f"📊 Imagen simulada: {test_image.shape}")
    
    # Probar con pose detectada = True
    print(f"\n🔍 Probando con pose detectada (modo ultra conservador)...")
    result_with_pose = _detect_bags_and_purses(test_image, pose_detected=True)
    print(f"   Resultado: {result_with_pose}")
    
    # Probar con pose detectada = False
    print(f"\n🔍 Probando sin pose detectada...")
    result_without_pose = _detect_bags_and_purses(test_image, pose_detected=False)
    print(f"   Resultado: {result_without_pose}")
    
    print(f"\n✅ Prueba de lógica ultra conservadora completada")
    print(f"\n📝 MEJORAS IMPLEMENTADAS PARA BOLSOS/MOCHILAS:")
    print(f"   🔹 Modo ULTRA CONSERVADOR activado")
    print(f"   🔹 Área mínima para mochilas: 10000px (antes 3000px)")
    print(f"   🔹 Área mínima para bolsos: 15000px (antes 4000px)")
    print(f"   🔹 Región más pequeña: 30%-70% altura (antes 20%-85%)")
    print(f"   🔹 Contraste mínimo: std > 30 (antes 15)")
    print(f"   🔹 Oscuridad máxima: mean < 100 (antes 140)")
    print(f"   🔹 Solo detecta con evidencia MUY MUY clara")
    print(f"\n🎯 RESULTADO ESPERADO:")
    print(f"   ✅ NO debería detectar 'mochila' cuando no hay ninguna")
    print(f"   ✅ Solo detectará bolsos con evidencia muy clara")
    print(f"   ✅ Casi cero falsos positivos")

if __name__ == "__main__":
    test_ultra_conservative_bag_detection()


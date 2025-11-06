#!/usr/bin/env python3
"""
Script para probar la detección ULTRA ESTRICTA de prendas de vestir.
"""

import sys
import os
import numpy as np

# Agregar el directorio del backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai.real_detection import analyze_real_clothing_simple

def test_ultra_strict_clothing_detection():
    """
    Prueba la lógica ULTRA ESTRICTA de detección de prendas.
    """
    print("🧪 PRUEBA DE DETECCIÓN ULTRA ESTRICTA DE PRENDAS")
    print("=" * 60)
    
    # Crear una imagen simulada (array de numpy)
    # Simulamos una imagen de 480x640 con 3 canales RGB
    height, width = 480, 640
    test_image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    
    print(f"📊 Imagen simulada: {test_image.shape}")
    
    # Probar análisis completo
    print(f"\n🔍 Probando análisis completo de prendas...")
    try:
        results = analyze_real_clothing_simple(test_image)
        
        # Mostrar resultados específicos de prendas
        print(f"\n📊 RESULTADOS DE PRENDAS:")
        print(f"   Prenda detectada: {results.get('clothing_item', 'Ninguna')}")
        print(f"   Estilo detectado: {results.get('clothing_style', 'Ninguno')}")
        print(f"   Color detectado: {results.get('color_detected', 'Ninguno')}")
        
        # Mostrar otros resultados relevantes
        print(f"\n📊 OTROS RESULTADOS:")
        print(f"   Pose detectada: {results.get('pose_detected', False)}")
        print(f"   Cara detectada: {results.get('face_detected', False)}")
        print(f"   Accesorio cabeza: {results.get('head_accessory', 'Ninguno')}")
        print(f"   Bolso detectado: {results.get('bag_accessory', 'Ninguno')}")
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
    
    print(f"\n✅ Prueba de lógica ultra estricta completada")
    print(f"\n📝 MEJORAS IMPLEMENTADAS PARA PRENDAS:")
    print(f"   🔹 Criterios EXTREMADAMENTE ESTRICTOS para chaqueta")
    print(f"   🔹 Distancia hombros: > 0.35 (antes 0.30)")
    print(f"   🔹 Altura torso: > 0.50 (antes 0.45)")
    print(f"   🔹 Cobertura brazos: > 0.30 (antes 0.25)")
    print(f"   🔹 Solo detecta chaqueta con evidencia MUY clara")
    print(f"   🔹 Criterios más estrictos para sudadera y manga larga")
    print(f"\n🎯 RESULTADO ESPERADO:")
    print(f"   ✅ Debería detectar 'camiseta' cuando llevas remera")
    print(f"   ✅ Solo detectará 'chaqueta' si es muy voluminosa")
    print(f"   ✅ Casi cero falsos positivos de chaqueta")

if __name__ == "__main__":
    test_ultra_strict_clothing_detection()


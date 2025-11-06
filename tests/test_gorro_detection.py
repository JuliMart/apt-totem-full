#!/usr/bin/env python3
"""
Script para probar la detección de gorro en tiempo real
"""

import requests
import json
import time

def test_gorro_detection():
    """Prueba la detección de gorro usando el endpoint demo"""
    
    print("🧢 Probando detección de gorro...")
    print("=" * 50)
    
    try:
        # Probar endpoint demo
        response = requests.get("http://localhost:8001/cv/analyze-customer-ai")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Respuesta del servidor:")
            print(f"👤 Persona detectada: {data.get('person_detected', False)}")
            print(f"🎂 Rango de edad: {data.get('age_range', 'desconocido')}")
            print(f"👕 Prenda detectada: {data.get('clothing_item', 'desconocido')}")
            print(f"🎨 Color principal: {data.get('primary_color', 'desconocido')}")
            print(f"👔 Estilo: {data.get('clothing_style', 'desconocido')}")
            print(f"📊 Confianza: {data.get('confidence', 0) * 100:.1f}%")
            print(f"🤖 Tipo de análisis: {data.get('analysis_type', 'desconocido')}")
            
            # Verificar si detecta accesorios de cabeza
            clothing_item = data.get('clothing_item', '').lower()
            head_accessories = ['gorro', 'gorra', 'jockey', 'sombrero', 'gafas']
            
            if any(accessory in clothing_item for accessory in head_accessories):
                print("\n🧢 ¡ACCESORIO DE CABEZA DETECTADO!")
                print(f"   Tipo: {clothing_item}")
            else:
                print("\n❌ No se detectó accesorio de cabeza")
                print(f"   Prenda detectada: {clothing_item}")
                
        else:
            print(f"❌ Error en la respuesta: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

def test_multiple_detections():
    """Prueba múltiples detecciones para ver variabilidad"""
    
    print("\n🔄 Probando múltiples detecciones...")
    print("=" * 50)
    
    detections = []
    
    for i in range(5):
        try:
            response = requests.get("http://localhost:8001/cv/analyze-customer-ai")
            if response.status_code == 200:
                data = response.json()
                clothing = data.get('clothing_item', 'desconocido')
                detections.append(clothing)
                print(f"Prueba {i+1}: {clothing}")
            time.sleep(1)
        except Exception as e:
            print(f"Error en prueba {i+1}: {e}")
    
    # Análisis de resultados
    print(f"\n📊 Resumen de {len(detections)} detecciones:")
    from collections import Counter
    counter = Counter(detections)
    
    for item, count in counter.most_common():
        percentage = (count / len(detections)) * 100
        print(f"   {item}: {count} veces ({percentage:.1f}%)")
    
    # Verificar si hay accesorios de cabeza
    head_accessories = ['gorro', 'gorra', 'jockey', 'sombrero', 'gafas']
    head_detected = any(any(acc in item.lower() for acc in head_accessories) for item in detections)
    
    if head_detected:
        print("\n🧢 ¡Se detectaron accesorios de cabeza en algunas pruebas!")
    else:
        print("\n❌ No se detectaron accesorios de cabeza en ninguna prueba")

if __name__ == "__main__":
    print("🧢 PRUEBA DE DETECCIÓN DE GORRO")
    print("=" * 50)
    print("Asegúrate de tener el gorro puesto y estar frente a la cámara")
    print("=" * 50)
    
    test_gorro_detection()
    test_multiple_detections()
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")
    print("💡 Para análisis con imagen real, usa el frontend en http://localhost:3000")












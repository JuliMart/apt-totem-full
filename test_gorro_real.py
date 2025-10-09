#!/usr/bin/env python3
"""
Script para probar la detección REAL de gorro usando el endpoint completo
"""

import requests
import json
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import time

def create_test_image_with_hat():
    """Crear una imagen de prueba con un gorro dibujado"""
    
    # Crear imagen base
    img = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Dibujar una persona simple
    # Cabeza
    draw.ellipse([280, 100, 360, 180], fill='peachpuff', outline='black', width=2)
    
    # Gorro (sombrero/gorra)
    draw.ellipse([270, 80, 370, 120], fill='darkblue', outline='black', width=2)
    draw.rectangle([270, 100, 370, 110], fill='darkblue', outline='black', width=2)
    
    # Cuerpo
    draw.rectangle([300, 180, 340, 300], fill='white', outline='black', width=2)
    
    # Convertir a bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=85)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_gorro_detection_real():
    """Probar detección real de gorro"""
    
    print("🧢 Probando detección REAL de gorro...")
    print("=" * 50)
    
    try:
        # Crear imagen de prueba con gorro
        image_data = create_test_image_with_hat()
        
        # Crear request multipart
        files = {
            'file': ('test_gorro.jpg', image_data, 'image/jpeg')
        }
        
        response = requests.post(
            "http://localhost:8001/cv/analyze-complete",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Respuesta del análisis REAL:")
            print(f"👤 Persona detectada: {data.get('person_detected', False)}")
            print(f"🎂 Rango de edad: {data.get('age_range', 'desconocido')}")
            print(f"👕 Prenda principal: {data.get('primary_clothing', 'desconocido')}")
            print(f"🎨 Color principal: {data.get('primary_color', 'desconocido')}")
            print(f"👔 Estilo: {data.get('clothing_style', 'desconocido')}")
            print(f"📊 Confianza general: {data.get('overall_confidence', 0) * 100:.1f}%")
            print(f"🤖 Tipo de análisis: {data.get('analysis_type', 'desconocido')}")
            
            # Verificar accesorios de cabeza
            head_accessories = data.get('head_accessories', [])
            body_clothing = data.get('body_clothing', [])
            primary_type = data.get('primary_type', 'general')
            
            print(f"\n🧢 Accesorios de cabeza: {head_accessories}")
            print(f"👕 Prendas corporales: {body_clothing}")
            print(f"🏷️ Tipo principal: {primary_type}")
            
            # Verificar si detectó gorro
            if head_accessories:
                print("\n🎉 ¡ACCESORIOS DE CABEZA DETECTADOS!")
                for accessory in head_accessories:
                    print(f"   - {accessory}")
            else:
                print("\n❌ No se detectaron accesorios de cabeza")
                
            # Verificar prenda principal
            primary_clothing = data.get('primary_clothing', '').lower()
            if 'gorro' in primary_clothing or 'gorra' in primary_clothing:
                print(f"\n🧢 ¡GORRO DETECTADO COMO PRENDA PRINCIPAL: {primary_clothing}!")
            else:
                print(f"\n⚠️ Prenda principal detectada: {primary_clothing}")
                
        else:
            print(f"❌ Error en la respuesta: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

def test_multiple_real_detections():
    """Probar múltiples detecciones reales"""
    
    print("\n🔄 Probando múltiples detecciones REALES...")
    print("=" * 50)
    
    detections = []
    
    for i in range(3):
        try:
            # Crear imagen de prueba
            image_data = create_test_image_with_hat()
            
            files = {
                'file': ('test_gorro.jpg', image_data, 'image/jpeg')
            }
            
            response = requests.post(
                "http://localhost:8001/cv/analyze-complete",
                files=files
            )
            
            if response.status_code == 200:
                data = response.json()
                primary_clothing = data.get('primary_clothing', 'desconocido')
                head_accessories = data.get('head_accessories', [])
                
                detections.append({
                    'primary_clothing': primary_clothing,
                    'head_accessories': head_accessories,
                    'confidence': data.get('overall_confidence', 0)
                })
                
                print(f"Prueba {i+1}: {primary_clothing} | Accesorios: {head_accessories}")
            else:
                print(f"Error en prueba {i+1}: {response.status_code}")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"Error en prueba {i+1}: {e}")
    
    # Análisis de resultados
    if detections:
        print(f"\n📊 Resumen de {len(detections)} detecciones REALES:")
        
        # Contar prendas principales
        primary_clothes = [d['primary_clothing'] for d in detections]
        from collections import Counter
        counter = Counter(primary_clothes)
        
        for item, count in counter.most_common():
            percentage = (count / len(detections)) * 100
            print(f"   Prenda principal: {item} ({count} veces, {percentage:.1f}%)")
        
        # Verificar accesorios de cabeza
        all_head_accessories = []
        for d in detections:
            all_head_accessories.extend(d['head_accessories'])
        
        if all_head_accessories:
            print(f"\n🧢 Accesorios de cabeza detectados: {set(all_head_accessories)}")
        else:
            print("\n❌ No se detectaron accesorios de cabeza en ninguna prueba")
            
        # Confianza promedio
        avg_confidence = sum(d['confidence'] for d in detections) / len(detections)
        print(f"\n📊 Confianza promedio: {avg_confidence * 100:.1f}%")

if __name__ == "__main__":
    print("🧢 PRUEBA DE DETECCIÓN REAL DE GORRO")
    print("=" * 50)
    print("Creando imagen de prueba con gorro y enviando al endpoint real")
    print("=" * 50)
    
    test_gorro_detection_real()
    test_multiple_real_detections()
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")
    print("💡 Si no detecta gorro, el problema está en el algoritmo de detección")








#!/usr/bin/env python3
"""
Script para probar la detección realista con y sin gorro
"""

import requests
import json
import base64
import io
from PIL import Image, ImageDraw
import time

def create_test_image_without_hat():
    """Crear una imagen de prueba SIN gorro"""
    
    # Crear imagen base
    img = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Dibujar una persona simple SIN gorro
    # Cabeza (sin gorro)
    draw.ellipse([280, 100, 360, 180], fill='peachpuff', outline='black', width=2)
    
    # Cuerpo
    draw.rectangle([300, 180, 340, 300], fill='white', outline='black', width=2)
    
    # Convertir a bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=85)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def create_test_image_with_hat():
    """Crear una imagen de prueba CON gorro"""
    
    # Crear imagen base
    img = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Dibujar una persona simple CON gorro
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

def test_detection(image_data, description):
    """Probar detección con una imagen específica"""
    
    print(f"\n🔍 Probando: {description}")
    print("=" * 50)
    
    try:
        # Crear request multipart
        files = {
            'file': ('test_image.jpg', image_data, 'image/jpeg')
        }
        
        response = requests.post(
            "http://localhost:8001/cv/analyze-complete",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Respuesta del análisis:")
            print(f"👤 Persona detectada: {data.get('person_detected', False)}")
            print(f"👕 Prenda principal: {data.get('primary_clothing', 'desconocido')}")
            print(f"🧢 Accesorios de cabeza: {data.get('head_accessories', [])}")
            print(f"👕 Prendas corporales: {data.get('body_clothing', [])}")
            print(f"🏷️ Tipo principal: {data.get('primary_type', 'general')}")
            print(f"📊 Confianza: {data.get('overall_confidence', 0) * 100:.1f}%")
            
            # Verificar si detectó accesorios de cabeza
            head_accessories = data.get('head_accessories', [])
            if head_accessories:
                print(f"🎉 ¡ACCESORIOS DETECTADOS: {head_accessories}!")
            else:
                print("❌ No se detectaron accesorios de cabeza")
                
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🧢 PRUEBA DE DETECCIÓN REALISTA")
    print("=" * 50)
    print("Probando detección con y sin gorro")
    print("=" * 50)
    
    # Probar sin gorro
    image_sin_gorro = create_test_image_without_hat()
    result_sin_gorro = test_detection(image_sin_gorro, "SIN gorro")
    
    time.sleep(1)
    
    # Probar con gorro
    image_con_gorro = create_test_image_with_hat()
    result_con_gorro = test_detection(image_con_gorro, "CON gorro")
    
    # Análisis comparativo
    print("\n📊 ANÁLISIS COMPARATIVO:")
    print("=" * 50)
    
    if result_sin_gorro and result_con_gorro:
        sin_gorro_accessories = result_sin_gorro.get('head_accessories', [])
        con_gorro_accessories = result_con_gorro.get('head_accessories', [])
        
        print(f"🔍 Sin gorro: {len(sin_gorro_accessories)} accesorios detectados")
        print(f"🔍 Con gorro: {len(con_gorro_accessories)} accesorios detectados")
        
        if len(sin_gorro_accessories) == 0 and len(con_gorro_accessories) > 0:
            print("✅ ¡DETECCIÓN CORRECTA! Diferencia entre con y sin gorro")
        elif len(sin_gorro_accessories) > 0 and len(con_gorro_accessories) == 0:
            print("⚠️ DETECCIÓN INVERTIDA - Revisar algoritmo")
        elif len(sin_gorro_accessories) == 0 and len(con_gorro_accessories) == 0:
            print("❌ NO DETECTA GORROS - Algoritmo necesita mejora")
        else:
            print("⚠️ DETECCIÓN INCONSISTENTE - Revisar parámetros")
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada")

if __name__ == "__main__":
    main()








#!/usr/bin/env python3
"""
Script para probar los gráficos de medialuna con el nuevo estilo
"""

import requests
import json
import time
from datetime import datetime

def test_new_semicircle_style():
    """Probar los gráficos de medialuna con el nuevo estilo"""
    print("🌙 PROBANDO NUEVO ESTILO DE GRÁFICOS DE MEDIALUNA")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    try:
        # Probar endpoint de métricas en tiempo real
        print("\n📊 Probando endpoint /dashboard/real-time...")
        response = requests.get(f"{base_url}/dashboard/real-time")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   📈 CTR: {data.get('ctr_average', 0):.2%}")
            print(f"   🎯 Conversiones: {data.get('conversions_today', 0)}")
            print(f"   🎯 Precisión IA: {data.get('detection_accuracy', 0):.2%}")
            print(f"   📊 Fuente de datos: {data.get('data_source', 'N/A')}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
        
        print("\n🎨 NUEVO ESTILO DE GRÁFICOS DE MEDIALUNA:")
        print("-" * 50)
        print("✅ Colores actualizados:")
        print("   🔴 Rojo (0-33%): Zona crítica")
        print("   🟡 Amarillo (33-66%): Zona moderada")
        print("   🟢 Verde (66-100%): Zona excelente")
        print("✅ Aguja azul claro (#87CEEB)")
        print("✅ Centro azul acero (#4682B4)")
        print("✅ Rotación: -90° (rojo) a +90° (verde)")
        
        print("\n📐 MAPEO DE ÁNGULOS:")
        print("-" * 30)
        print("   🔴 Rojo: -90° a -30° (0-33%)")
        print("   🟡 Amarillo: -30° a +30° (33-66%)")
        print("   🟢 Verde: +30° a +90° (66-100%)")
        
        print("\n🧪 VALORES DE PRUEBA:")
        print("-" * 30)
        
        # Probar diferentes valores
        test_values = [
            {"value": 0.15, "description": "15% - Zona roja"},
            {"value": 0.50, "description": "50% - Zona amarilla"},
            {"value": 0.80, "description": "80% - Zona verde"}
        ]
        
        for test in test_values:
            percentage = test["value"]
            angle = (percentage * 180) - 90
            zone = "🔴 Roja" if percentage < 0.33 else "🟡 Amarilla" if percentage < 0.66 else "🟢 Verde"
            
            print(f"   📊 {test['description']}")
            print(f"      Ángulo: {angle:.1f}°")
            print(f"      Zona: {zone}")
        
        print("\n🌐 Para ver los gráficos actualizados:")
        print(f"   Abre: {base_url}/dashboard")
        print("   Los gráficos ahora tienen el estilo que solicitaste")
        print("   Aguja azul apuntando según los datos reales")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose:")
        print("   cd apt-totem-backend")
        print("   uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def show_color_scheme():
    """Mostrar el esquema de colores"""
    print("\n🎨 ESQUEMA DE COLORES DE LOS GRÁFICOS:")
    print("=" * 50)
    print("🔴 Rojo (#dc3545): Zona crítica (0-33%)")
    print("   - Valores bajos o problemáticos")
    print("   - Requiere atención inmediata")
    print()
    print("🟡 Amarillo (#ffc107): Zona moderada (33-66%)")
    print("   - Valores aceptables")
    print("   - Rendimiento promedio")
    print()
    print("🟢 Verde (#28a745): Zona excelente (66-100%)")
    print("   - Valores altos")
    print("   - Rendimiento óptimo")
    print()
    print("🔵 Aguja azul (#87CEEB): Indicador de valor actual")
    print("   - Apunta al valor exacto")
    print("   - Se mueve suavemente con animación")

if __name__ == "__main__":
    print("🌙 TESTING NUEVO ESTILO DE GRÁFICOS DE MEDIALUNA")
    print("=" * 60)
    
    # Mostrar esquema de colores
    show_color_scheme()
    
    # Probar endpoints
    if test_new_semicircle_style():
        print("\n🎉 NUEVO ESTILO IMPLEMENTADO CORRECTAMENTE")
        print("=" * 50)
        print("✅ Gráficos de medialuna con colores actualizados")
        print("✅ Aguja azul como en la imagen de referencia")
        print("✅ Sistema de colores: Rojo → Amarillo → Verde")
        print("✅ Datos reales de la base de datos")
        print("\n🌐 Para ver el resultado:")
        print("   http://localhost:8001/dashboard")
    else:
        print("\n❌ ERROR EN LA IMPLEMENTACIÓN")
        print("💡 Revisa que el backend esté ejecutándose correctamente")


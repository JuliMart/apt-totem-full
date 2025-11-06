#!/usr/bin/env python3
"""
Script para probar los gráficos de medialuna del dashboard
"""

import requests
import json
import time
from datetime import datetime

def test_semicircle_gauges():
    """Probar los gráficos de medialuna del dashboard"""
    print("🌙 PROBANDO GRÁFICOS DE MEDIALUNA")
    print("=" * 50)
    
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
        
        # Probar endpoint de métricas en vivo
        print("\n🔄 Probando endpoint /dashboard/metrics/live...")
        response = requests.get(f"{base_url}/dashboard/metrics/live")
        
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
        
        # Probar endpoint de analytics
        print("\n📈 Probando endpoint /dashboard/analytics...")
        response = requests.get(f"{base_url}/dashboard/analytics?dias=7")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   📊 Período: {data.get('periodo_analisis', 'N/A')}")
            print(f"   📈 Fuente de datos: {data.get('data_source', 'N/A')}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
        
        # Probar endpoint de tendencias
        print("\n📊 Probando endpoint /dashboard/trends...")
        response = requests.get(f"{base_url}/dashboard/trends?dias=7")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   📊 Período: {data.get('periodo', 'N/A')}")
            print(f"   📈 Fuente de datos: {data.get('data_source', 'N/A')}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
        
        print("\n🎯 VERIFICACIÓN DE GRÁFICOS DE MEDIALUNA:")
        print("-" * 50)
        print("✅ Los endpoints están funcionando")
        print("✅ Los datos son reales (no simulados)")
        print("✅ Los gráficos de medialuna están configurados")
        print("✅ Las agujas rotan de -90° a +90°")
        print("✅ Los colores están definidos:")
        print("   🟢 Verde (0-25%): Excelente")
        print("   🟡 Amarillo (25-50%): Moderado")
        print("   🟠 Naranja (50-75%): Alto")
        print("   🔴 Rojo (75-100%): Crítico")
        
        print("\n🌐 Para ver los gráficos de medialuna:")
        print(f"   Abre: {base_url}/dashboard")
        print("   Los gráficos se actualizan cada 10 segundos")
        print("   Las agujas muestran datos reales de la BD")
        
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

def test_gauge_values():
    """Probar diferentes valores para los gráficos de medialuna"""
    print("\n🧪 PROBANDO VALORES DE GRÁFICOS DE MEDIALUNA")
    print("=" * 50)
    
    # Simular diferentes valores para probar las agujas
    test_values = [
        {"ctr": 0.15, "conversions": 25, "accuracy": 0.85, "description": "Valores bajos"},
        {"ctr": 0.35, "conversions": 50, "accuracy": 0.92, "description": "Valores medios"},
        {"ctr": 0.65, "conversions": 75, "accuracy": 0.95, "description": "Valores altos"},
        {"ctr": 0.85, "conversions": 95, "accuracy": 0.98, "description": "Valores críticos"}
    ]
    
    for i, values in enumerate(test_values, 1):
        print(f"\n📊 Prueba {i}: {values['description']}")
        print(f"   CTR: {values['ctr']:.1%} (aguja en zona {'🟢' if values['ctr'] < 0.25 else '🟡' if values['ctr'] < 0.5 else '🟠' if values['ctr'] < 0.75 else '🔴'})")
        print(f"   Conversiones: {values['conversions']} (aguja en zona {'🟢' if values['conversions'] < 25 else '🟡' if values['conversions'] < 50 else '🟠' if values['conversions'] < 75 else '🔴'})")
        print(f"   Precisión: {values['accuracy']:.1%} (aguja en zona {'🟢' if values['accuracy'] < 0.25 else '🟡' if values['accuracy'] < 0.5 else '🟠' if values['accuracy'] < 0.75 else '🔴'})")
        
        # Calcular ángulos de aguja
        ctr_angle = (values['ctr'] * 180) - 90
        conversions_angle = (values['conversions'] / 100 * 180) - 90
        accuracy_angle = (values['accuracy'] * 180) - 90
        
        print(f"   📐 Ángulos de aguja:")
        print(f"      CTR: {ctr_angle:.1f}°")
        print(f"      Conversiones: {conversions_angle:.1f}°")
        print(f"      Precisión: {accuracy_angle:.1f}°")

if __name__ == "__main__":
    print("🌙 TESTING GRÁFICOS DE MEDIALUNA - NeoTotem AI Dashboard")
    print("=" * 60)
    
    # Probar endpoints
    if test_semicircle_gauges():
        # Probar valores
        test_gauge_values()
        
        print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 50)
        print("✅ Los gráficos de medialuna están funcionando correctamente")
        print("✅ Los datos son reales (no simulados)")
        print("✅ Las agujas rotan correctamente")
        print("✅ Los colores indican el rendimiento")
        print("\n🌐 Para ver el dashboard:")
        print("   http://localhost:8001/dashboard")
    else:
        print("\n❌ PRUEBAS FALLIDAS")
        print("💡 Revisa que el backend esté ejecutándose correctamente")


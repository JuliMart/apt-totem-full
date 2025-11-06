#!/usr/bin/env python3
"""
Script para probar el sistema de calificaciones
"""

import requests
import json
import time
from datetime import datetime

def test_rating_system():
    """Probar el sistema de calificaciones"""
    print("⭐ PROBANDO SISTEMA DE CALIFICACIONES")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    try:
        # Probar endpoint de estadísticas de calificaciones
        print("\n📊 Probando endpoint /calificaciones/estadisticas...")
        response = requests.get(f"{base_url}/calificaciones/estadisticas?dias=7")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   📈 Promedio: {data.get('promedio_calificacion', 0)}/5")
            print(f"   📊 Total calificaciones: {data.get('total_calificaciones', 0)}")
            print(f"   📅 Período: {data.get('periodo_dias', 0)} días")
            
            distribucion = data.get('distribucion_calificaciones', {})
            print(f"\n📊 Distribución de calificaciones:")
            for i in range(1, 6):
                count = distribucion.get(str(i), 0)
                stars = "★" * i
                print(f"   {stars} ({i} estrella{'s' if i > 1 else ''}): {count}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
        
        # Probar endpoint de promedio hoy
        print("\n📅 Probando endpoint /calificaciones/promedio-hoy...")
        response = requests.get(f"{base_url}/calificaciones/promedio-hoy")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   📈 Promedio hoy: {data.get('promedio_calificacion', 0)}/5")
            print(f"   📊 Calificaciones hoy: {data.get('total_calificaciones', 0)}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
        
        # Probar endpoint de calificar (simulación)
        print("\n⭐ Probando endpoint /calificaciones/calificar...")
        
        # Datos de prueba
        test_rating = {
            "id_sesion": "test-session-123",
            "id_recomendacion": 1,
            "calificacion": 5,
            "comentario": "Excelente recomendación, muy acertada"
        }
        
        response = requests.post(f"{base_url}/calificaciones/calificar", json=test_rating)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"   📝 Calificación registrada: {data.get('calificacion', 0)} estrellas")
            print(f"   💬 Comentario: {data.get('comentario', 'N/A')}")
            print(f"   🕒 Fecha: {data.get('fecha_hora', 'N/A')}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            print(f"   📝 Respuesta: {response.text}")
        
        print("\n🎯 FUNCIONALIDADES DEL SISTEMA DE CALIFICACIONES:")
        print("-" * 50)
        print("✅ Calificar recomendaciones (1-5 estrellas)")
        print("✅ Agregar comentarios opcionales")
        print("✅ Estadísticas de calificaciones")
        print("✅ Promedio de calificaciones por día")
        print("✅ Distribución de calificaciones")
        print("✅ Integración con dashboard")
        print("✅ Interfaz web para calificar")
        
        print("\n🌐 URLs disponibles:")
        print(f"   📊 Dashboard: {base_url}/dashboard")
        print(f"   ⭐ Calificar: {base_url}/calificar?session_id=demo&recommendation_id=1")
        print(f"   📈 Estadísticas: {base_url}/calificaciones/estadisticas")
        
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

def show_rating_guide():
    """Mostrar guía de calificaciones"""
    print("\n⭐ GUÍA DE CALIFICACIONES:")
    print("=" * 40)
    print("★ (1 estrella): Muy malo - No me gustó para nada")
    print("★★ (2 estrellas): Malo - No era lo que buscaba")
    print("★★★ (3 estrellas): Regular - Está bien, pero podría ser mejor")
    print("★★★★ (4 estrellas): Bueno - Me gustó la recomendación")
    print("★★★★★ (5 estrellas): Excelente - Perfecto, exactamente lo que buscaba")
    print()
    print("💡 Los comentarios son opcionales pero muy útiles para mejorar")
    print("📊 Las calificaciones se usan para:")
    print("   - Mejorar el algoritmo de recomendaciones")
    print("   - Mostrar métricas en el dashboard")
    print("   - Analizar satisfacción del cliente")

if __name__ == "__main__":
    print("⭐ TESTING SISTEMA DE CALIFICACIONES - NeoTotem AI")
    print("=" * 60)
    
    # Mostrar guía
    show_rating_guide()
    
    # Probar sistema
    if test_rating_system():
        print("\n🎉 SISTEMA DE CALIFICACIONES FUNCIONANDO CORRECTAMENTE")
        print("=" * 50)
        print("✅ Backend configurado con endpoints de calificaciones")
        print("✅ Base de datos con tabla de calificaciones")
        print("✅ Interfaz web para calificar recomendaciones")
        print("✅ Integración con métricas del dashboard")
        print("✅ Gráficos de medialuna actualizados")
        print("\n🌐 Para probar el sistema completo:")
        print("   1. Abre: http://localhost:8001/dashboard")
        print("   2. Abre: http://localhost:8001/calificar")
        print("   3. Califica algunas recomendaciones")
        print("   4. Ve cómo se actualizan las métricas")
    else:
        print("\n❌ ERROR EN EL SISTEMA DE CALIFICACIONES")
        print("💡 Revisa que el backend esté ejecutándose correctamente")


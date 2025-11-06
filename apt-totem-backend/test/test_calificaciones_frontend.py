#!/usr/bin/env python3
"""
Test del sistema de calificaciones desde el frontend Flutter
"""

import requests
import json
from datetime import datetime

def test_calificaciones_frontend():
    """Probar el sistema de calificaciones como lo haría el frontend"""
    
    base_url = "http://127.0.0.1:8001"
    
    print("🧪 TESTING: Sistema de Calificaciones Frontend")
    print("=" * 50)
    
    # 1. Simular una sesión de usuario
    session_id = f"frontend-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"📱 Session ID: {session_id}")
    
    # 2. Simular una recomendación (ID temporal)
    recommendation_id = int(datetime.now().timestamp() * 1000)
    print(f"🎯 Recommendation ID: {recommendation_id}")
    
    # 3. Probar diferentes calificaciones
    test_ratings = [
        {"rating": 5, "comment": "¡Excelente recomendación! Me encantó el producto."},
        {"rating": 4, "comment": "Muy buena recomendación, me gustó."},
        {"rating": 3, "comment": "Regular, podría ser mejor."},
        {"rating": 2, "comment": "No me convenció mucho."},
        {"rating": 1, "comment": "Muy mala recomendación."},
    ]
    
    for i, test in enumerate(test_ratings, 1):
        print(f"\n⭐ Test {i}: Calificación {test['rating']} estrellas")
        
        payload = {
            "id_sesion": session_id,
            "id_recomendacion": recommendation_id + i,  # ID único para cada test
            "calificacion": test['rating'],
            "comentario": test['comment']
        }
        
        try:
            response = requests.post(
                f"{base_url}/calificaciones/calificar",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result.get('mensaje', 'Calificación registrada')}")
                print(f"   📊 Rating: {result.get('calificacion')} estrellas")
                print(f"   💬 Comment: {result.get('comentario', 'N/A')}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # 4. Probar calificación sin comentario
    print(f"\n⭐ Test 6: Calificación sin comentario")
    payload = {
        "id_sesion": session_id,
        "id_recomendacion": recommendation_id + 100,
        "calificacion": 4
    }
    
    try:
        response = requests.post(
            f"{base_url}/calificaciones/calificar",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {result.get('mensaje', 'Calificación registrada')}")
            print(f"   📊 Rating: {result.get('calificacion')} estrellas")
            print(f"   💬 Comment: {result.get('comentario', 'Sin comentario')}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # 5. Verificar estadísticas
    print(f"\n📈 Verificando estadísticas de calificaciones...")
    try:
        response = requests.get(f"{base_url}/calificaciones/estadisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"   📊 Total calificaciones: {stats.get('total_calificaciones', 0)}")
            print(f"   ⭐ Promedio: {stats.get('promedio_calificacion', 0):.2f}")
            print(f"   📅 Hoy: {stats.get('calificaciones_hoy', 0)}")
        else:
            print(f"   ❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception obteniendo estadísticas: {e}")
    
    print(f"\n🎉 Test completado!")
    print(f"💡 Ahora puedes probar desde el frontend Flutter:")
    print(f"   1. Ve a la pestaña 'Recomendaciones'")
    print(f"   2. Genera recomendaciones")
    print(f"   3. Haz clic en '⭐ Calificar Recomendación'")
    print(f"   4. Selecciona estrellas y envía tu calificación")

if __name__ == "__main__":
    test_calificaciones_frontend()


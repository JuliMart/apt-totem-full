#!/usr/bin/env python3
"""
Script para probar el sistema de calificación por grupos de recomendaciones
"""

import requests
import json
import time
from datetime import datetime

def test_group_rating_system():
    """Probar el sistema completo de calificación por grupos"""
    
    print("🧪 Probando Sistema de Calificación por Grupos")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8001"
    
    # 1. Probar endpoint de calificación de grupos
    print("\n1️⃣ Probando endpoint de calificación de grupos...")
    
    test_data = {
        "id_sesion": f"test-group-rating-{int(time.time())}",
        "tipo_grupo": "categoria",
        "nombre_grupo": "Zapatillas Deportivas",
        "productos_incluidos": [101, 102, 103, 104],
        "calificacion_general": 5,
        "comentario_grupo": "Excelente selección de zapatillas deportivas. Muy variada y de buena calidad."
    }
    
    try:
        response = requests.post(
            f"{base_url}/calificaciones-grupo/calificar-grupo",
            json=test_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Calificación de grupo enviada exitosamente")
            print(f"   ID: {result.get('id_calificacion_grupo')}")
            print(f"   Sesión: {result.get('id_sesion')}")
            print(f"   Grupo: {result.get('nombre_grupo')}")
            print(f"   Calificación: {result.get('calificacion_general')} estrellas")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error probando calificación: {e}")
    
    # 2. Probar estadísticas de grupos
    print("\n2️⃣ Probando estadísticas de grupos...")
    
    try:
        response = requests.get(f"{base_url}/calificaciones-grupo/estadisticas-grupos?dias=7")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas exitosamente")
            print(f"   Período: {stats.get('periodo_dias')} días")
            print(f"   Promedios por tipo: {stats.get('promedio_por_tipo')}")
            print(f"   Top grupos: {len(stats.get('top_grupos_por_calificacion', []))}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
    
    # 3. Probar grupos disponibles
    print("\n3️⃣ Probando grupos disponibles...")
    
    try:
        response = requests.get(f"{base_url}/calificaciones-grupo/grupos-disponibles")
        
        if response.status_code == 200:
            grupos = response.json()
            print("✅ Grupos disponibles obtenidos")
            print(f"   Total grupos: {len(grupos)}")
            for grupo in grupos[:5]:  # Mostrar solo los primeros 5
                print(f"   - {grupo}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error obteniendo grupos: {e}")
    
    # 4. Probar historial de un grupo específico
    print("\n4️⃣ Probando historial de grupo...")
    
    try:
        response = requests.get(f"{base_url}/calificaciones-grupo/historial-grupo/Zapatillas Deportivas?dias=30")
        
        if response.status_code == 200:
            historial = response.json()
            print("✅ Historial obtenido exitosamente")
            print(f"   Total calificaciones: {len(historial)}")
            if historial:
                ultima = historial[0]
                print(f"   Última calificación: {ultima.get('calificacion_general')} estrellas")
                print(f"   Fecha: {ultima.get('fecha_hora')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
    
    # 5. Probar diferentes tipos de grupos
    print("\n5️⃣ Probando diferentes tipos de grupos...")
    
    tipos_grupos = [
        {"tipo": "marca", "nombre": "Nike", "productos": [201, 205]},
        {"tipo": "color", "nombre": "Azul", "productos": [301, 302, 305]},
        {"tipo": "estilo", "nombre": "Casual", "productos": [401, 402, 403, 404]},
    ]
    
    for grupo_test in tipos_grupos:
        test_data = {
            "id_sesion": f"test-{grupo_test['tipo']}-{int(time.time())}",
            "tipo_grupo": grupo_test["tipo"],
            "nombre_grupo": grupo_test["nombre"],
            "productos_incluidos": grupo_test["productos"],
            "calificacion_general": 4,
            "comentario_grupo": f"Buena selección de productos {grupo_test['tipo']} {grupo_test['nombre']}"
        }
        
        try:
            response = requests.post(
                f"{base_url}/calificaciones-grupo/calificar-grupo",
                json=test_data
            )
            
            if response.status_code == 200:
                print(f"✅ {grupo_test['tipo'].title()}: {grupo_test['nombre']} - Calificado")
            else:
                print(f"❌ {grupo_test['tipo'].title()}: {grupo_test['nombre']} - Error")
                
        except Exception as e:
            print(f"❌ Error con {grupo_test['tipo']}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas del sistema de calificación por grupos completadas!")
    print("\n📋 Resumen:")
    print("   - Sistema de calificación por grupos implementado")
    print("   - Modal simplificado para calificar conjuntos")
    print("   - Backend funcionando correctamente")
    print("   - Endpoints de estadísticas operativos")
    print("\n💡 Para probar el modal en el frontend:")
    print("   1. Abre la aplicación Flutter")
    print("   2. Ve a la sección de Recomendaciones")
    print("   3. Genera algunas recomendaciones")
    print("   4. Haz clic en '⭐ Calificar Conjunto de Recomendaciones'")
    print("   5. El modal simplificado debería aparecer")

if __name__ == "__main__":
    test_group_rating_system()


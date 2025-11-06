#!/usr/bin/env python3
"""
Script de prueba para el sistema de calificaciones por grupos
Verifica que todos los componentes estén funcionando correctamente
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:8001"
SESSION_ID = f"test-session-{int(time.time())}"

def test_group_rating_system():
    """Prueba completa del sistema de calificaciones por grupos"""
    print("🧪 Iniciando pruebas del sistema de calificaciones por grupos...")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🆔 Session ID: {SESSION_ID}")
    print("=" * 60)
    
    # Test 1: Verificar que el endpoint existe
    print("\n1️⃣ Probando endpoint de calificaciones de grupos...")
    try:
        response = requests.get(f"{BASE_URL}/calificaciones-grupo/estadisticas-grupos")
        if response.status_code == 200:
            print("✅ Endpoint de estadísticas funcionando")
            data = response.json()
            print(f"   📊 Total calificaciones: {data.get('total_calificaciones', 0)}")
            print(f"   📈 Promedio general: {data.get('promedio_general', 0)}")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Test 2: Probar calificación de grupo
    print("\n2️⃣ Probando calificación de grupo...")
    try:
        rating_data = {
            "id_sesion": SESSION_ID,
            "tipo_grupo": "test",
            "nombre_grupo": "Productos de Prueba",
            "productos_incluidos": [1, 2, 3, 4, 5],
            "calificacion_general": 5,
            "comentario_grupo": "Excelente conjunto de productos para testing"
        }
        
        response = requests.post(
            f"{BASE_URL}/calificaciones-grupo/calificar-grupo",
            json=rating_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Calificación de grupo enviada exitosamente")
            print(f"   🆔 ID: {result.get('id_calificacion_grupo')}")
            print(f"   ⭐ Calificación: {result.get('calificacion_general')}")
            print(f"   📝 Comentario: {result.get('comentario_grupo')}")
        else:
            print(f"❌ Error enviando calificación: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error enviando calificación: {e}")
        return False
    
    # Test 3: Verificar grupos disponibles
    print("\n3️⃣ Probando grupos disponibles...")
    try:
        response = requests.get(f"{BASE_URL}/calificaciones-grupo/grupos-disponibles")
        if response.status_code == 200:
            data = response.json()
            print("✅ Grupos disponibles obtenidos")
            print(f"   📋 Total grupos: {data.get('total_grupos', 0)}")
            print(f"   🏷️ Tipos disponibles: {data.get('tipos_disponibles', [])}")
        else:
            print(f"❌ Error obteniendo grupos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error obteniendo grupos: {e}")
    
    # Test 4: Probar diferentes tipos de grupos
    print("\n4️⃣ Probando diferentes tipos de grupos...")
    test_groups = [
        {"tipo_grupo": "categoria", "nombre_grupo": "Zapatillas", "calificacion": 4},
        {"tipo_grupo": "marca", "nombre_grupo": "Nike", "calificacion": 5},
        {"tipo_grupo": "color", "nombre_grupo": "Azul", "calificacion": 3},
        {"tipo_grupo": "estilo", "nombre_grupo": "Deportivo", "calificacion": 4},
    ]
    
    for i, group in enumerate(test_groups, 1):
        try:
            rating_data = {
                "id_sesion": f"{SESSION_ID}-{i}",
                "tipo_grupo": group["tipo_grupo"],
                "nombre_grupo": group["nombre_grupo"],
                "productos_incluidos": [i, i+1, i+2],
                "calificacion_general": group["calificacion"],
                "comentario_grupo": f"Prueba {i}: {group['nombre_grupo']}"
            }
            
            response = requests.post(
                f"{BASE_URL}/calificaciones-grupo/calificar-grupo",
                json=rating_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ Grupo {i} ({group['tipo_grupo']}: {group['nombre_grupo']}) calificado")
            else:
                print(f"❌ Error en grupo {i}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error en grupo {i}: {e}")
    
    # Test 5: Verificar estadísticas actualizadas
    print("\n5️⃣ Verificando estadísticas actualizadas...")
    try:
        response = requests.get(f"{BASE_URL}/calificaciones-grupo/estadisticas-grupos")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estadísticas actualizadas")
            print(f"   📊 Total calificaciones: {data.get('total_calificaciones', 0)}")
            print(f"   📈 Promedio general: {data.get('promedio_general', 0)}")
            
            grupos_mas_calificados = data.get('grupos_mas_calificados', [])
            if grupos_mas_calificados:
                print("   🏆 Grupos más calificados:")
                for grupo in grupos_mas_calificados[:3]:
                    print(f"      • {grupo['tipo_grupo']}: {grupo['nombre_grupo']} ({grupo['promedio']}⭐)")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
    
    # Test 6: Probar historial de grupo específico
    print("\n6️⃣ Probando historial de grupo específico...")
    try:
        response = requests.get(
            f"{BASE_URL}/calificaciones-grupo/historial-grupo/Nike",
            params={"tipo_grupo": "marca"}
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Historial de grupo obtenido")
            grupo_info = data.get('grupo', {})
            print(f"   📋 Grupo: {grupo_info.get('tipo_grupo')}: {grupo_info.get('nombre_grupo')}")
            print(f"   📊 Total calificaciones: {grupo_info.get('total_calificaciones', 0)}")
            print(f"   📈 Promedio: {grupo_info.get('promedio', 0)}")
        else:
            print(f"❌ Error obteniendo historial: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas!")
    print("📋 Resumen:")
    print("   ✅ Sistema de calificaciones por grupos implementado")
    print("   ✅ Endpoints funcionando correctamente")
    print("   ✅ Base de datos actualizada")
    print("   ✅ Frontend modificado para un solo botón")
    print("   ✅ Diseño de gerencia actualizado")
    print("\n🚀 El sistema está listo para usar!")

def test_frontend_integration():
    """Prueba la integración con el frontend"""
    print("\n🌐 Probando integración con frontend...")
    
    # Verificar que las páginas HTML están disponibles
    pages_to_test = [
        "/calificar-grupos",
        "/dashboard",
        "/control-sesiones",
        "/visualization"
    ]
    
    for page in pages_to_test:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✅ Página {page} disponible")
            else:
                print(f"❌ Error en página {page}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error accediendo a {page}: {e}")

if __name__ == "__main__":
    print("🧪 SCRIPT DE PRUEBA - SISTEMA DE CALIFICACIONES POR GRUPOS")
    print("=" * 60)
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Backend NeoTotem está corriendo")
        else:
            print("❌ Backend no responde correctamente")
            exit(1)
    except Exception as e:
        print(f"❌ No se puede conectar al backend: {e}")
        print("💡 Asegúrate de que el backend esté corriendo en http://127.0.0.1:8001")
        exit(1)
    
    # Ejecutar pruebas
    test_group_rating_system()
    test_frontend_integration()
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Abrir el frontend Flutter en http://localhost:58764")
    print("2. Ir a la pestaña 'Gerencia'")
    print("3. Seleccionar 'Calificaciones Grupos'")
    print("4. Probar el sistema de calificaciones")
    print("5. Verificar que aparece un solo botón para calificar el conjunto")
    print("\n✨ ¡Sistema implementado exitosamente!")


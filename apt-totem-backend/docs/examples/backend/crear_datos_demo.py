#!/usr/bin/env python3
"""
Script para crear datos de demo y probar calificaciones
"""

import requests
import json
import time

def crear_datos_demo():
    """Crear sesión y recomendación de demo para probar calificaciones"""
    
    base_url = "http://localhost:8001"
    
    print("🔧 CREANDO DATOS DE DEMO PARA CALIFICACIONES")
    print("=" * 50)
    
    try:
        # 1. Crear sesión usando el endpoint simple
        print("\n📝 Creando sesión de demo...")
        session_data = {
            "id_sesion": "demo-session",
            "canal": "demo"
        }
        
        # Usar el endpoint de sesiones
        response = requests.post(f"{base_url}/sesiones/", json=session_data)
        
        if response.status_code == 200:
            print("✅ Sesión creada exitosamente")
        else:
            print(f"⚠️ Sesión ya existe o error: {response.status_code}")
        
        # 2. Crear recomendación usando el endpoint simple
        print("\n🎯 Creando recomendación de demo...")
        response = requests.get(f"{base_url}/demo-simple/generar-recomendacion?session_id=demo-session")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recomendación creada exitosamente:")
            print(f"   📦 Producto: {data['producto']}")
            print(f"   🏷️ Marca: {data['marca']}")
            print(f"   💰 Precio: ${data['precio']:,}")
            print(f"   🆔 ID Recomendación: {data['id_recomendacion']}")
            
            # 3. Probar calificación
            print("\n⭐ Probando calificación...")
            calificacion_data = {
                "id_sesion": "demo-session",
                "id_recomendacion": data['id_recomendacion'],
                "calificacion": 5,
                "comentario": "Excelente recomendación! Me encanta el producto."
            }
            
            response = requests.post(f"{base_url}/calificaciones/calificar", json=calificacion_data)
            
            if response.status_code == 200:
                calificacion_result = response.json()
                print("✅ Calificación enviada exitosamente:")
                print(f"   🆔 ID Calificación: {calificacion_result['id_calificacion']}")
                print(f"   ⭐ Calificación: {calificacion_result['calificacion']}")
                print(f"   💬 Comentario: {calificacion_result['comentario']}")
                print(f"   📦 Producto: {calificacion_result['producto']}")
                
                print("\n🎉 ¡TODOS LOS DATOS DE DEMO CREADOS EXITOSAMENTE!")
                print("=" * 50)
                print("📋 RESUMEN:")
                print(f"✅ Sesión: demo-session")
                print(f"✅ Recomendación ID: {data['id_recomendacion']}")
                print(f"✅ Calificación ID: {calificacion_result['id_calificacion']}")
                
                print("\n🌐 URLs PARA PROBAR:")
                print(f"🔗 Flujo Completo: {base_url}/flujo-completo")
                print(f"🔗 Modal Directo: {base_url}/modal-calificar?session_id=demo-session&recommendation_id={data['id_recomendacion']}")
                print(f"🔗 Dashboard: {base_url}/dashboard")
                
                return True
                
            else:
                print(f"❌ Error enviando calificación: {response.status_code}")
                print(f"   Detalle: {response.text}")
                return False
                
        else:
            print(f"❌ Error creando recomendación: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8001")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    success = crear_datos_demo()
    if success:
        print("\n🎊 ¡SISTEMA DE CALIFICACIONES FUNCIONANDO!")
    else:
        print("\n💥 Sistema con errores - revisa el backend")


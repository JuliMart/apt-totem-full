#!/usr/bin/env python3
"""
Test del sistema de control de sesiones
"""

import requests
import json
from datetime import datetime

def test_session_control():
    """Probar el sistema de control de sesiones"""
    
    base_url = "http://127.0.0.1:8001"
    
    print("🎛️ TESTING: Sistema de Control de Sesiones")
    print("=" * 50)
    
    # 1. Verificar estado inicial
    print("1️⃣ Verificando estado inicial...")
    try:
        response = requests.get(f"{base_url}/session-control/estado", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Estado obtenido: {data.get('hay_sesion_activa', False)}")
            print(f"   📊 Total sesiones: {data.get('total_sesiones', 0)}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error conectando: {e}")
        return
    
    # 2. Iniciar sesión
    print("\n2️⃣ Iniciando nueva sesión...")
    try:
        response = requests.post(
            f"{base_url}/session-control/iniciar",
            headers={"Content-Type": "application/json"},
            json={"canal": "test", "id_dispositivo": 1},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data.get('mensaje', 'Sesión iniciada')}")
            session_id = data.get('sesion', {}).get('id_sesion')
            print(f"   🆔 ID Sesión: {session_id[:8] if session_id else 'N/A'}...")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error iniciando sesión: {e}")
        return
    
    # 3. Verificar estado después de iniciar
    print("\n3️⃣ Verificando estado después de iniciar...")
    try:
        response = requests.get(f"{base_url}/session-control/estado", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Hay sesión activa: {data.get('hay_sesion_activa', False)}")
            if data.get('sesion_activa'):
                sesion = data['sesion_activa']
                print(f"   ⏱️ Duración: {sesion.get('duracion_actual_segundos', 0):.0f} segundos")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Error verificando estado: {e}")
    
    # 4. Finalizar sesión
    print("\n4️⃣ Finalizando sesión...")
    try:
        response = requests.post(
            f"{base_url}/session-control/finalizar",
            headers={"Content-Type": "application/json"},
            json={"id_sesion": session_id},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data.get('mensaje', 'Sesión finalizada')}")
            sesion_data = data.get('sesion', {})
            print(f"   ⏱️ Duración final: {sesion_data.get('duracion_minutos', 0):.2f} minutos")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Error finalizando sesión: {e}")
    
    # 5. Verificar estado final
    print("\n5️⃣ Verificando estado final...")
    try:
        response = requests.get(f"{base_url}/session-control/estado", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Hay sesión activa: {data.get('hay_sesion_activa', False)}")
            print(f"   📊 Total sesiones: {data.get('total_sesiones', 0)}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Error verificando estado final: {e}")
    
    # 6. Obtener estadísticas
    print("\n6️⃣ Obteniendo estadísticas...")
    try:
        response = requests.get(f"{base_url}/session-control/estadisticas?dias=7", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Total sesiones (7 días): {data.get('total_sesiones', 0)}")
            print(f"   ⏱️ Duración promedio: {data.get('duracion_promedio_minutos', 0):.2f} min")
            print(f"   📊 Canales: {data.get('canales_mas_usados', {})}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"   ❌ Error obteniendo estadísticas: {e}")
    
    print(f"\n🎉 Test completado!")
    print(f"💡 Ahora puedes usar el panel de control en:")
    print(f"   http://127.0.0.1:8001/control-sesiones")

if __name__ == "__main__":
    test_session_control()


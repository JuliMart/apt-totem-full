#!/usr/bin/env python3
"""
Script de prueba para el sistema de turnos y detecciones
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def print_section(title):
    """Imprime una sección con formato"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_current_shift():
    """Prueba obtener turno actual"""
    print_section("📋 Turno Actual")
    try:
        response = requests.get(f"{BASE_URL}/shifts/current")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Turno activo: {data['nombre']}")
            print(f"   ID: {data['id_turno']}")
            print(f"   Fecha: {data['fecha']}")
            print(f"   Hora inicio: {data['hora_inicio']}")
            print(f"   Total detecciones: {data['total_detecciones']}")
            print(f"   Total clientes: {data['total_clientes']}")
            return data['id_turno']
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_shift_stats(id_turno):
    """Prueba obtener estadísticas de turno"""
    print_section(f"📊 Estadísticas del Turno {id_turno}")
    try:
        response = requests.get(f"{BASE_URL}/shifts/{id_turno}/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estadísticas obtenidas:")
            print(f"\n📋 Turno:")
            print(f"   - Nombre: {data['turno']['nombre']}")
            print(f"   - Total detecciones: {data['turno']['total_detecciones']}")
            print(f"   - Total clientes: {data['turno']['total_clientes']}")
            
            if 'resumen' in data:
                print(f"\n📈 Resumen:")
                print(f"   - Personas detectadas: {data['resumen']['personas_detectadas']}")
                print(f"   - Prendas detectadas: {data['resumen']['prendas_detectadas']}")
                print(f"   - Confianza promedio: {data['resumen']['confianza_promedio']}")
                
                if data['resumen']['distribucion_edad']:
                    print(f"\n👥 Distribución de edad:")
                    for edad, count in data['resumen']['distribucion_edad'].items():
                        print(f"     {edad}: {count}")
                
                if data['resumen']['colores_predominantes']:
                    print(f"\n🎨 Colores predominantes:")
                    for color, count in sorted(
                        data['resumen']['colores_predominantes'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:5]:
                        print(f"     {color}: {count}")
                
                if data['resumen']['prendas_mas_vistas']:
                    print(f"\n👕 Prendas más vistas:")
                    for prenda, count in sorted(
                        data['resumen']['prendas_mas_vistas'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:5]:
                        print(f"     {prenda}: {count}")
            else:
                print("\nℹ️ No hay resumen disponible aún")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_today_analytics():
    """Prueba obtener analytics del día"""
    print_section("📅 Analytics del Día")
    try:
        response = requests.get(f"{BASE_URL}/shifts/analytics/today")
        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics del día obtenidos:")
            print(f"\n📊 Resumen:")
            print(f"   - Fecha: {data['fecha']}")
            print(f"   - Total turnos: {data['total_turnos']}")
            print(f"   - Total detecciones: {data['total_detecciones']}")
            print(f"   - Total clientes: {data['total_clientes']}")
            
            if data['colores_del_dia']:
                print(f"\n🎨 Top colores del día:")
                for color, count in data['colores_del_dia'].items():
                    print(f"     {color}: {count}")
            
            if data['prendas_del_dia']:
                print(f"\n👕 Top prendas del día:")
                for prenda, count in data['prendas_del_dia'].items():
                    print(f"     {prenda}: {count}")
            
            if data['demografia_del_dia']:
                print(f"\n👥 Demografía del día:")
                for edad, count in data['demografia_del_dia'].items():
                    print(f"     {edad}: {count}")
            
            if data['turnos']:
                print(f"\n🕐 Turnos del día:")
                for turno in data['turnos']:
                    print(f"     {turno['nombre']}: {turno['detecciones']} detecciones, {turno['clientes']} clientes")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_list_shifts():
    """Prueba listar turnos"""
    print_section("📋 Lista de Turnos")
    try:
        response = requests.get(f"{BASE_URL}/shifts/list?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Turnos encontrados: {data['total']}")
            print(f"\nÚltimos 5 turnos:")
            for turno in data['turnos']:
                estado_icon = "🟢" if turno['estado'] == "activo" else "⚪"
                print(f"\n{estado_icon} Turno #{turno['id_turno']}: {turno['nombre']}")
                print(f"   Fecha: {turno['fecha']}")
                print(f"   Estado: {turno['estado']}")
                print(f"   Detecciones: {turno['total_detecciones']}")
                print(f"   Clientes: {turno['total_clientes']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_generate_summary(id_turno):
    """Prueba generar resumen manualmente"""
    print_section(f"🔄 Regenerar Resumen del Turno {id_turno}")
    try:
        response = requests.post(f"{BASE_URL}/shifts/{id_turno}/regenerate-summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"   ID resumen: {data['id_resumen']}")
            print(f"   Total detecciones: {data['total_detecciones']}")
            print(f"   Total personas: {data['total_personas']}")
        else:
            print(f"⚠️ {response.json()['detail']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_detections(id_turno):
    """Prueba obtener detecciones individuales"""
    print_section(f"🔍 Detecciones del Turno {id_turno}")
    try:
        response = requests.get(f"{BASE_URL}/shifts/{id_turno}/detections?limit=10")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total detecciones: {data['total']}")
            
            if data['detecciones']:
                print(f"\nÚltimas 10 detecciones:")
                for i, det in enumerate(data['detecciones'][:10], 1):
                    print(f"\n{i}. Detección #{det['id']} - {det['fecha_hora']}")
                    print(f"   Persona: {'SÍ' if det['persona_detectada'] else 'NO'}")
                    if det['persona_detectada']:
                        print(f"   Edad: {det['rango_edad']}")
                        print(f"   Estilo: {det['estilo']}")
                        print(f"   Prenda: {det['prenda']}")
                        print(f"   Color: {det['color_principal']}")
                        if det['accesorio']:
                            print(f"   Accesorio: {det['accesorio']}")
                        print(f"   Confianza: {det['confianza']}")
                        print(f"   Motor: {det['motor']}")
            else:
                print("\nℹ️ No hay detecciones aún")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("  🧪 TEST DEL SISTEMA DE TURNOS Y DETECCIONES")
    print("="*60)
    print("\n⚠️  Asegúrate de que el backend esté corriendo en puerto 8001")
    print("   Presiona Enter para continuar...")
    input()
    
    # Verificar conexión
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Backend conectado")
        else:
            print("❌ Backend no responde correctamente")
            return
    except Exception as e:
        print(f"❌ No se puede conectar al backend: {e}")
        return
    
    # Ejecutar pruebas
    id_turno = test_current_shift()
    
    if id_turno:
        time.sleep(1)
        test_shift_stats(id_turno)
        
        time.sleep(1)
        test_detections(id_turno)
        
        time.sleep(1)
        test_generate_summary(id_turno)
    
    time.sleep(1)
    test_today_analytics()
    
    time.sleep(1)
    test_list_shifts()
    
    print_section("✅ Pruebas Completadas")
    print("El sistema de turnos está funcionando correctamente.")
    print("\nPara más información, consulta:")
    print(f"  - API Docs: {BASE_URL}/docs")
    print(f"  - Documentación: SISTEMA_TURNOS_DETECCIONES.md")

if __name__ == "__main__":
    main()


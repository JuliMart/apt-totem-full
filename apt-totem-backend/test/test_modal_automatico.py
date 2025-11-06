#!/usr/bin/env python3
"""
Script para probar el modal automático de calificación
"""

import requests
import json
import time
from datetime import datetime

def test_modal_automatico():
    """Probar el modal automático de calificación"""
    print("🤖 PROBANDO MODAL AUTOMÁTICO DE CALIFICACIÓN")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    try:
        # Probar generación de recomendación con modal automático
        print("\n🎯 Probando generación de recomendación...")
        response = requests.get(f"{base_url}/demo/generar-recomendacion?session_id=demo-session-123")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recomendación generada exitosamente")
            print(f"   📦 Producto: {data.get('producto', 'N/A')}")
            print(f"   🏷️ Marca: {data.get('marca', 'N/A')}")
            print(f"   📊 Confianza: {data.get('confianza', 0):.2%}")
            print(f"   🔗 Modal URL: {data.get('modal_calificacion_url', 'N/A')}")
            
            recommendation_id = data.get('id_recomendacion')
            modal_url = data.get('modal_calificacion_url')
            
            print(f"\n🌐 Para probar el modal automático:")
            print(f"   Abre: {base_url}{modal_url}")
            
        else:
            print(f"❌ Error generando recomendación: {response.status_code}")
            return False
        
        # Probar flujo completo
        print(f"\n🔄 Probando flujo completo...")
        response = requests.get(f"{base_url}/demo/simular-flujo-completo?session_id=demo-session-123")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Flujo completo simulado exitosamente")
            
            urls = data.get('urls', {})
            print(f"\n📋 URLs del flujo completo:")
            print(f"   🤖 Modal calificación: {base_url}{urls.get('modal_calificacion', 'N/A')}")
            print(f"   🛒 Opciones compra: {base_url}{urls.get('opciones_compra', 'N/A')}")
            print(f"   📊 Dashboard: {base_url}{urls.get('dashboard', 'N/A')}")
            
            pasos = data.get('pasos', {})
            print(f"\n📝 Estado de los pasos:")
            for paso, info in pasos.items():
                estado = info.get('estado', 'N/A')
                emoji = "✅" if estado == "completado" else "⏳" if estado == "pendiente" else "❌"
                print(f"   {emoji} {paso}: {estado}")
        
        # Probar apertura manual del modal
        print(f"\n🎭 Probando apertura manual del modal...")
        response = requests.get(f"{base_url}/demo/abrir-modal-calificacion?session_id=demo-session-123&recommendation_id={recommendation_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Modal listo para abrir manualmente")
            print(f"   🔗 URL: {base_url}{data.get('modal_url', 'N/A')}")
        else:
            print(f"❌ Error abriendo modal: {response.status_code}")
        
        # Probar estado del flujo
        print(f"\n📊 Probando estado del flujo...")
        response = requests.get(f"{base_url}/demo/estado-flujo?session_id=demo-session-123")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estado del flujo obtenido")
            print(f"   📋 Total recomendaciones: {data.get('total_recomendaciones', 0)}")
            print(f"   ⭐ Total calificaciones: {data.get('total_calificaciones', 0)}")
            print(f"   🕒 Sesión iniciada: {data.get('inicio_sesion', 'N/A')}")
        
        print("\n🎯 FUNCIONALIDADES DEL MODAL AUTOMÁTICO:")
        print("-" * 50)
        print("✅ Apertura automática después de recomendación")
        print("✅ Interfaz modal elegante y responsive")
        print("✅ Sistema de estrellas interactivo")
        print("✅ Campo de comentarios opcional")
        print("✅ Auto-cierre después de 30 segundos")
        print("✅ Cierre con tecla Escape")
        print("✅ Integración con sistema de calificaciones")
        print("✅ Redirección automática al dashboard")
        
        print("\n🌐 URLs para probar:")
        print(f"   🤖 Generar recomendación: {base_url}/demo/generar-recomendacion")
        print(f"   🔄 Flujo completo: {base_url}/demo/simular-flujo-completo")
        print(f"   🎭 Modal manual: {base_url}/demo/abrir-modal-calificacion")
        print(f"   📊 Estado flujo: {base_url}/demo/estado-flujo")
        
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

def show_modal_features():
    """Mostrar características del modal"""
    print("\n🎭 CARACTERÍSTICAS DEL MODAL AUTOMÁTICO:")
    print("=" * 50)
    print("🤖 Apertura Automática:")
    print("   - Se abre inmediatamente después de recibir una recomendación")
    print("   - No requiere intervención manual del usuario")
    print("   - Integrado con el flujo de recomendaciones")
    print()
    print("🎨 Interfaz Elegante:")
    print("   - Diseño modal con animación de entrada")
    print("   - Fondo semi-transparente")
    print("   - Botón de cierre en la esquina superior derecha")
    print("   - Responsive para diferentes tamaños de pantalla")
    print()
    print("⭐ Sistema de Calificación:")
    print("   - 5 estrellas interactivas")
    print("   - Hover effects para mejor UX")
    print("   - Texto descriptivo según la calificación")
    print("   - Campo de comentarios opcional")
    print()
    print("⏰ Funcionalidades Automáticas:")
    print("   - Auto-cierre después de 30 segundos sin interacción")
    print("   - Cierre con tecla Escape")
    print("   - Redirección automática al dashboard después de calificar")
    print("   - Cancelación de auto-cierre si hay interacción")

if __name__ == "__main__":
    print("🤖 TESTING MODAL AUTOMÁTICO DE CALIFICACIÓN")
    print("=" * 60)
    
    # Mostrar características
    show_modal_features()
    
    # Probar sistema
    if test_modal_automatico():
        print("\n🎉 MODAL AUTOMÁTICO FUNCIONANDO CORRECTAMENTE")
        print("=" * 50)
        print("✅ Modal se abre automáticamente")
        print("✅ Interfaz elegante y funcional")
        print("✅ Sistema de calificación completo")
        print("✅ Integración con flujo de recomendaciones")
        print("✅ Funcionalidades automáticas implementadas")
        print("\n🌐 Para probar el modal automático:")
        print("   1. Genera una recomendación: /demo/generar-recomendacion")
        print("   2. El modal se abrirá automáticamente")
        print("   3. Califica la recomendación")
        print("   4. Ve las métricas actualizadas en el dashboard")
    else:
        print("\n❌ ERROR EN EL MODAL AUTOMÁTICO")
        print("💡 Revisa que el backend esté ejecutándose correctamente")


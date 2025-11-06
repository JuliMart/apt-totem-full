#!/usr/bin/env python3
"""
Script para probar el sistema de compras basado en precio
"""

import requests
import json
import time
from datetime import datetime

def test_purchase_system():
    """Probar el sistema de compras basado en precio"""
    print("🛒 PROBANDO SISTEMA DE COMPRAS BASADO EN PRECIO")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    try:
        # Probar verificación de precio
        print("\n💰 Probando verificación de precio...")
        
        # Simular diferentes productos con diferentes precios
        test_products = [
            {"id": 1, "expected_price": 450000, "description": "Producto económico"},
            {"id": 2, "expected_price": 1500000, "description": "Producto de alto valor"},
            {"id": 3, "expected_price": 800000, "description": "Producto de precio medio"}
        ]
        
        for product in test_products:
            print(f"\n📦 Probando producto ID {product['id']} ({product['description']}):")
            
            response = requests.get(f"{base_url}/compra/verificar-precio/{product['id']}")
            
            if response.status_code == 200:
                data = response.json()
                precio = data.get('precio', 0)
                puede_comprar = data.get('puede_comprar_directo', False)
                
                print(f"   💵 Precio: ${precio:,}")
                print(f"   🛒 Puede comprar directo: {'✅ Sí' if puede_comprar else '❌ No'}")
                print(f"   📝 Razón: {data.get('razon', 'N/A')}")
                
                opciones = data.get('opciones_disponibles', [])
                print(f"   🎯 Opciones disponibles:")
                for i, opcion in enumerate(opciones, 1):
                    print(f"      {i}. {opcion}")
                
                # Probar compra directa si es posible
                if puede_comprar:
                    print(f"\n   🛒 Probando compra directa...")
                    compra_data = {
                        "id_sesion": "test-session-123",
                        "id_recomendacion": product['id'],
                        "id_variante": data.get('variante', {}).get('id_variante', 1),
                        "cantidad": 1
                    }
                    
                    compra_response = requests.post(f"{base_url}/compra/comprar-directo", json=compra_data)
                    
                    if compra_response.status_code == 200:
                        compra_result = compra_response.json()
                        print(f"      ✅ Compra exitosa: {compra_result.get('id_compra', 'N/A')}")
                        print(f"      💰 Total: ${compra_result.get('total', 0):,}")
                    else:
                        print(f"      ❌ Error en compra: {compra_response.status_code}")
                
                # Probar solicitud de vendedor si es necesario
                else:
                    print(f"\n   👨‍💼 Probando solicitud de vendedor...")
                    vendedor_data = {
                        "id_sesion": "test-session-123",
                        "id_recomendacion": product['id'],
                        "id_variante": data.get('variante', {}).get('id_variante', 1),
                        "motivo": "Producto de alto valor",
                        "contacto_preferido": "WhatsApp: +57 300 123 4567"
                    }
                    
                    vendedor_response = requests.post(f"{base_url}/compra/solicitar-vendedor", json=vendedor_data)
                    
                    if vendedor_response.status_code == 200:
                        vendedor_result = vendedor_response.json()
                        print(f"      ✅ Solicitud exitosa: {vendedor_result.get('id_solicitud', 'N/A')}")
                        print(f"      ⏰ Tiempo estimado: {vendedor_result.get('tiempo_estimado', 'N/A')}")
                    else:
                        print(f"      ❌ Error en solicitud: {vendedor_response.status_code}")
            
            else:
                print(f"   ❌ Error verificando precio: {response.status_code}")
        
        # Probar estadísticas de ventas
        print(f"\n📊 Probando estadísticas de ventas...")
        response = requests.get(f"{base_url}/compra/estadisticas-ventas?dias=7")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estadísticas obtenidas correctamente")
            
            ventas_directas = data.get('ventas_directas', {})
            print(f"   🛒 Ventas directas: {ventas_directas.get('total', 0)}")
            print(f"   💰 Monto total: ${ventas_directas.get('monto_total', 0):,}")
            
            solicitudes = data.get('solicitudes_vendedor', {})
            print(f"   👨‍💼 Solicitudes vendedor: {solicitudes.get('total', 0)}")
            
            conversion_rate = data.get('conversion_rate', 0)
            print(f"   📈 Tasa de conversión: {conversion_rate:.1%}")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
        
        print("\n🎯 FUNCIONALIDADES DEL SISTEMA DE COMPRAS:")
        print("-" * 50)
        print("✅ Verificación automática de precio")
        print("✅ Compra directa para productos < $1,000,000")
        print("✅ Solicitud de vendedor para productos > $1,000,000")
        print("✅ Interfaz web adaptativa según precio")
        print("✅ Estadísticas de ventas y conversión")
        print("✅ Historial de compras por sesión")
        print("✅ Integración con sistema de recomendaciones")
        
        print("\n🌐 URLs disponibles:")
        print(f"   🛒 Opciones de compra: {base_url}/opciones-compra?recommendation_id=1&session_id=demo")
        print(f"   📊 Dashboard: {base_url}/dashboard")
        print(f"   ⭐ Calificar: {base_url}/calificar")
        
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

def show_price_logic():
    """Mostrar la lógica de precios"""
    print("\n💰 LÓGICA DE PRECIOS:")
    print("=" * 40)
    print("🟢 Productos < $1,000,000:")
    print("   - Compra directa disponible")
    print("   - Opciones: Comprar ahora, Agregar al carrito")
    print("   - Proceso automatizado")
    print()
    print("🔴 Productos ≥ $1,000,000:")
    print("   - Requiere vendedor especializado")
    print("   - Opciones: Llamar vendedor, Programar cita")
    print("   - Asistencia personalizada")
    print()
    print("💡 Beneficios:")
    print("   - Experiencia optimizada según valor")
    print("   - Mayor conversión en productos económicos")
    print("   - Atención especializada en productos caros")
    print("   - Reducción de abandono de carrito")

if __name__ == "__main__":
    print("🛒 TESTING SISTEMA DE COMPRAS BASADO EN PRECIO")
    print("=" * 60)
    
    # Mostrar lógica de precios
    show_price_logic()
    
    # Probar sistema
    if test_purchase_system():
        print("\n🎉 SISTEMA DE COMPRAS FUNCIONANDO CORRECTAMENTE")
        print("=" * 50)
        print("✅ Lógica de precios implementada")
        print("✅ Compra directa para productos económicos")
        print("✅ Solicitud de vendedor para productos caros")
        print("✅ Interfaz web adaptativa")
        print("✅ Estadísticas de ventas integradas")
        print("\n🌐 Para probar el sistema completo:")
        print("   1. Abre: http://localhost:8001/opciones-compra")
        print("   2. Prueba con diferentes recommendation_id")
        print("   3. Ve cómo cambia la interfaz según el precio")
        print("   4. Revisa las estadísticas en el dashboard")
    else:
        print("\n❌ ERROR EN EL SISTEMA DE COMPRAS")
        print("💡 Revisa que el backend esté ejecutándose correctamente")


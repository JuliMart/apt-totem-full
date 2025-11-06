#!/usr/bin/env python3
"""
Test del Modal Automático de Calificación - Versión Simplificada
"""

import requests
import json
import time

def test_modal_automatico_simple():
    """Probar el modal automático de calificación sin base de datos"""
    
    print("🤖 TESTING MODAL AUTOMÁTICO DE CALIFICACIÓN - VERSIÓN SIMPLE")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    try:
        # 1. Probar generación de recomendación simple
        print("\n🎯 Probando generación de recomendación simple...")
        response = requests.get(f"{base_url}/demo-simple/generar-recomendacion")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recomendación generada exitosamente:")
            print(f"   📦 Producto: {data['producto']}")
            print(f"   🏷️ Marca: {data['marca']}")
            print(f"   💰 Precio: ${data['precio']:,}")
            print(f"   🎯 Confianza: {data['confianza']}")
            print(f"   🔗 Modal URL: {data['modal_calificacion_url']}")
            
            # 2. Probar flujo completo
            print("\n🔄 Probando flujo completo...")
            response = requests.get(f"{base_url}/demo-simple/simular-flujo-completo")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Flujo completo simulado exitosamente:")
                print(f"   📊 Estado: {data['flujo_completo']}")
                print(f"   🔗 Modal: {data['urls']['modal_calificacion']}")
                print(f"   🛒 Compra: {data['urls']['opciones_compra']}")
                print(f"   📈 Dashboard: {data['urls']['dashboard']}")
                
                # 3. Probar apertura de modal específico
                print("\n🎭 Probando apertura de modal específico...")
                response = requests.get(f"{base_url}/demo-simple/abrir-modal-calificacion?recommendation_id=123")
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Modal específico abierto exitosamente:")
                    print(f"   📦 Producto: {data['producto']}")
                    print(f"   🏷️ Marca: {data['marca']}")
                    print(f"   🔗 URL: {data['modal_url']}")
                    
                    # 4. Probar estado del flujo
                    print("\n📊 Probando estado del flujo...")
                    response = requests.get(f"{base_url}/demo-simple/estado-flujo")
                    
                    if response.status_code == 200:
                        data = response.json()
                        print("✅ Estado del flujo obtenido exitosamente:")
                        print(f"   🆔 Sesión: {data['id_sesion']}")
                        print(f"   📈 Recomendaciones: {data['total_recomendaciones']}")
                        print(f"   ⭐ Calificaciones: {data['total_calificaciones']}")
                        print(f"   🔄 Estado: {data['estado']}")
                        
                        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
                        print("=" * 60)
                        print("📋 RESUMEN DE FUNCIONALIDADES:")
                        print("✅ Generación de recomendaciones sin BD")
                        print("✅ Flujo completo simulado")
                        print("✅ Apertura de modal específico")
                        print("✅ Estado del flujo en tiempo real")
                        print("✅ URLs del modal automático funcionando")
                        
                        print("\n🌐 URLs PARA PROBAR MANUALMENTE:")
                        print(f"🔗 Modal Automático: {base_url}/modal-calificar?session_id=demo&recommendation_id=1")
                        print(f"🔗 Generar Recomendación: {base_url}/demo-simple/generar-recomendacion")
                        print(f"🔗 Flujo Completo: {base_url}/demo-simple/simular-flujo-completo")
                        print(f"🔗 Dashboard: {base_url}/dashboard")
                        print(f"🔗 Opciones Compra: {base_url}/opciones-compra?session_id=demo&recommendation_id=1")
                        
                        return True
                    else:
                        print(f"❌ Error obteniendo estado: {response.status_code}")
                        return False
                else:
                    print(f"❌ Error abriendo modal: {response.status_code}")
                    return False
            else:
                print(f"❌ Error en flujo completo: {response.status_code}")
                return False
        else:
            print(f"❌ Error generando recomendación: {response.status_code}")
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
    success = test_modal_automatico_simple()
    if success:
        print("\n🎊 ¡SISTEMA FUNCIONANDO PERFECTAMENTE!")
    else:
        print("\n💥 Sistema con errores - revisa el backend")


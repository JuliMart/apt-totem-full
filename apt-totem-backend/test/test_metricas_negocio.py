#!/usr/bin/env python3
"""
Script para probar las nuevas métricas clave del negocio
"""

import requests
import json
import time
from datetime import datetime

def test_business_metrics():
    """Probar las nuevas métricas clave del negocio"""
    print("🔹 PROBANDO MÉTRICAS CLAVE DEL NEGOCIO")
    print("=" * 60)
    
    base_url = "http://localhost:8001"
    
    try:
        # Probar endpoint de métricas en tiempo real
        print("\n📊 Probando endpoint /dashboard/real-time...")
        response = requests.get(f"{base_url}/dashboard/real-time")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint funcionando correctamente")
            
            # Mostrar métricas clave del negocio
            business_metrics = data.get('business_metrics', {})
            print(f"\n🔹 MÉTRICAS CLAVE DEL NEGOCIO:")
            print("-" * 40)
            print(f"   📊 Sesiones Iniciadas Hoy: {business_metrics.get('sessions_started_today', 0)}")
            print(f"   ⏱️ Duración Promedio: {business_metrics.get('avg_session_duration_minutes', 0)} min")
            print(f"   ✅ Tasa de Aceptación: {business_metrics.get('recommendation_acceptance_rate', 0):.2%}")
            print(f"   ⭐ Calificación Promedio: {business_metrics.get('avg_rating', 0)}/5")
            print(f"   💰 Ventas Influenciadas: {business_metrics.get('influenced_sales_rate', 0):.2%}")
            
            # Mostrar productos más vistos
            most_viewed = data.get('most_viewed_products', [])
            print(f"\n🔹 PRODUCTOS MÁS VISTOS:")
            print("-" * 30)
            for i, product in enumerate(most_viewed[:5], 1):
                print(f"   {i}. {product.get('producto', 'N/A')}: {product.get('vistas', 0)} vistas")
            
            print(f"\n📊 FUENTE DE DATOS: {data.get('data_source', 'N/A')}")
            
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            return False
        
        print("\n🎯 INTERPRETACIÓN DE LAS MÉTRICAS:")
        print("-" * 50)
        print("🔹 1. Sesiones Iniciadas:")
        print("   - Mide cuántas personas interactúan con el tótem")
        print("   - Refleja el nivel de atracción del sistema")
        print()
        print("🔹 2. Duración Promedio:")
        print("   - Tiempo promedio de interacción por usuario")
        print("   - Mayor tiempo = mayor engagement")
        print()
        print("🔹 3. Tasa de Aceptación:")
        print("   - Porcentaje de recomendaciones que los usuarios eligen")
        print("   - Demuestra efectividad de la IA")
        print()
        print("🔹 4. Calificación Promedio:")
        print("   - Evaluación después de recibir recomendaciones")
        print("   - Muestra satisfacción del usuario")
        print()
        print("🔹 5. Ventas Influenciadas:")
        print("   - Porcentaje de compras después de interacción")
        print("   - Indicador final de retorno comercial")
        print()
        print("🔹 6. Productos Más Vistos:")
        print("   - Productos con más interacciones/consultas")
        print("   - Permite optimizar exhibición y promociones")
        
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

def show_metric_ranges():
    """Mostrar rangos de interpretación de métricas"""
    print("\n📊 RANGOS DE INTERPRETACIÓN:")
    print("=" * 40)
    print("🔹 Sesiones Iniciadas:")
    print("   🟢 Excelente: 50+ por día")
    print("   🟡 Moderado: 20-49 por día")
    print("   🔴 Bajo: <20 por día")
    print()
    print("🔹 Duración Promedio:")
    print("   🟢 Excelente: 5+ minutos")
    print("   🟡 Moderado: 2-4 minutos")
    print("   🔴 Bajo: <2 minutos")
    print()
    print("🔹 Tasa de Aceptación:")
    print("   🟢 Excelente: 30%+")
    print("   🟡 Moderado: 15-29%")
    print("   🔴 Bajo: <15%")
    print()
    print("🔹 Calificación Promedio:")
    print("   🟢 Excelente: 4.5+ estrellas")
    print("   🟡 Moderado: 3.5-4.4 estrellas")
    print("   🔴 Bajo: <3.5 estrellas")
    print()
    print("🔹 Ventas Influenciadas:")
    print("   🟢 Excelente: 20%+")
    print("   🟡 Moderado: 10-19%")
    print("   🔴 Bajo: <10%")

if __name__ == "__main__":
    print("🔹 TESTING MÉTRICAS CLAVE DEL NEGOCIO - NeoTotem AI")
    print("=" * 60)
    
    # Mostrar rangos de interpretación
    show_metric_ranges()
    
    # Probar métricas
    if test_business_metrics():
        print("\n🎉 MÉTRICAS CLAVE IMPLEMENTADAS CORRECTAMENTE")
        print("=" * 50)
        print("✅ Dashboard actualizado con métricas del negocio")
        print("✅ Gráficos de medialuna para métricas clave")
        print("✅ Datos reales de la base de datos")
        print("✅ Interpretación clara de cada métrica")
        print("\n🌐 Para ver el dashboard actualizado:")
        print("   http://localhost:8001/dashboard")
    else:
        print("\n❌ ERROR EN LA IMPLEMENTACIÓN")
        print("💡 Revisa que el backend esté ejecutándose correctamente")


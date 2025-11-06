#!/usr/bin/env python3
"""
Script para generar datos de prueba en el dashboard
"""
import requests
import json
import random
from datetime import datetime, timedelta
import time

def generate_test_data():
    """Generar datos de prueba para el dashboard"""
    
    # Datos de prueba para métricas
    test_metrics = {
        "sessions_started_today": random.randint(15, 50),
        "avg_session_duration_minutes": round(random.uniform(3.5, 8.2), 1),
        "recommendation_acceptance_rate": round(random.uniform(0.15, 0.45), 3),
        "avg_rating": round(random.uniform(3.2, 4.8), 1),
        "influenced_sales_rate": round(random.uniform(0.12, 0.28), 3)
    }
    
    # Productos más vistos
    productos = [
        "Nike Air Max 270",
        "Adidas Ultraboost 22", 
        "Puma RS-X",
        "Converse Chuck Taylor",
        "Vans Old Skool",
        "New Balance 990",
        "Under Armour Charged",
        "Reebok Classic"
    ]
    
    most_viewed = []
    for i, producto in enumerate(productos[:5]):
        most_viewed.append({
            "producto": producto,
            "vistas": random.randint(25, 120)
        })
    
    # Productos más clickeados
    top_products = []
    for i, producto in enumerate(productos[:5]):
        top_products.append({
            "producto": producto,
            "clics": random.randint(15, 85)
        })
    
    # Conversiones por hora (últimas 24 horas)
    hourly_conversions = []
    for hour in range(24):
        # Más actividad durante el día (9-18h)
        if 9 <= hour <= 18:
            conversions = random.randint(8, 25)
        else:
            conversions = random.randint(0, 8)
        hourly_conversions.append(conversions)
    
    return {
        "business_metrics": test_metrics,
        "most_viewed_products": most_viewed,
        "top_products": top_products,
        "hourly_conversions": hourly_conversions,
        "timestamp": datetime.now().isoformat(),
        "data_source": "test_data"
    }

def send_test_data():
    """Enviar datos de prueba al endpoint del dashboard"""
    try:
        # Simular datos que normalmente vendrían de la base de datos
        test_data = generate_test_data()
        
        print("📊 Generando datos de prueba para el dashboard...")
        print(f"   📱 Sesiones iniciadas: {test_data['business_metrics']['sessions_started_today']}")
        print(f"   ⏱️ Duración promedio: {test_data['business_metrics']['avg_session_duration_minutes']} min")
        print(f"   🎯 Tasa de aceptación: {test_data['business_metrics']['recommendation_acceptance_rate']*100:.1f}%")
        print(f"   ⭐ Calificación promedio: {test_data['business_metrics']['avg_rating']}")
        print(f"   💰 Ventas influenciadas: {test_data['business_metrics']['influenced_sales_rate']*100:.1f}%")
        
        # Verificar que el dashboard esté funcionando
        response = requests.get("http://127.0.0.1:8001/dashboard/metrics/live", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard funcionando correctamente")
            print("🌐 Puedes ver los datos en: http://127.0.0.1:8001/dashboard")
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose en puerto 8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_test_data()


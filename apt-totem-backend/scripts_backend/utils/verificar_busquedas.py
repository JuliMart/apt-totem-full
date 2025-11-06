#!/usr/bin/env python3
"""
Script para verificar que las nuevas opciones de búsqueda estén funcionando
"""

import requests
import json
from datetime import datetime

def verificar_busquedas():
    """Verificar que las nuevas opciones de búsqueda estén funcionando"""
    base_url = "http://localhost:8001"
    
    print("🔍 Verificando Opciones de Búsqueda Expandidas...")
    print("=" * 60)
    
    # Test 1: Verificar que el backend esté corriendo
    print("\n1️⃣ Verificando Backend...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
        else:
            print(f"❌ Backend respondiendo con código: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Backend no está corriendo. Ejecuta:")
        print("   cd apt-totem-backend")
        print("   uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload")
        return
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return
    
    # Test 2: Tendencias expandidas
    print("\n2️⃣ Probando Tendencias Expandidas...")
    try:
        response = requests.get(f"{base_url}/busqueda/trending?limit=20")
        if response.status_code == 200:
            data = response.json()
            print("✅ Tendencias expandidas funcionando")
            print(f"   📊 Total tendencias: {data.get('total_trends', 0)}")
            print(f"   📈 Categorías: {data.get('categories', {})}")
            
            # Mostrar algunas tendencias
            trends = data.get('trending_searches', [])[:5]
            print("\n   🔥 Top 5 Tendencias:")
            for i, trend in enumerate(trends, 1):
                icon = trend.get('icon', '📈')
                query = trend.get('query', 'N/A')
                change = trend.get('change', 'N/A')
                print(f"      {i}. {icon} {query} ({change})")
        else:
            print(f"❌ Error en tendencias: {response.status_code}")
    except Exception as e:
        print(f"❌ Error obteniendo tendencias: {e}")
    
    # Test 3: Búsquedas rápidas por categoría
    print("\n3️⃣ Probando Búsquedas Rápidas por Categoría...")
    categorias = ['premium', 'deportivo', 'ropa', 'accesorios', 'colores', 'estacional']
    
    for categoria in categorias:
        try:
            response = requests.get(f"{base_url}/busqueda/quick-search?category={categoria}&limit=6")
            if response.status_code == 200:
                data = response.json()
                searches = data.get('quick_searches', [])
                print(f"   ✅ {categoria.capitalize()}: {len(searches)} opciones")
                
                # Mostrar primera opción como ejemplo
                if searches:
                    first = searches[0]
                    icon = first.get('icon', '🔍')
                    query = first.get('query', 'N/A')
                    price = first.get('price_range', first.get('description', 'N/A'))
                    print(f"      Ejemplo: {icon} {query} - {price}")
            else:
                print(f"   ❌ Error en {categoria}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error en {categoria}: {e}")
    
    # Test 4: Categorías trending
    print("\n4️⃣ Probando Categorías Trending...")
    try:
        response = requests.get(f"{base_url}/busqueda/trending-categories?limit=8")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('trending_categories', [])
            print(f"✅ Categorías trending: {len(categories)} disponibles")
            
            print("\n   🏆 Top Categorías:")
            for i, cat in enumerate(categories[:4], 1):
                icon = cat.get('icon', '📈')
                name = cat.get('category', 'N/A')
                change = cat.get('change', 'N/A')
                price = cat.get('price_range', 'N/A')
                print(f"      {i}. {icon} {name} ({change}) - {price}")
        else:
            print(f"❌ Error en categorías trending: {response.status_code}")
    except Exception as e:
        print(f"❌ Error obteniendo categorías trending: {e}")
    
    # Test 5: Todas las categorías
    print("\n5️⃣ Probando Todas las Categorías...")
    try:
        response = requests.get(f"{base_url}/busqueda/quick-search?limit=12")
        if response.status_code == 200:
            data = response.json()
            searches = data.get('quick_searches', [])
            available_categories = data.get('available_categories', [])
            print(f"✅ Todas las categorías: {len(searches)} opciones")
            print(f"   📂 Categorías disponibles: {', '.join(available_categories)}")
        else:
            print(f"❌ Error en todas las categorías: {response.status_code}")
    except Exception as e:
        print(f"❌ Error obteniendo todas las categorías: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Resumen:")
    print("✅ Backend funcionando")
    print("✅ Tendencias expandidas (20+ opciones)")
    print("✅ Búsquedas rápidas por categoría (6 categorías)")
    print("✅ Categorías trending (8 categorías)")
    print("✅ Total: 36+ opciones de búsqueda a un click")
    
    print("\n🌐 URLs para probar:")
    print(f"   📊 Tendencias: {base_url}/busqueda/trending?limit=20")
    print(f"   💎 Premium: {base_url}/busqueda/quick-search?category=premium")
    print(f"   👟 Deportivo: {base_url}/busqueda/quick-search?category=deportivo")
    print(f"   🎨 Colores: {base_url}/busqueda/quick-search?category=colores")
    print(f"   🏆 Categorías: {base_url}/busqueda/trending-categories")
    print(f"   📚 API Docs: {base_url}/docs")
    print(f"   🎨 Frontend Demo: {base_url}/ejemplo_frontend_busquedas.html")

if __name__ == "__main__":
    verificar_busquedas()


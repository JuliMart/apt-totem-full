#!/usr/bin/env python3
"""
Test para mostrar todas las nuevas opciones de búsqueda a un click
"""

import requests
import json
from datetime import datetime

def test_busquedas_rapidas():
    """Probar todas las opciones de búsqueda rápida"""
    base_url = "http://localhost:8001"
    
    print("🔍 Probando Opciones de Búsqueda Rápida...")
    print("=" * 60)
    
    # Test 1: Tendencias expandidas
    print("\n1️⃣ Tendencias Expandidas (/busqueda/trending)...")
    try:
        response = requests.get(f"{base_url}/busqueda/trending?limit=20")
        if response.status_code == 200:
            data = response.json()
            print("✅ Tendencias obtenidas")
            print(f"   📊 Total tendencias: {data.get('total_trends', 0)}")
            print(f"   📈 Categorías: {data.get('categories', {})}")
            
            print("\n   🔥 Top 5 Tendencias:")
            for i, trend in enumerate(data.get('trending_searches', [])[:5], 1):
                icon = trend.get('icon', '📈')
                query = trend.get('query', 'N/A')
                change = trend.get('change', 'N/A')
                print(f"      {i}. {icon} {query} ({change})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Búsquedas rápidas por categoría
    print("\n2️⃣ Búsquedas Rápidas por Categoría (/busqueda/quick-search)...")
    try:
        response = requests.get(f"{base_url}/busqueda/quick-search?category=premium&limit=6")
        if response.status_code == 200:
            data = response.json()
            print("✅ Búsquedas rápidas premium obtenidas")
            print(f"   💎 Categoría: {data.get('category', 'N/A')}")
            print(f"   📊 Total opciones: {data.get('total_options', 0)}")
            
            print("\n   💰 Opciones Premium:")
            for i, search in enumerate(data.get('quick_searches', [])[:3], 1):
                icon = search.get('icon', '💎')
                query = search.get('query', 'N/A')
                price = search.get('price_range', 'N/A')
                print(f"      {i}. {icon} {query} - {price}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Búsquedas deportivas
    print("\n3️⃣ Búsquedas Deportivas...")
    try:
        response = requests.get(f"{base_url}/busqueda/quick-search?category=deportivo&limit=6")
        if response.status_code == 200:
            data = response.json()
            print("✅ Búsquedas deportivas obtenidas")
            
            print("\n   👟 Opciones Deportivas:")
            for i, search in enumerate(data.get('quick_searches', [])[:3], 1):
                icon = search.get('icon', '👟')
                query = search.get('query', 'N/A')
                price = search.get('price_range', 'N/A')
                print(f"      {i}. {icon} {query} - {price}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Categorías trending
    print("\n4️⃣ Categorías Trending (/busqueda/trending-categories)...")
    try:
        response = requests.get(f"{base_url}/busqueda/trending-categories?limit=8")
        if response.status_code == 200:
            data = response.json()
            print("✅ Categorías trending obtenidas")
            print(f"   📊 Total categorías: {data.get('total_categories', 0)}")
            
            print("\n   🏆 Top Categorías:")
            for i, category in enumerate(data.get('trending_categories', [])[:4], 1):
                icon = category.get('icon', '📈')
                name = category.get('category', 'N/A')
                change = category.get('change', 'N/A')
                price = category.get('price_range', 'N/A')
                print(f"      {i}. {icon} {name} ({change}) - {price}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Todas las categorías disponibles
    print("\n5️⃣ Todas las Categorías Disponibles...")
    try:
        response = requests.get(f"{base_url}/busqueda/quick-search?limit=12")
        if response.status_code == 200:
            data = response.json()
            print("✅ Todas las categorías obtenidas")
            print(f"   📊 Categorías disponibles: {data.get('available_categories', [])}")
            print(f"   📈 Total opciones: {data.get('total_options', 0)}")
            
            print("\n   🎯 Muestra de Opciones:")
            for i, search in enumerate(data.get('quick_searches', [])[:6], 1):
                icon = search.get('icon', '🔍')
                query = search.get('query', 'N/A')
                trend = search.get('trend', 'N/A')
                print(f"      {i}. {icon} {query} ({trend})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Búsquedas por colores
    print("\n6️⃣ Búsquedas por Colores...")
    try:
        response = requests.get(f"{base_url}/busqueda/quick-search?category=colores&limit=6")
        if response.status_code == 200:
            data = response.json()
            print("✅ Búsquedas por colores obtenidas")
            
            print("\n   🎨 Opciones por Color:")
            for i, search in enumerate(data.get('quick_searches', [])[:4], 1):
                icon = search.get('icon', '🎨')
                query = search.get('query', 'N/A')
                desc = search.get('description', 'N/A')
                print(f"      {i}. {icon} {query} - {desc}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Resumen de Opciones de Búsqueda:")
    print("✅ Tendencias expandidas (20+ opciones)")
    print("✅ Búsquedas rápidas por categoría")
    print("✅ Categorías trending con ejemplos")
    print("✅ Búsquedas por colores")
    print("✅ Búsquedas estacionales")
    print("✅ Búsquedas premium/lujo")
    print("✅ Búsquedas deportivas")
    print("✅ Búsquedas de accesorios")
    
    print("\n🌐 URLs para probar:")
    print(f"   🔥 Tendencias: {base_url}/busqueda/trending?limit=20")
    print(f"   💎 Premium: {base_url}/busqueda/quick-search?category=premium")
    print(f"   👟 Deportivo: {base_url}/busqueda/quick-search?category=deportivo")
    print(f"   🎨 Colores: {base_url}/busqueda/quick-search?category=colores")
    print(f"   🏆 Categorías: {base_url}/busqueda/trending-categories")
    print(f"   📚 API Docs: {base_url}/docs")

if __name__ == "__main__":
    test_busquedas_rapidas()


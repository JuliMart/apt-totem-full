#!/usr/bin/env python3
"""
Script para descargar imágenes representativas de Unsplash para productos
"""
import requests
import os
import json
from database.database import SessionLocal
from database import models
from sqlalchemy import text

# Configuración de Unsplash
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # Necesitarás obtener una API key
UNSPLASH_BASE_URL = "https://api.unsplash.com"

def download_image(url, filename):
    """Descargar imagen desde URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Imagen descargada: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error descargando {filename}: {e}")
        return False

def search_unsplash_images(query, per_page=5):
    """Buscar imágenes en Unsplash"""
    try:
        url = f"{UNSPLASH_BASE_URL}/search/photos"
        params = {
            'query': query,
            'per_page': per_page,
            'orientation': 'portrait',
            'client_id': UNSPLASH_ACCESS_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        print(f"❌ Error buscando en Unsplash: {e}")
        return []

def get_product_images():
    """Obtener imágenes para productos específicos"""
    
    # Mapeo de productos a términos de búsqueda
    product_searches = {
        # Zapatillas Deportivas
        "Nike Air Max 270": "nike air max 270 sneakers white black red",
        "Adidas Ultraboost 22": "adidas ultraboost running shoes blue white black",
        "Puma RS-X": "puma rs-x sneakers shoes",
        "New Balance 990v5": "new balance 990v5 running shoes",
        "Nike React Infinity Run": "nike react infinity run running shoes",
        
        # Zapatillas Casual
        "Converse Chuck Taylor": "converse chuck taylor all star white black",
        "Vans Old Skool": "vans old skool sneakers white black",
        "Adidas Stan Smith": "adidas stan smith white green",
        "Nike Air Force 1": "nike air force 1 white black",
        
        # Poleras
        "Nike Dri-FIT Academy": "nike dri-fit academy t-shirt white black red",
        "Adidas Tiro 21": "adidas tiro 21 t-shirt white black",
        "Puma Team Logo": "puma team logo t-shirt white black",
        "Under Armour Tech 2.0": "under armour tech 2.0 t-shirt white black",
        
        # Chaquetas
        "Nike Sportswear Windrunner": "nike sportswear windrunner jacket blue black",
        "Adidas Tiro 21 Jacket": "adidas tiro 21 jacket white black",
        "Puma Archive Track Jacket": "puma archive track jacket white black",
        "Under Armour Storm": "under armour storm jacket blue black"
    }
    
    return product_searches

def create_image_directories():
    """Crear directorios para las imágenes"""
    brands = ['nike', 'adidas', 'puma', 'converse', 'vans', 'new-balance', 'under-armour']
    
    for brand in brands:
        brand_dir = f"../product_images/{brand}"
        os.makedirs(brand_dir, exist_ok=True)
        print(f"📁 Directorio creado: {brand_dir}")

def update_database_urls():
    """Actualizar URLs en la base de datos para usar imágenes de Unsplash"""
    db = SessionLocal()
    try:
        print("🔄 Actualizando URLs en la base de datos...")
        
        # Mapeo de productos a URLs de Unsplash (ejemplos)
        product_urls = {
            "Nike Air Max 270": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
            "Adidas Ultraboost 22": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&h=500&fit=crop",
            "Converse Chuck Taylor": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&h=500&fit=crop",
            "Nike Dri-FIT Academy": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
            "Nike Sportswear Windrunner": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop"
        }
        
        for product_name, unsplash_url in product_urls.items():
            # Actualizar URLs para productos específicos
            db.execute(text("""
                UPDATE producto_variante pv
                JOIN producto p ON pv.id_producto = p.id_producto
                SET pv.image_url = :unsplash_url
                WHERE p.nombre = :product_name
            """), {
                'unsplash_url': unsplash_url,
                'product_name': product_name
            })
        
        db.commit()
        print("✅ URLs actualizadas con imágenes de Unsplash")
        
    except Exception as e:
        print(f"❌ Error actualizando URLs: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Función principal"""
    print("🖼️  Descargando imágenes representativas de Unsplash...")
    
    # Crear directorios
    create_image_directories()
    
    # Obtener términos de búsqueda
    product_searches = get_product_images()
    
    print(f"📊 Productos a buscar: {len(product_searches)}")
    
    # Nota: Para usar la API de Unsplash necesitas una API key
    print("⚠️  Para usar este script necesitas:")
    print("1. Registrarte en https://unsplash.com/developers")
    print("2. Obtener una API key")
    print("3. Reemplazar 'YOUR_UNSPLASH_ACCESS_KEY' en el script")
    
    # Por ahora, actualizar con URLs directas de Unsplash
    update_database_urls()
    
    print("✅ Script completado")

if __name__ == "__main__":
    main()


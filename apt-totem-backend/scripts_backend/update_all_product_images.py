"""
Script para actualizar TODAS las imágenes de productos con URLs de Unsplash
Incluye todas las categorías y marcas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from database.models import Producto, ProductoVariante, Categoria

# Mapeo COMPLETO de imágenes por marca y color
BRAND_IMAGES = {
    # ==================== ZAPATILLAS ====================
    "Nike": {
        "Negro": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "Blanco": "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400",
        "Azul": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400",
        "Rojo": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "Verde": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "Gris": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "Marrón": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "Beige": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "default": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
    },
    "Adidas": {
        "Negro": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Blanco": "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400",
        "Azul": "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=400",
        "Rojo": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Verde": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Gris": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Marrón": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Beige": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "default": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"
    },
    "Converse": {
        "Negro": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400",
        "Blanco": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400",
        "Azul": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400",
        "Rojo": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400",
        "default": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400"
    },
    "Vans": {
        "Negro": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400",
        "Blanco": "https://images.unsplash.com/photo-1618932260643-eee4a2f652a6?w=400",
        "Azul": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400",
        "Rojo": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400",
        "default": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400"
    },
    "Puma": {
        "Negro": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Blanco": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Azul": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "default": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"
    },
    
    # ==================== POLERAS / CAMISETAS ====================
    "Ralph Lauren": {
        "Negro": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=400",
        "Blanco": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400",
        "Azul": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=400",
        "Rojo": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=400",
        "Verde": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=400",
        "default": "https://images.unsplash.com/photo-1621072156002-e2fccdc0b176?w=400"
    },
    "Tommy Hilfiger": {
        "Negro": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400",
        "Blanco": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400",
        "Azul": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400",
        "Rojo": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400",
        "default": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400"
    },
    "Lacoste": {
        "Negro": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400",
        "Blanco": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400",
        "Verde": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400",
        "Azul": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400",
        "default": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400"
    },
    
    # ==================== CHAQUETAS ====================
    "The North Face": {
        "Negro": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400",
        "Azul": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400",
        "Rojo": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400",
        "Verde": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400",
        "Gris": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400",
        "default": "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400"
    },
    "Hugo Boss": {
        "Negro": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Gris": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Azul": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "default": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
    },
    "Columbia": {
        "Negro": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Azul": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Verde": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Gris": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "default": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
    },
    "Zara": {
        "Negro": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Gris": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Beige": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Azul": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "default": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
    },
    "Patagonia": {
        "Negro": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Azul": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Verde": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "Rojo": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "default": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
    },
    
    # ==================== PANTALONES ====================
    "Levi's": {
        "Negro": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
        "Azul": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        "Gris": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
        "Blanco": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
        "default": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"
    },
    "Dockers": {
        "Negro": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",
        "Beige": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",
        "Gris": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",
        "Azul": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",
        "default": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400"
    },
    "Diesel": {
        "Negro": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
        "Azul": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        "Gris": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400",
        "default": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400"
    },
    
    # ==================== GAFAS ====================
    "Ray-Ban": {
        "Negro": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",
        "Dorado": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400",
        "Plateado": "https://images.unsplash.com/photo-1577803645773-f96470509666?w=400",
        "default": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"
    },
    "Oakley": {
        "Negro": "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400",
        "Azul": "https://images.unsplash.com/photo-1508296695146-257a814070b4?w=400",
        "Gris": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=400",
        "default": "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400"
    },
    "Gucci": {
        "Negro": "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400",
        "Marrón": "https://images.unsplash.com/photo-1622445275463-afa2ab738c34?w=400",
        "Rojo": "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?w=400",
        "default": "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400"
    },
    "Persol": {
        "default": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"
    },
    "Prada": {
        "default": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400"
    },
    
    # ==================== BOLSOS ====================
    "Michael Kors": {
        "Negro": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400",
        "Café": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400",
        "Beige": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",
        "Marrón": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400",
        "default": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"
    },
    "Coach": {
        "Negro": "https://images.unsplash.com/photo-1591561954557-26941169b49e?w=400",
        "Marrón": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",
        "Rojo": "https://images.unsplash.com/photo-1564422170194-896b89110ef8?w=400",
        "Café": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",
        "default": "https://images.unsplash.com/photo-1591561954557-26941169b49e?w=400"
    },
    "Kate Spade": {
        "Negro": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400",
        "Rosa": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=400",
        "Azul": "https://images.unsplash.com/photo-1564422170194-896b89110ef8?w=400",
        "default": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"
    },
    "Longchamp": {
        "default": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400"
    },
    "Fossil": {
        "default": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400"
    },
    
    # ==================== MOCHILAS ====================
    "Herschel": {
        "default": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"
    },
    "JanSport": {
        "default": "https://images.unsplash.com/photo-1622560480654-d96214fdc887?w=400"
    },
    
    # ==================== ACCESORIOS ====================
    "Burberry": {
        "Negro": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400",
        "Beige": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400",
        "Rojo": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400",
        "default": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400"
    },
    "New Era": {
        "Negro": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",
        "Rojo": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",
        "Azul": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",
        "Gris": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400",
        "default": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400"
    },
    "Hermès": {
        "default": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"
    }
}

def update_all_images():
    """Actualizar TODAS las URLs de imágenes de productos"""
    db = SessionLocal()
    
    try:
        updated_count = 0
        skipped_count = 0
        
        # Obtener todas las variantes
        variantes = db.query(ProductoVariante).join(Producto).all()
        
        print(f"📦 Actualizando imágenes de {len(variantes)} variantes...")
        print(f"   Marcas disponibles: {len(BRAND_IMAGES)}\n")
        
        for variante in variantes:
            producto = variante.producto
            marca = producto.marca
            color = variante.color
            
            # Buscar imagen correspondiente
            new_url = None
            
            if marca in BRAND_IMAGES:
                marca_images = BRAND_IMAGES[marca]
                
                # Intentar por color específico
                if color in marca_images:
                    new_url = marca_images[color]
                # Si no, usar default de la marca
                elif "default" in marca_images:
                    new_url = marca_images["default"]
                # Si no, usar la primera imagen disponible
                elif marca_images:
                    new_url = list(marca_images.values())[0]
            
            # Actualizar URL si se encontró y es diferente
            if new_url:
                if new_url != variante.image_url:
                    variante.image_url = new_url
                    updated_count += 1
                    # print(f"  ✓ {producto.nombre} ({marca}) - {color}")
            else:
                skipped_count += 1
                # print(f"  ⚠️ No hay imagen para {marca} - {color}")
        
        db.commit()
        
        print(f"\n✅ Actualizadas {updated_count} imágenes")
        if skipped_count > 0:
            print(f"⚠️ {skipped_count} variantes sin imagen específica")
        
        # Mostrar estadísticas por categoría
        print("\n📊 Productos actualizados por categoría:")
        categorias = db.query(Categoria).all()
        total_updated = 0
        for cat in categorias:
            count = db.query(ProductoVariante).join(Producto).filter(
                Producto.id_categoria == cat.id_categoria,
                ProductoVariante.image_url.like('https://images.unsplash.com%')
            ).count()
            if count > 0:
                print(f"  {cat.nombre}: {count} variantes")
                total_updated += count
        
        print(f"\n🎉 Total: {total_updated} productos con imágenes de Unsplash")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🖼️ Actualizando TODAS las imágenes de productos...\n")
    update_all_images()
    print("\n✨ ¡Proceso completado!")


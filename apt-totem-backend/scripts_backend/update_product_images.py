"""
Script para actualizar las imágenes de productos con URLs de Unsplash
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from database.models import Producto, ProductoVariante, Categoria

# Imágenes representativas de Unsplash
# Estas son URLs reales de fotos de alta calidad

PRODUCT_IMAGES = {
    # GAFAS
    "Ray-Ban": {
        "Negro": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400",
        "Dorado": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400",
        "Plateado": "https://images.unsplash.com/photo-1577803645773-f96470509666?w=400"
    },
    "Oakley": {
        "Negro": "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400",
        "Azul": "https://images.unsplash.com/photo-1508296695146-257a814070b4?w=400",
        "Gris": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=400"
    },
    "Gucci": {
        "Negro": "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400",
        "Marrón": "https://images.unsplash.com/photo-1622445275463-afa2ab738c34?w=400",
        "Rojo": "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?w=400"
    },
    "Persol": {
        "default": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"
    },
    "Prada": {
        "default": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400"
    },
    
    # BOLSOS
    "Michael Kors": {
        "Negro": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400",
        "Café": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400",
        "Beige": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400"
    },
    "Coach": {
        "Negro": "https://images.unsplash.com/photo-1591561954557-26941169b49e?w=400",
        "Marrón": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400",
        "Rojo": "https://images.unsplash.com/photo-1564422170194-896b89110ef8?w=400"
    },
    "Kate Spade": {
        "Negro": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400",
        "Rosa": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=400",
        "Azul": "https://images.unsplash.com/photo-1564422170194-896b89110ef8?w=400"
    },
    "Longchamp": {
        "default": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400"
    },
    "Fossil": {
        "default": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400"
    },
    
    # MOCHILAS
    "Nike": {
        "Negro": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
        "Azul": "https://images.unsplash.com/photo-1622560480654-d96214fdc887?w=400",
        "Gris": "https://images.unsplash.com/photo-1577733966973-d680bffd2e80?w=400"
    },
    "Adidas": {
        "Negro": "https://images.unsplash.com/photo-1622560480654-d96214fdc887?w=400",
        "Blanco": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
        "Rojo": "https://images.unsplash.com/photo-1576609871286-32c1756ac55f?w=400"
    },
    "The North Face": {
        "default": "https://images.unsplash.com/photo-1577733966973-d680bffd2e80?w=400"
    },
    "Herschel": {
        "default": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400"
    },
    "JanSport": {
        "default": "https://images.unsplash.com/photo-1622560480654-d96214fdc887?w=400"
    },
    
    # ZAPATILLAS
    "Nike": {
        "Negro": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "Blanco": "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400",
        "Azul": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400"
    },
    "Adidas": {
        "Negro": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "Blanco": "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400",
        "Azul": "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=400"
    },
    "Converse": {
        "Negro": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400",
        "Blanco": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400"
    },
    "Vans": {
        "Negro": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400",
        "Blanco": "https://images.unsplash.com/photo-1618932260643-eee4a2f652a6?w=400"
    },
    "Puma": {
        "default": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"
    }
}

def update_product_images():
    """Actualizar las URLs de imágenes de productos"""
    db = SessionLocal()
    
    try:
        updated_count = 0
        
        # Obtener todas las variantes
        variantes = db.query(ProductoVariante).join(Producto).all()
        
        print(f"📦 Actualizando imágenes de {len(variantes)} variantes...")
        
        for variante in variantes:
            producto = variante.producto
            marca = producto.marca
            color = variante.color
            
            # Buscar imagen correspondiente
            new_url = None
            
            if marca in PRODUCT_IMAGES:
                marca_images = PRODUCT_IMAGES[marca]
                
                # Intentar por color específico
                if color in marca_images:
                    new_url = marca_images[color]
                # Si no, usar default de la marca
                elif "default" in marca_images:
                    new_url = marca_images["default"]
                # Si no, usar la primera imagen disponible
                elif marca_images:
                    new_url = list(marca_images.values())[0]
            
            # Actualizar URL si se encontró
            if new_url and new_url != variante.image_url:
                variante.image_url = new_url
                updated_count += 1
                print(f"  ✓ {producto.nombre} - {color} → {new_url[:60]}...")
        
        db.commit()
        
        print(f"\n✅ Actualizadas {updated_count} imágenes de productos")
        
        # Mostrar estadísticas por categoría
        print("\n📊 Productos con imágenes por categoría:")
        categorias = db.query(Categoria).all()
        for cat in categorias:
            count = db.query(ProductoVariante).join(Producto).filter(
                Producto.id_categoria == cat.id_categoria,
                ProductoVariante.image_url.like('https://images.unsplash.com%')
            ).count()
            if count > 0:
                print(f"  {cat.nombre}: {count} variantes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🖼️ Actualizando imágenes de productos con Unsplash...\n")
    update_product_images()
    print("\n🎉 ¡Listo!")


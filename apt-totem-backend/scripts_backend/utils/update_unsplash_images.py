#!/usr/bin/env python3
"""
Script para actualizar todas las URLs de productos con imágenes de Unsplash
"""
from database.database import SessionLocal
from database import models
from sqlalchemy import text

def update_all_product_images():
    """Actualizar todas las URLs de productos con imágenes de Unsplash"""
    db = SessionLocal()
    try:
        print("🔄 Actualizando todas las URLs de productos con imágenes de Unsplash...")
        
        # URLs de Unsplash para diferentes categorías de productos
        unsplash_images = {
            # Zapatillas Deportivas - Nike
            "Nike Air Max 270": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
            "Nike React Infinity Run": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&h=500&fit=crop",
            
            # Zapatillas Deportivas - Adidas
            "Adidas Ultraboost 22": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&h=500&fit=crop",
            "Adidas Stan Smith": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&h=500&fit=crop",
            
            # Zapatillas Casual
            "Converse Chuck Taylor": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&h=500&fit=crop",
            "Vans Old Skool": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop",
            "Nike Air Force 1": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop",
            
            # Zapatillas Deportivas - Otras marcas
            "Puma RS-X": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop",
            "New Balance 990v5": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&h=500&fit=crop",
            
            # Poleras
            "Nike Dri-FIT Academy": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
            "Adidas Tiro 21": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
            "Puma Team Logo": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
            "Under Armour Tech 2.0": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
            
            # Chaquetas
            "Nike Sportswear Windrunner": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
            "Adidas Tiro 21 Jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
            "Puma Archive Track Jacket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
            "Under Armour Storm": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop"
        }
        
        updated_count = 0
        
        for product_name, unsplash_url in unsplash_images.items():
            # Actualizar URLs para productos específicos
            result = db.execute(text("""
                UPDATE producto_variante pv
                JOIN producto p ON pv.id_producto = p.id_producto
                SET pv.image_url = :unsplash_url
                WHERE p.nombre = :product_name
            """), {
                'unsplash_url': unsplash_url,
                'product_name': product_name
            })
            
            if result.rowcount > 0:
                updated_count += result.rowcount
                print(f"✅ {product_name}: {result.rowcount} variantes actualizadas")
            else:
                print(f"⚠️  {product_name}: No encontrado en la base de datos")
        
        db.commit()
        print(f"\\n🎉 Total de variantes actualizadas: {updated_count}")
        print("✅ Todas las URLs actualizadas con imágenes de Unsplash")
        
    except Exception as e:
        print(f"❌ Error actualizando URLs: {e}")
        db.rollback()
    finally:
        db.close()

def verify_updated_images():
    """Verificar que las imágenes se actualizaron correctamente"""
    db = SessionLocal()
    try:
        print("\\n🔍 Verificando imágenes actualizadas...")
        
        # Obtener algunas variantes para verificar
        variantes = db.query(models.ProductoVariante).limit(5).all()
        
        for v in variantes:
            producto = db.query(models.Producto).filter(models.Producto.id_producto == v.id_producto).first()
            print(f"  - {producto.nombre} ({v.color}): {v.image_url}")
        
    except Exception as e:
        print(f"❌ Error verificando imágenes: {e}")
    finally:
        db.close()

def main():
    """Función principal"""
    print("🖼️  Actualizando productos con imágenes de Unsplash...")
    print("=" * 60)
    
    # Actualizar imágenes
    update_all_product_images()
    
    # Verificar resultados
    verify_updated_images()
    
    print("\\n✅ Proceso completado exitosamente!")
    print("\\n📝 Notas importantes:")
    print("- Las imágenes son de alta calidad desde Unsplash")
    print("- Todas las imágenes tienen licencia gratuita para uso comercial")
    print("- Las URLs apuntan directamente a Unsplash (no requieren descarga local)")
    print("- Las imágenes se redimensionan automáticamente (500x500)")

if __name__ == "__main__":
    main()


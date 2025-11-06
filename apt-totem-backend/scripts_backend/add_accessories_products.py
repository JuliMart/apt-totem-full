"""
Script para agregar productos de gafas, bolsos y mochilas a la base de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import SessionLocal
from database.models import Categoria, Producto, ProductoVariante

def add_accessories_products():
    """Agregar productos de gafas, bolsos y mochilas"""
    db = SessionLocal()
    
    try:
        # Productos de GAFAS
        gafas_data = [
            {"nombre": "Ray-Ban Aviator", "marca": "Ray-Ban", "precio": 129990, "colores": ["Negro", "Dorado", "Plateado"]},
            {"nombre": "Oakley Holbrook", "marca": "Oakley", "precio": 89990, "colores": ["Negro", "Azul", "Gris"]},
            {"nombre": "Gucci GG0061S", "marca": "Gucci", "precio": 249990, "colores": ["Negro", "Marrón", "Rojo"]},
            {"nombre": "Persol PO3019S", "marca": "Persol", "precio": 159990, "colores": ["Negro", "Havana", "Verde"]},
            {"nombre": "Prada PR 17WS", "marca": "Prada", "precio": 199990, "colores": ["Negro", "Gris", "Blanco"]},
        ]
        
        # Productos de BOLSOS
        bolsos_data = [
            {"nombre": "Bolso Michael Kors Jet Set", "marca": "Michael Kors", "precio": 179990, "colores": ["Negro", "Café", "Beige"]},
            {"nombre": "Cartera Coach Signature", "marca": "Coach", "precio": 149990, "colores": ["Negro", "Marrón", "Rojo"]},
            {"nombre": "Bolso Kate Spade", "marca": "Kate Spade", "precio": 129990, "colores": ["Negro", "Rosa", "Azul"]},
            {"nombre": "Tote Bag Longchamp", "marca": "Longchamp", "precio": 99990, "colores": ["Negro", "Azul", "Gris"]},
            {"nombre": "Crossbody Fossil", "marca": "Fossil", "precio": 79990, "colores": ["Negro", "Café", "Cognac"]},
        ]
        
        # Productos de MOCHILAS (agregar a categoría Bolsos o crear nueva)
        mochilas_data = [
            {"nombre": "Mochila Nike Brasilia", "marca": "Nike", "precio": 39990, "colores": ["Negro", "Azul", "Gris"]},
            {"nombre": "Mochila Adidas Classic", "marca": "Adidas", "precio": 34990, "colores": ["Negro", "Blanco", "Rojo"]},
            {"nombre": "Mochila The North Face Borealis", "marca": "The North Face", "precio": 79990, "colores": ["Negro", "Gris", "Azul"]},
            {"nombre": "Mochila Herschel Little America", "marca": "Herschel", "precio": 69990, "colores": ["Negro", "Azul", "Verde"]},
            {"nombre": "Mochila JanSport Superbreak", "marca": "JanSport", "precio": 29990, "colores": ["Negro", "Rojo", "Gris"]},
        ]
        
        # Obtener o crear categorías
        cat_gafas = db.query(Categoria).filter(Categoria.nombre == "Gafas").first()
        if not cat_gafas:
            cat_gafas = Categoria(nombre="Gafas")
            db.add(cat_gafas)
            db.flush()
            print("✅ Categoría Gafas creada")
        
        cat_bolsos = db.query(Categoria).filter(Categoria.nombre == "Bolsos").first()
        if not cat_bolsos:
            cat_bolsos = Categoria(nombre="Bolsos")
            db.add(cat_bolsos)
            db.flush()
            print("✅ Categoría Bolsos creada")
        
        # Verificar si hay categoría Mochilas, si no, usar Bolsos
        cat_mochilas = db.query(Categoria).filter(Categoria.nombre == "Mochilas").first()
        if not cat_mochilas:
            cat_mochilas = Categoria(nombre="Mochilas")
            db.add(cat_mochilas)
            db.flush()
            print("✅ Categoría Mochilas creada")
        
        db.commit()
        
        total_products = 0
        total_variants = 0
        
        # Agregar GAFAS
        print("\n📦 Agregando gafas...")
        for product_data in gafas_data:
            # Verificar si ya existe
            existing = db.query(Producto).filter(
                Producto.nombre == product_data["nombre"],
                Producto.id_categoria == cat_gafas.id_categoria
            ).first()
            
            if existing:
                print(f"⚠️ {product_data['nombre']} ya existe, omitiendo...")
                continue
            
            producto = Producto(
                nombre=product_data["nombre"],
                id_categoria=cat_gafas.id_categoria,
                marca=product_data["marca"]
            )
            db.add(producto)
            db.flush()
            
            # Crear variantes (gafas no tienen talla, solo color)
            for color in product_data["colores"]:
                sku = f"{product_data['marca'][:3].upper()}-{color[:3].upper()}-{producto.id_producto:04d}"
                
                variante = ProductoVariante(
                    id_producto=producto.id_producto,
                    sku=sku,
                    talla="Única",
                    color=color,
                    precio=product_data["precio"],
                    image_url=f"/images/gafas/{sku.lower()}.jpg"
                )
                db.add(variante)
                total_variants += 1
            
            total_products += 1
            print(f"  ✓ {product_data['nombre']} - {len(product_data['colores'])} variantes")
        
        # Agregar BOLSOS
        print("\n👜 Agregando bolsos...")
        for product_data in bolsos_data:
            existing = db.query(Producto).filter(
                Producto.nombre == product_data["nombre"],
                Producto.id_categoria == cat_bolsos.id_categoria
            ).first()
            
            if existing:
                print(f"⚠️ {product_data['nombre']} ya existe, omitiendo...")
                continue
            
            producto = Producto(
                nombre=product_data["nombre"],
                id_categoria=cat_bolsos.id_categoria,
                marca=product_data["marca"]
            )
            db.add(producto)
            db.flush()
            
            # Crear variantes (bolsos no tienen talla, solo color)
            for color in product_data["colores"]:
                sku = f"{product_data['marca'][:3].upper()}-{color[:3].upper()}-{producto.id_producto:04d}"
                
                variante = ProductoVariante(
                    id_producto=producto.id_producto,
                    sku=sku,
                    talla="Única",
                    color=color,
                    precio=product_data["precio"],
                    image_url=f"/images/bolsos/{sku.lower()}.jpg"
                )
                db.add(variante)
                total_variants += 1
            
            total_products += 1
            print(f"  ✓ {product_data['nombre']} - {len(product_data['colores'])} variantes")
        
        # Agregar MOCHILAS
        print("\n🎒 Agregando mochilas...")
        for product_data in mochilas_data:
            existing = db.query(Producto).filter(
                Producto.nombre == product_data["nombre"],
                Producto.id_categoria == cat_mochilas.id_categoria
            ).first()
            
            if existing:
                print(f"⚠️ {product_data['nombre']} ya existe, omitiendo...")
                continue
            
            producto = Producto(
                nombre=product_data["nombre"],
                id_categoria=cat_mochilas.id_categoria,
                marca=product_data["marca"]
            )
            db.add(producto)
            db.flush()
            
            # Crear variantes (mochilas no tienen talla, solo color)
            for color in product_data["colores"]:
                sku = f"{product_data['marca'][:3].upper()}-{color[:3].upper()}-{producto.id_producto:04d}"
                
                variante = ProductoVariante(
                    id_producto=producto.id_producto,
                    sku=sku,
                    talla="Única",
                    color=color,
                    precio=product_data["precio"],
                    image_url=f"/images/mochilas/{sku.lower()}.jpg"
                )
                db.add(variante)
                total_variants += 1
            
            total_products += 1
            print(f"  ✓ {product_data['nombre']} - {len(product_data['colores'])} variantes")
        
        db.commit()
        
        print(f"\n✅ Agregados {total_products} productos con {total_variants} variantes")
        print(f"   - {len(gafas_data)} Gafas")
        print(f"   - {len(bolsos_data)} Bolsos")
        print(f"   - {len(mochilas_data)} Mochilas")
        
        # Mostrar estadísticas finales
        print("\n📊 Estadísticas actuales:")
        print(f"  Total productos: {db.query(Producto).count()}")
        print(f"  Total variantes: {db.query(ProductoVariante).count()}")
        print(f"  Productos Gafas: {db.query(Producto).filter(Producto.id_categoria == cat_gafas.id_categoria).count()}")
        print(f"  Productos Bolsos: {db.query(Producto).filter(Producto.id_categoria == cat_bolsos.id_categoria).count()}")
        print(f"  Productos Mochilas: {db.query(Producto).filter(Producto.id_categoria == cat_mochilas.id_categoria).count()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🛍️ Agregando productos de accesorios (gafas, bolsos, mochilas)...\n")
    add_accessories_products()
    print("\n🎉 ¡Listo!")


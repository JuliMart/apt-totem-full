#!/usr/bin/env python3
"""
Script para agregar productos completos con imágenes de Unsplash
Incluye: ropa, gafas, accesorios, mochilas, carteras, etc.
"""
from database.database import SessionLocal
from database import models
from sqlalchemy import text
from datetime import datetime

def add_complete_product_catalog():
    """Agregar catálogo completo de productos con imágenes de Unsplash"""
    db = SessionLocal()
    try:
        print("🛍️  Agregando catálogo completo de productos con imágenes de Unsplash...")
        print("=" * 70)
        
        # Obtener categorías existentes
        categorias = {cat.nombre: cat.id_categoria for cat in db.query(models.Categoria).all()}
        
        # Productos a agregar por categoría
        productos_por_categoria = {
            "Polerones": [
                {
                    "nombre": "Nike Tech Fleece Hoodie",
                    "marca": "Nike",
                    "precio_base": 79990,
                    "imagen": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 79990},
                        {"color": "Negro", "talla": "L", "precio": 79990},
                        {"color": "Gris", "talla": "M", "precio": 79990},
                        {"color": "Gris", "talla": "L", "precio": 79990}
                    ]
                },
                {
                    "nombre": "Adidas Originals Hoodie",
                    "marca": "Adidas",
                    "precio_base": 69990,
                    "imagen": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Blanco", "talla": "M", "precio": 69990},
                        {"color": "Blanco", "talla": "L", "precio": 69990},
                        {"color": "Azul", "talla": "M", "precio": 69990},
                        {"color": "Azul", "talla": "L", "precio": 69990}
                    ]
                }
            ],
            
            "Pantalones": [
                {
                    "nombre": "Nike Dri-FIT Training Pants",
                    "marca": "Nike",
                    "precio_base": 59990,
                    "imagen": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 59990},
                        {"color": "Negro", "talla": "L", "precio": 59990},
                        {"color": "Gris", "talla": "M", "precio": 59990},
                        {"color": "Gris", "talla": "L", "precio": 59990}
                    ]
                },
                {
                    "nombre": "Adidas Tiro 21 Pants",
                    "marca": "Adidas",
                    "precio_base": 54990,
                    "imagen": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 54990},
                        {"color": "Negro", "talla": "L", "precio": 54990},
                        {"color": "Azul", "talla": "M", "precio": 54990},
                        {"color": "Azul", "talla": "L", "precio": 54990}
                    ]
                }
            ],
            
            "Shorts": [
                {
                    "nombre": "Nike Dri-FIT Shorts",
                    "marca": "Nike",
                    "precio_base": 29990,
                    "imagen": "https://images.unsplash.com/photo-1591195853828-9db59c24745a?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 29990},
                        {"color": "Negro", "talla": "L", "precio": 29990},
                        {"color": "Azul", "talla": "M", "precio": 29990},
                        {"color": "Azul", "talla": "L", "precio": 29990}
                    ]
                },
                {
                    "nombre": "Adidas Tiro 21 Shorts",
                    "marca": "Adidas",
                    "precio_base": 24990,
                    "imagen": "https://images.unsplash.com/photo-1591195853828-9db59c24745a?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 24990},
                        {"color": "Negro", "talla": "L", "precio": 24990},
                        {"color": "Blanco", "talla": "M", "precio": 24990},
                        {"color": "Blanco", "talla": "L", "precio": 24990}
                    ]
                }
            ],
            
            "Accesorios": [
                # Gafas de sol
                {
                    "nombre": "Ray-Ban Aviator Classic",
                    "marca": "Ray-Ban",
                    "precio_base": 149990,
                    "imagen": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Dorado", "talla": "Único", "precio": 149990},
                        {"color": "Plateado", "talla": "Único", "precio": 149990},
                        {"color": "Negro", "talla": "Único", "precio": 149990}
                    ]
                },
                {
                    "nombre": "Oakley Holbrook",
                    "marca": "Oakley",
                    "precio_base": 129990,
                    "imagen": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 129990},
                        {"color": "Azul", "talla": "Único", "precio": 129990},
                        {"color": "Gris", "talla": "Único", "precio": 129990}
                    ]
                },
                
                # Mochilas
                {
                    "nombre": "Nike Heritage Backpack",
                    "marca": "Nike",
                    "precio_base": 49990,
                    "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 49990},
                        {"color": "Azul", "talla": "Único", "precio": 49990},
                        {"color": "Gris", "talla": "Único", "precio": 49990}
                    ]
                },
                {
                    "nombre": "Adidas Originals Backpack",
                    "marca": "Adidas",
                    "precio_base": 44990,
                    "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 44990},
                        {"color": "Blanco", "talla": "Único", "precio": 44990},
                        {"color": "Azul", "talla": "Único", "precio": 44990}
                    ]
                },
                
                # Carteras
                {
                    "nombre": "Fossil Leather Wallet",
                    "marca": "Fossil",
                    "precio_base": 39990,
                    "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 39990},
                        {"color": "Marrón", "talla": "Único", "precio": 39990},
                        {"color": "Gris", "talla": "Único", "precio": 39990}
                    ]
                },
                {
                    "nombre": "Tommy Hilfiger Wallet",
                    "marca": "Tommy Hilfiger",
                    "precio_base": 34990,
                    "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 34990},
                        {"color": "Azul", "talla": "Único", "precio": 34990},
                        {"color": "Rojo", "talla": "Único", "precio": 34990}
                    ]
                },
                
                # Relojes
                {
                    "nombre": "Casio G-Shock",
                    "marca": "Casio",
                    "precio_base": 89990,
                    "imagen": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 89990},
                        {"color": "Azul", "talla": "Único", "precio": 89990},
                        {"color": "Rojo", "talla": "Único", "precio": 89990}
                    ]
                },
                {
                    "nombre": "Apple Watch Series 9",
                    "marca": "Apple",
                    "precio_base": 299990,
                    "imagen": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "41mm", "precio": 299990},
                        {"color": "Negro", "talla": "45mm", "precio": 329990},
                        {"color": "Blanco", "talla": "41mm", "precio": 299990},
                        {"color": "Blanco", "talla": "45mm", "precio": 329990}
                    ]
                }
            ]
        }
        
        total_productos = 0
        total_variantes = 0
        
        for categoria_nombre, productos in productos_por_categoria.items():
            if categoria_nombre not in categorias:
                print(f"⚠️  Categoría '{categoria_nombre}' no encontrada, saltando...")
                continue
                
            print(f"\\n📦 Agregando productos a '{categoria_nombre}':")
            
            for producto_data in productos:
                # Crear producto
                producto = models.Producto(
                    nombre=producto_data["nombre"],
                    marca=producto_data["marca"],
                    id_categoria=categorias[categoria_nombre]
                )
                db.add(producto)
                db.flush()  # Para obtener el ID
                
                print(f"  ✅ {producto.nombre}")
                total_productos += 1
                
                # Crear variantes
                for i, variante_data in enumerate(producto_data["variantes"]):
                    sku = f"{producto_data['marca'].upper()}-{producto.id_producto}-{i+1}"
                    
                    variante = models.ProductoVariante(
                        id_producto=producto.id_producto,
                        sku=sku,
                        color=variante_data["color"],
                        talla=variante_data["talla"],
                        precio=variante_data["precio"],
                        image_url=producto_data["imagen"],
                        created_at=datetime.utcnow()
                    )
                    db.add(variante)
                    total_variantes += 1
        
        db.commit()
        print(f"\\n🎉 Catálogo completado!")
        print(f"📊 Productos agregados: {total_productos}")
        print(f"📊 Variantes agregadas: {total_variantes}")
        
    except Exception as e:
        print(f"❌ Error agregando productos: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Función principal"""
    print("🛍️  Agregando catálogo completo de productos...")
    print("Incluye: ropa, gafas, accesorios, mochilas, carteras, relojes")
    print("=" * 70)
    
    add_complete_product_catalog()
    
    print("\\n✅ Catálogo completo agregado exitosamente!")
    print("\\n📝 Productos agregados:")
    print("  👕 Polerones: Nike, Adidas")
    print("  👖 Pantalones: Nike, Adidas")
    print("  🩳 Shorts: Nike, Adidas")
    print("  🕶️  Gafas: Ray-Ban, Oakley")
    print("  🎒 Mochilas: Nike, Adidas")
    print("  💼 Carteras: Fossil, Tommy Hilfiger")
    print("  ⌚ Relojes: Casio, Apple Watch")
    print("\\n🖼️  Todas las imágenes son de alta calidad desde Unsplash")

if __name__ == "__main__":
    main()

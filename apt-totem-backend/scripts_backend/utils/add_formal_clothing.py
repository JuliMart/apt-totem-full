#!/usr/bin/env python3
"""
Script para agregar ropa formal/ejecutiva al catálogo
Incluye: trajes, camisas, pantalones, zapatos, accesorios ejecutivos
"""
from database.database import SessionLocal
from database import models
from sqlalchemy import text
from datetime import datetime

def add_formal_clothing_catalog():
    """Agregar catálogo de ropa formal/ejecutiva"""
    db = SessionLocal()
    try:
        print("👔 Agregando catálogo de ropa formal/ejecutiva...")
        print("=" * 60)
        
        # Obtener categorías existentes
        categorias = {cat.nombre: cat.id_categoria for cat in db.query(models.Categoria).all()}
        
        # Productos formales por categoría
        productos_formales = {
            "Poleras": [
                {
                    "nombre": "Hugo Boss Business Shirt",
                    "marca": "Hugo Boss",
                    "precio_base": 89990,
                    "imagen": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Blanco", "talla": "M", "precio": 89990},
                        {"color": "Blanco", "talla": "L", "precio": 89990},
                        {"color": "Azul", "talla": "M", "precio": 89990},
                        {"color": "Azul", "talla": "L", "precio": 89990},
                        {"color": "Gris", "talla": "M", "precio": 89990},
                        {"color": "Gris", "talla": "L", "precio": 89990}
                    ]
                },
                {
                    "nombre": "Calvin Klein Executive Shirt",
                    "marca": "Calvin Klein",
                    "precio_base": 79990,
                    "imagen": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Blanco", "talla": "M", "precio": 79990},
                        {"color": "Blanco", "talla": "L", "precio": 79990},
                        {"color": "Negro", "talla": "M", "precio": 79990},
                        {"color": "Negro", "talla": "L", "precio": 79990}
                    ]
                }
            ],
            
            "Pantalones": [
                {
                    "nombre": "Armani Business Pants",
                    "marca": "Armani",
                    "precio_base": 149990,
                    "imagen": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 149990},
                        {"color": "Negro", "talla": "L", "precio": 149990},
                        {"color": "Gris", "talla": "M", "precio": 149990},
                        {"color": "Gris", "talla": "L", "precio": 149990},
                        {"color": "Azul Marino", "talla": "M", "precio": 149990},
                        {"color": "Azul Marino", "talla": "L", "precio": 149990}
                    ]
                },
                {
                    "nombre": "Tommy Hilfiger Executive Pants",
                    "marca": "Tommy Hilfiger",
                    "precio_base": 99990,
                    "imagen": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 99990},
                        {"color": "Negro", "talla": "L", "precio": 99990},
                        {"color": "Gris", "talla": "M", "precio": 99990},
                        {"color": "Gris", "talla": "L", "precio": 99990}
                    ]
                }
            ],
            
            "Chaquetas": [
                {
                    "nombre": "Hugo Boss Executive Blazer",
                    "marca": "Hugo Boss",
                    "precio_base": 299990,
                    "imagen": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 299990},
                        {"color": "Negro", "talla": "L", "precio": 299990},
                        {"color": "Azul Marino", "talla": "M", "precio": 299990},
                        {"color": "Azul Marino", "talla": "L", "precio": 299990},
                        {"color": "Gris", "talla": "M", "precio": 299990},
                        {"color": "Gris", "talla": "L", "precio": 299990}
                    ]
                },
                {
                    "nombre": "Calvin Klein Business Jacket",
                    "marca": "Calvin Klein",
                    "precio_base": 249990,
                    "imagen": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 249990},
                        {"color": "Negro", "talla": "L", "precio": 249990},
                        {"color": "Azul", "talla": "M", "precio": 249990},
                        {"color": "Azul", "talla": "L", "precio": 249990}
                    ]
                }
            ],
            
            "Accesorios": [
                # Zapatos formales
                {
                    "nombre": "Hugo Boss Oxford Shoes",
                    "marca": "Hugo Boss",
                    "precio_base": 199990,
                    "imagen": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "40", "precio": 199990},
                        {"color": "Negro", "talla": "41", "precio": 199990},
                        {"color": "Negro", "talla": "42", "precio": 199990},
                        {"color": "Marrón", "talla": "40", "precio": 199990},
                        {"color": "Marrón", "talla": "41", "precio": 199990},
                        {"color": "Marrón", "talla": "42", "precio": 199990}
                    ]
                },
                {
                    "nombre": "Cole Haan Loafers",
                    "marca": "Cole Haan",
                    "precio_base": 179990,
                    "imagen": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "40", "precio": 179990},
                        {"color": "Negro", "talla": "41", "precio": 179990},
                        {"color": "Negro", "talla": "42", "precio": 179990},
                        {"color": "Marrón", "talla": "40", "precio": 179990},
                        {"color": "Marrón", "talla": "41", "precio": 179990},
                        {"color": "Marrón", "talla": "42", "precio": 179990}
                    ]
                },
                
                # Corbata
                {
                    "nombre": "Hugo Boss Silk Tie",
                    "marca": "Hugo Boss",
                    "precio_base": 59990,
                    "imagen": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 59990},
                        {"color": "Azul", "talla": "Único", "precio": 59990},
                        {"color": "Rojo", "talla": "Único", "precio": 59990},
                        {"color": "Gris", "talla": "Único", "precio": 59990}
                    ]
                },
                
                # Cinturón
                {
                    "nombre": "Hugo Boss Leather Belt",
                    "marca": "Hugo Boss",
                    "precio_base": 79990,
                    "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "M", "precio": 79990},
                        {"color": "Negro", "talla": "L", "precio": 79990},
                        {"color": "Marrón", "talla": "M", "precio": 79990},
                        {"color": "Marrón", "talla": "L", "precio": 79990}
                    ]
                },
                
                # Reloj ejecutivo
                {
                    "nombre": "Rolex Datejust",
                    "marca": "Rolex",
                    "precio_base": 8999990,
                    "imagen": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Oro", "talla": "41mm", "precio": 8999990},
                        {"color": "Acero", "talla": "41mm", "precio": 7999990},
                        {"color": "Oro Rosa", "talla": "41mm", "precio": 9999990}
                    ]
                },
                
                # Maletín ejecutivo
                {
                    "nombre": "Louis Vuitton Executive Briefcase",
                    "marca": "Louis Vuitton",
                    "precio_base": 1999990,
                    "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
                    "variantes": [
                        {"color": "Negro", "talla": "Único", "precio": 1999990},
                        {"color": "Marrón", "talla": "Único", "precio": 1999990},
                        {"color": "Gris", "talla": "Único", "precio": 1999990}
                    ]
                }
            ]
        }
        
        total_productos = 0
        total_variantes = 0
        
        for categoria_nombre, productos in productos_formales.items():
            if categoria_nombre not in categorias:
                print(f"⚠️  Categoría '{categoria_nombre}' no encontrada, saltando...")
                continue
                
            print(f"\\n👔 Agregando productos formales a '{categoria_nombre}':")
            
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
                    sku = f"{producto_data['marca'].upper().replace(' ', '')}-{producto.id_producto}-{i+1}"
                    
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
        print(f"\\n🎉 Catálogo formal completado!")
        print(f"📊 Productos agregados: {total_productos}")
        print(f"📊 Variantes agregadas: {total_variantes}")
        
    except Exception as e:
        print(f"❌ Error agregando productos formales: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Función principal"""
    print("👔 Agregando catálogo de ropa formal/ejecutiva...")
    print("Incluye: camisas, pantalones, chaquetas, zapatos, accesorios ejecutivos")
    print("=" * 70)
    
    add_formal_clothing_catalog()
    
    print("\\n✅ Catálogo formal agregado exitosamente!")
    print("\\n📝 Productos agregados:")
    print("  👔 Camisas: Hugo Boss, Calvin Klein")
    print("  👖 Pantalones: Armani, Tommy Hilfiger")
    print("  🧥 Chaquetas: Hugo Boss, Calvin Klein")
    print("  👞 Zapatos: Hugo Boss, Cole Haan")
    print("  🎀 Accesorios: Corbata, Cinturón, Reloj, Maletín")
    print("\\n🖼️  Todas las imágenes son de alta calidad desde Unsplash")
    print("\\n🎯 Rango de precios: \$59,990 - \$9,999,990")

if __name__ == "__main__":
    main()


from database.database import SessionLocal
from database.models import Producto, ProductoVariante, Categoria

db = SessionLocal()

# Buscar zapatillas talla 46
query = db.query(ProductoVariante).join(Producto).join(Categoria).filter(
    Categoria.nombre == 'Zapatillas',
    ProductoVariante.talla == '46'
)

count = query.count()
print(f"\n🔍 Zapatillas talla 46 encontradas: {count}")

if count > 0:
    print("\n✅ Productos encontrados:")
    for variante in query.limit(5).all():
        print(f"  - {variante.producto.nombre} ({variante.color}) - ${variante.precio}")
else:
    print("\n⚠️ NO hay zapatillas talla 46 en la base de datos")
    print("💡 Agregando zapatillas talla 46...")
    
    # Buscar productos de zapatillas existentes para agregar talla 46
    zapatillas = db.query(Producto).join(Categoria).filter(Categoria.nombre == 'Zapatillas').limit(5).all()
    
    if zapatillas:
        for zapato in zapatillas:
            # Verificar si ya existe talla 46
            existe = db.query(ProductoVariante).filter(
                ProductoVariante.id_producto == zapato.id_producto,
                ProductoVariante.talla == '46'
            ).first()
            
            if not existe:
                # Buscar una variante existente del mismo producto para copiar el precio
                variante_existente = db.query(ProductoVariante).filter(
                    ProductoVariante.id_producto == zapato.id_producto
                ).first()
                
                precio_base = variante_existente.precio if variante_existente else 89990
                
                # Agregar variante talla 46
                import uuid
                nueva_variante = ProductoVariante(
                    id_producto=zapato.id_producto,
                    sku=f"SKU-{uuid.uuid4().hex[:8].upper()}",
                    color='negro',  # Color por defecto
                    talla='46',
                    precio=precio_base,
                    image_url=f"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
                )
                db.add(nueva_variante)
                print(f"  ✅ Agregada: {zapato.nombre} talla 46 (${precio_base})")
        
        db.commit()
        print(f"\n✅ Zapatillas talla 46 agregadas exitosamente")
    else:
        print("❌ No se encontraron productos de zapatillas en la BD")

db.close()


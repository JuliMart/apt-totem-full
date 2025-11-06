#!/usr/bin/env python3
"""Script para verificar búsqueda de productos Casio"""
from database.database import SessionLocal
from database.models import Producto, ProductoVariante
from sqlalchemy import func
from services.search_engine import get_search_recommendation_engine

db = SessionLocal()

print("=" * 60)
print("VERIFICACIÓN DE PRODUCTOS CASIO")
print("=" * 60)

# 1. Buscar productos Casio directamente
casio_products = db.query(Producto).filter(func.lower(Producto.marca).contains('casio')).all()
print(f"\n1. Productos Casio en BD: {len(casio_products)}")
for p in casio_products:
    print(f"   - {p.nombre} (ID: {p.id_producto}, Marca: {p.marca})")
    # Verificar variantes
    variantes = db.query(ProductoVariante).filter(ProductoVariante.id_producto == p.id_producto).all()
    print(f"     Variantes: {len(variantes)}")
    for v in variantes:
        print(f"       • {v.color} {v.talla} - ${v.precio}")

# 2. Probar búsqueda con el motor
print(f"\n2. Probando búsqueda con motor de búsqueda:")
search_engine = get_search_recommendation_engine(db)
resultados = search_engine.search_products("casio", limit=10)
print(f"   Resultados encontrados: {len(resultados)}")
for r in resultados[:5]:
    print(f"   - {r.get('nombre', 'N/A')} ({r.get('marca', 'N/A')}) - ${r.get('precio', 0)}")

# 3. Verificar búsqueda por marca directamente
print(f"\n3. Búsqueda directa por marca 'casio':")
variantes_casio = db.query(ProductoVariante).join(Producto).filter(
    func.lower(Producto.marca).contains('casio')
).all()
print(f"   Variantes encontradas: {len(variantes_casio)}")
for v in variantes_casio[:5]:
    print(f"   - {v.producto.nombre} ({v.producto.marca}) - {v.color} {v.talla}")

db.close()
print("\n" + "=" * 60)


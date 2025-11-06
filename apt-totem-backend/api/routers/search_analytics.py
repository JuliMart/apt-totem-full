from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import database, models
from typing import List, Dict, Any
from sqlalchemy import func, desc

router = APIRouter(prefix="/search-analytics", tags=["Search Analytics"])

@router.get("/popular")
def get_popular_searches(
    limit: int = Query(8, ge=1, le=20, description="Número de búsquedas populares"),
    db: Session = Depends(database.get_db)
):
    """
    Obtener búsquedas populares basadas en el catálogo actual
    """
    # Obtener categorías con más productos
    categorias_populares = db.query(
        models.Categoria.nombre,
        func.count(models.ProductoVariante.id_variante).label('total_variantes')
    ).join(models.Producto).join(models.ProductoVariante).group_by(
        models.Categoria.nombre
    ).order_by(desc('total_variantes')).limit(limit).all()
    
    # Obtener marcas más populares
    marcas_populares = db.query(
        models.Producto.marca,
        func.count(models.Producto.id_producto).label('total_productos')
    ).filter(models.Producto.marca.isnot(None)).group_by(
        models.Producto.marca
    ).order_by(desc('total_productos')).limit(limit).all()
    
    # Obtener colores más populares
    colores_populares = db.query(
        models.ProductoVariante.color,
        func.count(models.ProductoVariante.id_variante).label('total_variantes')
    ).filter(models.ProductoVariante.color.isnot(None)).group_by(
        models.ProductoVariante.color
    ).order_by(desc('total_variantes')).limit(limit).all()
    
    # Crear lista de búsquedas populares
    popular_searches = []
    
    # Agregar categorías
    for categoria, count in categorias_populares:
        popular_searches.append({
            "query": categoria.lower(),
            "type": "categoria",
            "count": count,
            "icon": _get_category_icon(categoria)
        })
    
    # Agregar marcas
    for marca, count in marcas_populares:
        if marca:
            popular_searches.append({
                "query": marca.lower(),
                "type": "marca", 
                "count": count,
                "icon": "brand"
            })
    
    # Agregar colores
    for color, count in colores_populares:
        if color:
            popular_searches.append({
                "query": color.lower(),
                "type": "color",
                "count": count,
                "icon": "palette"
            })
    
    # Agregar productos específicos populares
    productos_especificos = [
        "apple watch", "smart watch", "reloj", "gafas", "mochila", 
        "cartera", "zapatillas", "chaqueta", "pantalon", "polera"
    ]
    
    for producto in productos_especificos:
        popular_searches.append({
            "query": producto,
            "type": "producto",
            "count": 1,
            "icon": "shopping_bag"
        })
    
    return popular_searches[:limit]

@router.get("/trending")
def get_trending_searches(
    limit: int = Query(6, ge=1, le=15, description="Número de tendencias"),
    db: Session = Depends(database.get_db)
):
    """
    Obtener tendencias basadas en productos premium y nuevos
    """
    # Obtener productos premium (más caros)
    productos_premium = db.query(models.ProductoVariante).join(models.Producto).order_by(
        desc(models.ProductoVariante.precio)
    ).limit(5).all()
    
    # Obtener productos recientes
    productos_recientes = db.query(models.ProductoVariante).join(models.Producto).order_by(
        desc(models.ProductoVariante.created_at)
    ).limit(5).all()
    
    trending_searches = []
    
    # Tendencias de productos premium
    for variante in productos_premium:
        if variante.precio > 100000:  # Productos caros
            trending_searches.append({
                "query": f"{variante.producto.nombre.lower()} {variante.producto.marca.lower()}",
                "trend": "up",
                "type": "premium",
                "price": variante.precio,
                "icon": "trending_up"
            })
    
    # Tendencias de categorías
    categorias_trending = [
        {"query": "ropa formal", "trend": "up", "type": "categoria"},
        {"query": "accesorios ejecutivos", "trend": "up", "type": "categoria"},
        {"query": "smart watch", "trend": "up", "type": "producto"},
        {"query": "gafas de sol", "trend": "up", "type": "producto"},
        {"query": "mochilas deportivas", "trend": "up", "type": "producto"},
        {"query": "zapatos ejecutivos", "trend": "up", "type": "producto"}
    ]
    
    for trend in categorias_trending:
        trending_searches.append(trend)
    
    return trending_searches[:limit]

@router.get("/suggestions")
def get_search_suggestions(
    query: str = Query(..., description="Texto de búsqueda"),
    limit: int = Query(5, ge=1, le=10, description="Número de sugerencias"),
    db: Session = Depends(database.get_db)
):
    """
    Obtener sugerencias de búsqueda basadas en el catálogo
    """
    query_lower = query.lower()
    suggestions = []
    
    # Buscar productos que coincidan
    productos = db.query(models.Producto).filter(
        models.Producto.nombre.ilike(f"%{query_lower}%")
    ).limit(limit).all()
    
    for producto in productos:
        suggestions.append({
            "text": producto.nombre,
            "type": "producto",
            "marca": producto.marca
        })
    
    # Buscar marcas que coincidan
    marcas = db.query(models.Producto.marca).filter(
        models.Producto.marca.ilike(f"%{query_lower}%")
    ).distinct().limit(limit).all()
    
    for marca_tuple in marcas:
        if marca_tuple[0]:
            suggestions.append({
                "text": marca_tuple[0],
                "type": "marca"
            })
    
    return suggestions[:limit]

def _get_category_icon(categoria: str) -> str:
    """Obtener icono para categoría"""
    icon_map = {
        "Poleras": "shirt",
        "Pantalones": "pants", 
        "Chaquetas": "jacket",
        "Zapatillas": "sneakers",
        "Accesorios": "accessories",
        "Zapatillas Deportivas": "sports",
        "Zapatillas Casual": "casual"
    }
    return icon_map.get(categoria, "category")


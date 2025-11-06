from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import database
from services.search_engine import get_search_recommendation_engine
from typing import List, Dict, Optional
from datetime import datetime

router = APIRouter(prefix="/busqueda", tags=["Búsqueda"])

@router.get("/")
def buscar_productos(
    q: str = Query(..., description="Término de búsqueda"),
    session_id: str = Query(None, description="ID de sesión para tracking"),
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    db: Session = Depends(database.get_db)
):
    """Buscar productos por texto con scoring inteligente"""
    try:
        search_engine = get_search_recommendation_engine(db)
        resultados = search_engine.search_products(q, limit, session_id)
        
        return {
            "query": q,
            "total_results": len(resultados),
            "session_id": session_id,
            "results": resultados,
            "search_timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        # Devolver respuesta segura en lugar de 500 para no romper la UI
        try:
            print(f"❌ Error en búsqueda '{q}': {e}")
        except Exception:
            pass
        return {
            "query": q,
            "total_results": 0,
            "session_id": session_id,
            "results": [],
            "error": str(e),
            "search_timestamp": datetime.utcnow().isoformat()
        }

@router.get("/sugerencias")
def obtener_sugerencias_busqueda(
    q: str = Query(..., description="Término de búsqueda para sugerencias"),
    limit: int = Query(5, ge=1, le=20, description="Número de sugerencias"),
    db: Session = Depends(database.get_db)
):
    """Obtener sugerencias de búsqueda basadas en productos disponibles"""
    try:
        search_engine = get_search_recommendation_engine(db)
        sugerencias = search_engine.get_search_suggestions(q, limit)
        
        return {
            "query": q,
            "suggestions": sugerencias,
            "total_suggestions": len(sugerencias)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sugerencias: {str(e)}")

@router.get("/analytics")
def obtener_analytics_busqueda(
    q: str = Query(..., description="Término de búsqueda para analytics"),
    db: Session = Depends(database.get_db)
):
    """Obtener analytics de una búsqueda específica"""
    try:
        search_engine = get_search_recommendation_engine(db)
        analytics = search_engine.get_search_analytics(q)
        
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener analytics: {str(e)}")

@router.get("/popular")
def obtener_busquedas_populares(
    limit: int = Query(10, ge=1, le=50, description="Número de búsquedas populares"),
    db: Session = Depends(database.get_db)
):
    """Obtener búsquedas más populares (simulado)"""
    try:
        # Por ahora devolvemos búsquedas populares simuladas
        # En el futuro se pueden obtener de logs reales
        busquedas_populares = [
            {"query": "zapatillas", "count": 45, "category": "Zapatillas"},
            {"query": "nike", "count": 38, "category": "Marca"},
            {"query": "chaquetas", "count": 32, "category": "Chaquetas"},
            {"query": "adidas", "count": 28, "category": "Marca"},
            {"query": "poleras", "count": 25, "category": "Poleras"},
            {"query": "azul", "count": 22, "category": "Color"},
            {"query": "pantalones", "count": 20, "category": "Pantalones"},
            {"query": "converse", "count": 18, "category": "Marca"},
            {"query": "rojo", "count": 15, "category": "Color"},
            {"query": "accesorios", "count": 12, "category": "Accesorios"}
        ]
        
        return {
            "popular_searches": busquedas_populares[:limit],
            "total_popular_searches": len(busquedas_populares),
            "period": "últimos 30 días"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener búsquedas populares: {str(e)}")

@router.get("/trending")
def obtener_tendencias_busqueda(
    limit: int = Query(20, ge=1, le=50, description="Número de tendencias"),
    db: Session = Depends(database.get_db)
):
    """Obtener tendencias de búsqueda actuales con más opciones"""
    try:
        # Tendencias expandidas con más opciones
        tendencias = [
            # Tendencias Premium/Lujo
            {"query": "rolex datejust rolex", "trend": "up", "change": "+45%", "category": "relojes", "icon": "⌚"},
            {"query": "louis vuitton executive briefcase louis vuitton", "trend": "up", "change": "+38%", "category": "accesorios", "icon": "💼"},
            {"query": "gucci belt gucci", "trend": "up", "change": "+32%", "category": "accesorios", "icon": "👔"},
            {"query": "prada sunglasses prada", "trend": "up", "change": "+28%", "category": "accesorios", "icon": "🕶️"},
            
            # Tendencias Deportivas
            {"query": "nike air max 270 nike", "trend": "up", "change": "+35%", "category": "zapatillas", "icon": "👟"},
            {"query": "adidas ultraboost 22 adidas", "trend": "up", "change": "+30%", "category": "zapatillas", "icon": "🏃"},
            {"query": "jordan 1 retro jordan", "trend": "up", "change": "+25%", "category": "zapatillas", "icon": "🏀"},
            {"query": "yeezy boost 350 yeezy", "trend": "up", "change": "+22%", "category": "zapatillas", "icon": "👟"},
            
            # Tendencias Ropa
            {"query": "ropa formal", "trend": "up", "change": "+18%", "category": "ropa", "icon": "👔"},
            {"query": "chaquetas de invierno", "trend": "up", "change": "+15%", "category": "ropa", "icon": "🧥"},
            {"query": "hoodies nike", "trend": "up", "change": "+12%", "category": "ropa", "icon": "👕"},
            {"query": "jeans levis", "trend": "up", "change": "+10%", "category": "ropa", "icon": "👖"},
            
            # Tendencias Accesorios
            {"query": "smart watch apple", "trend": "up", "change": "+40%", "category": "tecnología", "icon": "⌚"},
            {"query": "gafas de sol ray ban", "trend": "up", "change": "+25%", "category": "accesorios", "icon": "🕶️"},
            {"query": "mochilas nike", "trend": "up", "change": "+20%", "category": "accesorios", "icon": "🎒"},
            {"query": "gorras new era", "trend": "up", "change": "+15%", "category": "accesorios", "icon": "🧢"},
            
            # Tendencias Colores
            {"query": "ropa negra", "trend": "up", "change": "+20%", "category": "color", "icon": "⚫"},
            {"query": "zapatillas blancas", "trend": "up", "change": "+18%", "category": "color", "icon": "⚪"},
            {"query": "ropa azul", "trend": "up", "change": "+12%", "category": "color", "icon": "🔵"},
            {"query": "accesorios dorados", "trend": "up", "change": "+8%", "category": "color", "icon": "🟡"},
            
            # Tendencias Estacionales
            {"query": "ropa de invierno", "trend": "up", "change": "+30%", "category": "estacional", "icon": "❄️"},
            {"query": "zapatos de lluvia", "trend": "up", "change": "+25%", "category": "estacional", "icon": "🌧️"},
            {"query": "guantes de cuero", "trend": "up", "change": "+20%", "category": "estacional", "icon": "🧤"},
            {"query": "bufandas de lana", "trend": "up", "change": "+15%", "category": "estacional", "icon": "🧣"}
        ]
        
        return {
            "trending_searches": tendencias[:limit],
            "total_trends": len(tendencias),
            "period": "última semana",
            "analysis_date": datetime.utcnow().isoformat(),
            "categories": {
                "premium": len([t for t in tendencias if t.get("category") in ["relojes", "accesorios"]]),
                "deportivo": len([t for t in tendencias if t.get("category") == "zapatillas"]),
                "ropa": len([t for t in tendencias if t.get("category") == "ropa"]),
                "accesorios": len([t for t in tendencias if t.get("category") == "accesorios"]),
                "color": len([t for t in tendencias if t.get("category") == "color"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tendencias: {str(e)}")

@router.get("/autocomplete")
def autocompletar_busqueda(
    q: str = Query(..., description="Término de búsqueda para autocompletar"),
    limit: int = Query(8, ge=1, le=20, description="Número de sugerencias"),
    db: Session = Depends(database.get_db)
):
    """Autocompletar búsqueda con sugerencias inteligentes"""
    try:
        search_engine = get_search_recommendation_engine(db)
        
        if len(q) < 2:
            return {
                "query": q,
                "suggestions": [],
                "total_suggestions": 0
            }
        
        # Obtener sugerencias
        sugerencias = search_engine.get_search_suggestions(q, limit)
        
        # Formatear sugerencias con información adicional
        sugerencias_formateadas = []
        for sugerencia in sugerencias:
            # Buscar productos que coincidan con la sugerencia
            productos = search_engine.search_products(sugerencia, limit=1)
            
            sugerencias_formateadas.append({
                "text": sugerencia,
                "type": "suggestion",
                "product_count": len(productos),
                "category": productos[0]['categoria'] if productos else None
            })
        
        return {
            "query": q,
            "suggestions": sugerencias_formateadas,
            "total_suggestions": len(sugerencias_formateadas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en autocompletar: {str(e)}")

@router.get("/filters")
def obtener_filtros_disponibles(
    q: str = Query(None, description="Término de búsqueda para filtrar opciones"),
    db: Session = Depends(database.get_db)
):
    """Obtener filtros disponibles para una búsqueda"""
    try:
        from database.models import Categoria, Producto, ProductoVariante
        from sqlalchemy import func
        
        # Obtener categorías disponibles
        categorias = db.query(Categoria.nombre).all()
        
        # Obtener marcas disponibles
        marcas = db.query(Producto.marca).distinct().all()
        
        # Obtener colores disponibles
        colores = db.query(ProductoVariante.color).distinct().all()
        
        # Obtener rangos de precio
        precio_min = db.query(func.min(ProductoVariante.precio)).scalar()
        precio_max = db.query(func.max(ProductoVariante.precio)).scalar()
        
        # Filtrar por búsqueda si se proporciona
        if q:
            search_engine = get_search_recommendation_engine(db)
            productos_busqueda = search_engine.search_products(q, limit=100)
            
            # Extraer categorías, marcas y colores de los resultados
            categorias_resultado = list(set([p['categoria'] for p in productos_busqueda]))
            marcas_resultado = list(set([p['marca'] for p in productos_busqueda]))
            colores_resultado = list(set([p['color'] for p in productos_busqueda]))
            
            # Filtrar precios de los resultados
            precios_resultado = [p['precio'] for p in productos_busqueda]
            precio_min_resultado = min(precios_resultado) if precios_resultado else precio_min
            precio_max_resultado = max(precios_resultado) if precios_resultado else precio_max
        else:
            categorias_resultado = [cat.nombre for cat in categorias]
            marcas_resultado = [marca.marca for marca in marcas if marca.marca]
            colores_resultado = [color.color for color in colores if color.color]
            precio_min_resultado = precio_min
            precio_max_resultado = precio_max
        
        return {
            "query": q,
            "filters": {
                "categories": categorias_resultado,
                "brands": marcas_resultado,
                "colors": colores_resultado,
                "price_range": {
                    "min": precio_min_resultado,
                    "max": precio_max_resultado
                }
            },
            "total_options": {
                "categories": len(categorias_resultado),
                "brands": len(marcas_resultado),
                "colors": len(colores_resultado)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener filtros: {str(e)}")

@router.get("/quick-search")
def busquedas_rapidas(
    category: str = Query(None, description="Categoría para búsquedas rápidas"),
    limit: int = Query(12, ge=1, le=30, description="Número de opciones rápidas"),
    db: Session = Depends(database.get_db)
):
    """Obtener opciones de búsqueda rápida por categorías"""
    try:
        # Búsquedas rápidas organizadas por categorías
        quick_searches = {
            "premium": [
                {"query": "rolex submariner rolex", "icon": "⌚", "trend": "up", "price_range": "$5,000+"},
                {"query": "louis vuitton neverfull louis vuitton", "icon": "👜", "trend": "up", "price_range": "$1,500+"},
                {"query": "gucci loafers gucci", "icon": "👞", "trend": "up", "price_range": "$800+"},
                {"query": "prada handbag prada", "icon": "👜", "trend": "up", "price_range": "$1,200+"},
                {"query": "hermes birkin hermes", "icon": "👜", "trend": "up", "price_range": "$10,000+"},
                {"query": "cartier santos cartier", "icon": "⌚", "trend": "up", "price_range": "$3,000+"}
            ],
            "deportivo": [
                {"query": "nike air jordan 1 nike", "icon": "🏀", "trend": "up", "price_range": "$150-300"},
                {"query": "adidas yeezy boost adidas", "icon": "👟", "trend": "up", "price_range": "$200-400"},
                {"query": "nike dunk low nike", "icon": "👟", "trend": "up", "price_range": "$100-200"},
                {"query": "converse chuck taylor converse", "icon": "👟", "trend": "up", "price_range": "$50-100"},
                {"query": "vans old skool vans", "icon": "🛹", "trend": "up", "price_range": "$60-120"},
                {"query": "new balance 990 new balance", "icon": "👟", "trend": "up", "price_range": "$120-200"}
            ],
            "ropa": [
                {"query": "hoodies nike", "icon": "👕", "trend": "up", "price_range": "$40-80"},
                {"query": "jeans levis 501", "icon": "👖", "trend": "up", "price_range": "$60-120"},
                {"query": "chaquetas bomber", "icon": "🧥", "trend": "up", "price_range": "$80-150"},
                {"query": "poleras básicas", "icon": "👕", "trend": "up", "price_range": "$20-40"},
                {"query": "pantalones cargo", "icon": "👖", "trend": "up", "price_range": "$50-100"},
                {"query": "suéteres de lana", "icon": "🧥", "trend": "up", "price_range": "$60-120"}
            ],
            "accesorios": [
                {"query": "smart watch apple", "icon": "⌚", "trend": "up", "price_range": "$200-500"},
                {"query": "gafas de sol ray ban", "icon": "🕶️", "trend": "up", "price_range": "$100-300"},
                {"query": "mochilas nike", "icon": "🎒", "trend": "up", "price_range": "$40-80"},
                {"query": "gorras new era", "icon": "🧢", "trend": "up", "price_range": "$25-50"},
                {"query": "cinturones de cuero", "icon": "👔", "trend": "up", "price_range": "$30-80"},
                {"query": "relojes casio", "icon": "⌚", "trend": "up", "price_range": "$50-150"}
            ],
            "colores": [
                {"query": "ropa negra", "icon": "⚫", "trend": "up", "description": "Clásico y elegante"},
                {"query": "zapatillas blancas", "icon": "⚪", "trend": "up", "description": "Versátil y limpio"},
                {"query": "ropa azul marino", "icon": "🔵", "trend": "up", "description": "Profesional"},
                {"query": "accesorios dorados", "icon": "🟡", "trend": "up", "description": "Lujoso"},
                {"query": "ropa verde militar", "icon": "🟢", "trend": "up", "description": "Tendencia"},
                {"query": "zapatillas rojas", "icon": "🔴", "trend": "up", "description": "Llamativo"}
            ],
            "estacional": [
                {"query": "ropa de invierno", "icon": "❄️", "trend": "up", "description": "Temporada actual"},
                {"query": "zapatos de lluvia", "icon": "🌧️", "trend": "up", "description": "Protección"},
                {"query": "guantes de cuero", "icon": "🧤", "trend": "up", "description": "Elegancia"},
                {"query": "bufandas de lana", "icon": "🧣", "trend": "up", "description": "Calidez"},
                {"query": "botas de invierno", "icon": "🥾", "trend": "up", "description": "Resistencia"},
                {"query": "chaquetas parka", "icon": "🧥", "trend": "up", "description": "Abrigo completo"}
            ]
        }
        
        # Si se especifica una categoría, devolver solo esa
        if category and category in quick_searches:
            return {
                "category": category,
                "quick_searches": quick_searches[category][:limit],
                "total_options": len(quick_searches[category]),
                "description": f"Búsquedas rápidas para {category}"
            }
        
        # Si no se especifica categoría, devolver todas
        all_searches = []
        for cat, searches in quick_searches.items():
            all_searches.extend(searches[:2])  # 2 de cada categoría
        
        return {
            "quick_searches": all_searches[:limit],
            "total_options": len(all_searches),
            "available_categories": list(quick_searches.keys()),
            "description": "Búsquedas rápidas por categorías"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener búsquedas rápidas: {str(e)}")

@router.get("/trending-categories")
def obtener_categorias_trending(
    limit: int = Query(8, ge=1, le=20, description="Número de categorías trending"),
    db: Session = Depends(database.get_db)
):
    """Obtener categorías más trending con ejemplos"""
    try:
        trending_categories = [
            {
                "category": "relojes de lujo",
                "icon": "⌚",
                "trend": "up",
                "change": "+45%",
                "examples": ["rolex submariner", "omega speedmaster", "cartier santos"],
                "price_range": "$1,000+",
                "description": "Relojes premium y de colección"
            },
            {
                "category": "zapatillas limitadas",
                "icon": "👟",
                "trend": "up",
                "change": "+40%",
                "examples": ["nike air jordan", "adidas yeezy", "off-white nike"],
                "price_range": "$200-800",
                "description": "Ediciones especiales y colaboraciones"
            },
            {
                "category": "accesorios ejecutivos",
                "icon": "💼",
                "trend": "up",
                "change": "+35%",
                "examples": ["maletines louis vuitton", "cinturones gucci", "corbatas hermes"],
                "price_range": "$200-2,000",
                "description": "Accesorios para profesionales"
            },
            {
                "category": "ropa streetwear",
                "icon": "👕",
                "trend": "up",
                "change": "+30%",
                "examples": ["hoodies supreme", "camisetas off-white", "pantalones balenciaga"],
                "price_range": "$50-500",
                "description": "Moda urbana y juvenil"
            },
            {
                "category": "gafas de sol premium",
                "icon": "🕶️",
                "trend": "up",
                "change": "+25%",
                "examples": ["ray ban aviator", "oakley holbrook", "persol 649"],
                "price_range": "$100-400",
                "description": "Protección solar de alta calidad"
            },
            {
                "category": "mochilas técnicas",
                "icon": "🎒",
                "trend": "up",
                "change": "+20%",
                "examples": ["nike tech pack", "adidas originals", "herschel supply"],
                "price_range": "$40-150",
                "description": "Funcionalidad y estilo"
            },
            {
                "category": "zapatos formales",
                "icon": "👞",
                "trend": "up",
                "change": "+15%",
                "examples": ["oxfords church", "loafers gucci", "botines allen edmonds"],
                "price_range": "$200-800",
                "description": "Elegancia para oficina"
            },
            {
                "category": "ropa de invierno",
                "icon": "🧥",
                "trend": "up",
                "change": "+10%",
                "examples": ["chaquetas canada goose", "abrigos burberry", "suéteres moncler"],
                "price_range": "$100-1,500",
                "description": "Protección contra el frío"
            }
        ]
        
        return {
            "trending_categories": trending_categories[:limit],
            "total_categories": len(trending_categories),
            "period": "última semana",
            "analysis_date": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías trending: {str(e)}")

@router.get("/health")
def verificar_salud_busqueda(db: Session = Depends(database.get_db)):
    """Verificar el estado del sistema de búsqueda"""
    try:
        search_engine = get_search_recommendation_engine(db)
        
        # Probar búsqueda básica
        test_results = search_engine.search_products("test", limit=1)
        
        # Obtener estadísticas de la base de datos
        from database.models import Producto, ProductoVariante, Categoria
        
        total_productos = db.query(Producto).count()
        total_variantes = db.query(ProductoVariante).count()
        total_categorias = db.query(Categoria).count()
        
        return {
            "status": "healthy",
            "search_engine": "operational",
            "database_stats": {
                "total_productos": total_productos,
                "total_variantes": total_variantes,
                "total_categorias": total_categorias
            },
            "test_search": "successful",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "search_engine": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

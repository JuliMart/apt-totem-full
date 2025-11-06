from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import models, database
from services.recommendation_engine import get_recommendation_engine
from typing import List, Optional

router = APIRouter(prefix="/recomendaciones", tags=["Recomendaciones"])

@router.get("/")
def recomendar(
    categoria: str = Query(None, description="Ej: zapatillas"),
    color: str = Query(None, description="Ej: rojo"),
    marca: str = Query(None, description="Ej: nike"),
    precio_max: float = Query(None, description="Precio máximo"),
    session_id: str = Query(None, description="ID de sesión para tracking"),
    limit: int = Query(10, ge=1, le=50, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """Recomendaciones básicas por filtros con tracking"""
    engine = get_recommendation_engine(db)
    
    if categoria:
        return engine.get_products_by_category(categoria, limit, session_id)
    elif color:
        return engine.get_products_by_color(color, limit, session_id)
    elif marca:
        return engine.get_products_by_brand(marca, limit, session_id)
    elif precio_max:
        return engine.get_products_by_price_range(0, precio_max, limit, session_id)
    else:
        # Si no hay filtros, devolver productos trending
        return engine.get_trending_products(limit=limit, session_id=session_id)

@router.get("/similar/{product_id}")
def productos_similares(
    product_id: int,
    limit: int = Query(5, ge=1, le=20, description="Número de productos similares"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos similares a uno específico"""
    engine = get_recommendation_engine(db)
    return engine.get_similar_products(product_id, limit)

@router.get("/cross-sell/{product_id}")
def productos_complementarios(
    product_id: int,
    limit: int = Query(5, ge=1, le=20, description="Número de productos complementarios"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos complementarios (cross-selling)"""
    engine = get_recommendation_engine(db)
    return engine.get_cross_sell_recommendations(product_id, limit)

@router.get("/personalizadas")
def recomendaciones_personalizadas(
    edad: str = Query(None, description="Rango de edad: 18-25, 26-35, 36-45, 46-55, 55+"),
    genero: str = Query(None, description="masculino, femenino"),
    estilo: str = Query(None, description="casual, formal, deportivo, elegante"),
    color_preferido: str = Query(None, description="Color preferido"),
    limit: int = Query(10, ge=1, le=50, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """Recomendaciones personalizadas basadas en perfil del usuario"""
    engine = get_recommendation_engine(db)
    return engine.get_personalized_recommendations(
        age_range=edad,
        gender=genero,
        clothing_style=estilo,
        color_preference=color_preferido,
        limit=limit
    )

@router.get("/trending")
def productos_trending(
    dias: int = Query(7, ge=1, le=30, description="Días para calcular trending"),
    limit: int = Query(10, ge=1, le=50, description="Número de productos trending"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos trending basados en detecciones recientes"""
    engine = get_recommendation_engine(db)
    return engine.get_trending_products(days=dias, limit=limit)

@router.get("/presupuesto")
def recomendaciones_presupuesto(
    presupuesto_max: float = Query(..., description="Presupuesto máximo"),
    limit: int = Query(10, ge=1, le=50, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """Recomendaciones dentro de un presupuesto"""
    engine = get_recommendation_engine(db)
    return engine.get_budget_recommendations(presupuesto_max, limit)

@router.get("/estacionales")
def recomendaciones_estacionales(
    temporada: str = Query("verano", description="verano, invierno, primavera, otoño"),
    limit: int = Query(10, ge=1, le=50, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """Recomendaciones estacionales"""
    engine = get_recommendation_engine(db)
    return engine.get_seasonal_recommendations(temporada, limit)

@router.get("/categoria/{categoria}")
def productos_por_categoria(
    categoria: str,
    limit: int = Query(10, ge=1, le=50, description="Número de productos"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos por categoría específica"""
    engine = get_recommendation_engine(db)
    return engine.get_products_by_category(categoria, limit)

@router.get("/marca/{marca}")
def productos_por_marca(
    marca: str,
    limit: int = Query(10, ge=1, le=50, description="Número de productos"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos por marca específica"""
    engine = get_recommendation_engine(db)
    return engine.get_products_by_brand(marca, limit)

@router.get("/color/{color}")
def productos_por_color(
    color: str,
    limit: int = Query(10, ge=1, le=50, description="Número de productos"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos por color específico"""
    engine = get_recommendation_engine(db)
    return engine.get_products_by_color(color, limit)

@router.get("/rango-precio")
def productos_por_rango_precio(
    precio_min: float = Query(0, description="Precio mínimo"),
    precio_max: float = Query(..., description="Precio máximo"),
    limit: int = Query(10, ge=1, le=50, description="Número de productos"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos por rango de precio"""
    engine = get_recommendation_engine(db)
    return engine.get_products_by_price_range(precio_min, precio_max, limit)

@router.post("/basadas-deteccion")
def recomendaciones_basadas_deteccion(
    edad: str = Query(..., description="Rango de edad detectado: 18-25, 26-35, 36-45, 46-55, 55+"),
    color: str = Query(..., description="Color detectado: blanco, negro, azul, rojo, etc."),
    estilo: str = Query(..., description="Estilo detectado: casual, formal, deportivo, elegante"),
    prenda: str = Query(None, description="Prenda detectada: camiseta, pantalon, chaqueta, etc."),
    session_id: str = Query(None, description="ID de sesión para tracking"),
    limit: int = Query(10, ge=1, le=50, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """Recomendaciones basadas en datos de detección en tiempo real"""
    engine = get_recommendation_engine(db)
    
    # Generar recomendaciones personalizadas basadas en detección
    recommendations = engine.get_personalized_recommendations(
        age_range=edad,
        clothing_style=estilo,
        color_preference=color,
        limit=limit,
        session_id=session_id
    )
    
    # Agregar información de contexto de detección
    detection_context = {
        "detection_data": {
            "age_range": edad,
            "detected_color": color,
            "detected_style": estilo,
            "detected_clothing": prenda
        },
        "recommendation_strategy": "real_time_detection",
        "confidence_level": "high" if prenda else "medium"
    }
    
    return {
        "recommendations": recommendations,
        "context": detection_context,
        "total_found": len(recommendations)
    }

@router.get("/smart")
def recomendaciones_inteligentes(
    # Parámetros de detección de IMAGEN (CV/IA)
    edad: str = Query(None, description="Rango de edad detectado: 18-25, 26-35, 36-45, 46-55, 55+"),
    color: str = Query(None, description="Color detectado: blanco, negro, azul, rojo, etc."),
    estilo: str = Query(None, description="Estilo: casual, formal, deportivo, elegante"),
    prenda: str = Query(None, description="Prenda detectada"),
    
    # Parámetros de análisis de VOZ (NLU)
    texto_voz: str = Query(None, description="Texto transcrito de voz"),
    intencion_voz: str = Query(None, description="Intención detectada: buscar, recomendar, etc."),
    
    # Generales
    session_id: str = Query(None, description="ID de sesión"),
    limit: int = Query(8, ge=1, le=20, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """
    🧠 Endpoint INTELIGENTE para recomendaciones basadas en:
    - Análisis de IMAGEN (CV/IA): edad, color, estilo, prenda
    - Análisis de VOZ (NLU): texto, intención
    
    Combina ambas fuentes para generar recomendaciones personalizadas.
    """
    # Crear sesión automáticamente si no existe
    if session_id and session_id != 'unknown':
        existing_session = db.query(models.Sesion).filter(models.Sesion.id_sesion == session_id).first()
        if not existing_session:
            # Crear sesión automáticamente usando SQL directo
            try:
                # Obtener o crear dispositivo por defecto
                dispositivo_result = db.execute(text("SELECT id_dispositivo FROM dispositivo LIMIT 1")).fetchone()
                if not dispositivo_result:
                    db.execute(text("INSERT INTO dispositivo (id_tienda, etiqueta, estado) VALUES (1, 'Totem-Default', 'active')"))
                    db.commit()
                    dispositivo_id = db.execute(text("SELECT id_dispositivo FROM dispositivo WHERE etiqueta = 'Totem-Default'")).fetchone()[0]
                else:
                    dispositivo_id = dispositivo_result[0]
                
                # Crear sesión
                db.execute(text("""
                    INSERT INTO sesion (id_sesion, id_dispositivo, canal, consent) 
                    VALUES (:id_sesion, :id_dispositivo, 'mixto', 1)
                """), {
                    'id_sesion': session_id,
                    'id_dispositivo': dispositivo_id
                })
                db.commit()
                print(f"✅ Sesión creada automáticamente: {session_id}")
            except Exception as e:
                print(f"⚠️ Error creando sesión: {e}")
                # Continuar sin sesión si hay error
    
    engine = get_recommendation_engine(db)
    
    # Determinar estrategia según qué datos están disponibles
    has_image_data = bool(edad or color or estilo or prenda)
    has_voice_data = bool(texto_voz or intencion_voz)
    
    if not has_image_data and not has_voice_data:
        # Sin datos: productos trending
        return {
            "recommendations": engine.get_trending_products(limit=limit, session_id=session_id),
            "strategy": "trending",
            "source": "none",
            "message": "Mostrando productos populares"
        }
    
    all_recommendations = []
    strategy = []
    
    # ═══════════════════════════════════════════
    # 1. ANÁLISIS DE VOZ (prioridad MÁS ALTA)
    # ═══════════════════════════════════════════
    if has_voice_data and texto_voz:
        strategy.append("voice")
        
        # Extraer keywords del texto de voz
        keywords = texto_voz.lower().split()
        
        # Buscar por categorías mencionadas
        categorias_map = {
            'zapatillas': 'Zapatillas',
            'zapatos': 'Zapatillas',
            'tenis': 'Zapatillas',
            'polera': 'Poleras',
            'camiseta': 'Poleras',
            'remera': 'Poleras',
            'camisa': 'Camisas',
            'chaqueta': 'Chaquetas',
            'casaca': 'Chaquetas',
            'jacket': 'Chaquetas',
            'pantalon': 'Pantalones',
            'jeans': 'Pantalones',
            'short': 'Shorts',
            'gorro': 'Gorros',
            'gafas': 'Gafas',
            'lentes': 'Gafas',
            'reloj': 'Accesorios',
            'watch': 'Accesorios',
            'relojes': 'Accesorios',
            'smart': 'Accesorios',
            'smartwatch': 'Accesorios',
            'smart watch': 'Accesorios',
            'apple': 'Accesorios',
            'rolex': 'Accesorios',
            'casio': 'Accesorios',
            'mochila': 'Accesorios',
            'cartera': 'Accesorios',
            'accesorios': 'Accesorios'
        }
        
        # Colores mencionados
        colores_map = {
            'azul': 'azul',
            'azules': 'azul',
            'rojo': 'rojo',
            'rojos': 'rojo',
            'negro': 'negro',
            'negros': 'negro',
            'blanco': 'blanco',
            'blancos': 'blanco',
            'verde': 'verde',
            'verdes': 'verde',
            'amarillo': 'amarillo',
            'amarillos': 'amarillo',
            'gris': 'gris',
            'grises': 'gris'
        }
        
        # Buscar categoría en el texto
        voice_category = None
        for keyword in keywords:
            if keyword in categorias_map:
                voice_category = categorias_map[keyword]
                break
        
        # Buscar color en el texto
        voice_color = None
        for keyword in keywords:
            if keyword in colores_map:
                voice_color = colores_map[keyword]
                break
        
        # Extraer talla mencionada (números de 35-50 típicamente para calzado)
        import re
        tallas_pattern = r'\b(3[5-9]|4[0-9]|50)\b'  # Tallas 35-50
        talla_match = re.search(tallas_pattern, texto_voz)
        voice_talla = talla_match.group(0) if talla_match else None
        
        # Búsqueda por categoría y talla de voz (PRIORIDAD MÁXIMA)
        if voice_category and voice_talla:
            # Buscar productos específicos de la categoría Y talla
            query = db.query(models.ProductoVariante).join(models.Producto).join(models.Categoria).filter(
                models.Categoria.nombre == voice_category,
                models.ProductoVariante.talla == voice_talla
            ).limit(8)
            
            category_size_products = []
            for variante in query.all():
                category_size_products.append({
                    'id_variante': variante.id_variante,
                    'id_producto': variante.id_producto,
                    'nombre': variante.producto.nombre,
                    'marca': variante.producto.marca,
                    'categoria': variante.producto.categoria,
                    'color': variante.color,
                    'talla': variante.talla,
                    'precio': float(variante.precio),
                    'stock': variante.stock,
                    'image_url': variante.image_url
                })
            
            if category_size_products:
                all_recommendations.extend(category_size_products)
                print(f"✅ VOZ: Encontrados {len(category_size_products)} productos de {voice_category} talla {voice_talla}")
            else:
                print(f"⚠️ VOZ: No se encontraron {voice_category} talla {voice_talla}, buscando sin talla...")
                # Fallback: buscar sin talla
                category_products = engine.get_products_by_category(voice_category, limit=5, session_id=session_id)
                all_recommendations.extend(category_products)
        elif voice_category:
            # Búsqueda solo por categoría
            category_products = engine.get_products_by_category(voice_category, limit=5, session_id=session_id)
            all_recommendations.extend(category_products)
            print(f"✅ VOZ: Encontrados productos de {voice_category} (sin talla específica)")
        
        # Búsqueda por color de voz
        if voice_color:
            color_products = engine.get_products_by_color(voice_color, limit=4, session_id=session_id)
            all_recommendations.extend(color_products)
    
    # ═══════════════════════════════════════════
    # 2. ANÁLISIS DE IMAGEN (prioridad ALTA)
    # ═══════════════════════════════════════════
    if has_image_data:
        strategy.append("image_detection")
        
        # Mapeo de prendas detectadas a categorías
        clothing_to_category = {
            'camiseta': 'Poleras',
            'pantalon': 'Pantalones', 
            'chaqueta': 'Chaquetas',
            'zapatillas': 'Zapatillas',
            'vestido': 'Vestidos',
            'gorro': 'Gorros',
            'gafas': 'Gafas',
            'gafas_sol': 'Gafas',
            'reloj': 'Accesorios',
            'watch': 'Accesorios',
            'relojes': 'Accesorios',
            'mochila': 'Accesorios',
            'cartera': 'Accesorios',
            'bolso': 'Bolsos',
            'bolso_cruzado': 'Bolsos',
            'mochila': 'Mochilas',
            'cartera': 'Bolsos'
        }
        
        specific_category = None
        if prenda and prenda.lower() in clothing_to_category:
            specific_category = clothing_to_category[prenda.lower()]
        
        # Productos del color detectado
        if color and color != "desconocido":
            color_products = engine.get_products_by_color(color, limit=3, session_id=session_id)
            all_recommendations.extend(color_products)
        
        # Productos de la categoría detectada
        if specific_category:
            category_products = engine.get_products_by_category(specific_category, limit=3, session_id=session_id)
            all_recommendations.extend(category_products)
        
        # Recomendaciones personalizadas por edad y estilo
        if edad or estilo:
            personalized = engine.get_personalized_recommendations(
                age_range=edad,
                clothing_style=estilo,
                color_preference=color if color != "desconocido" else None,
                limit=4,
                session_id=session_id
            )
            all_recommendations.extend(personalized)
    
    # ═══════════════════════════════════════════
    # 3. ELIMINAR DUPLICADOS Y LIMITAR
    # ═══════════════════════════════════════════
    unique_products = []
    seen_ids = set()
    for product in all_recommendations:
        product_id = product.get('id_variante')
        if product_id and product_id not in seen_ids:
            unique_products.append(product)
            seen_ids.add(product_id)
            if len(unique_products) >= limit:
                break
    
    # Si no hay suficientes, rellenar con trending
    if len(unique_products) < limit:
        trending = engine.get_trending_products(limit=limit - len(unique_products), session_id=session_id)
        for product in trending:
            product_id = product.get('id_variante')
            if product_id and product_id not in seen_ids:
                unique_products.append(product)
                seen_ids.add(product_id)
    
    return {
        "recommendations": unique_products,
        "analysis_summary": {
            # Datos de imagen
            "image_data": {
                "age_range": edad,
                "detected_color": color,
                "detected_style": estilo,
                "detected_clothing": prenda
            } if has_image_data else None,
            # Datos de voz
            "voice_data": {
                "transcribed_text": texto_voz,
                "detected_intent": intencion_voz
            } if has_voice_data else None
        },
        "strategy": "+".join(strategy) if strategy else "trending",
        "sources_used": {
            "voice_analysis": has_voice_data,
            "image_analysis": has_image_data
        },
        "total_found": len(unique_products),
        "confidence": "high" if (has_voice_data and has_image_data) else ("medium" if (has_voice_data or has_image_data) else "low")
    }

@router.get("/detection-based")
def recomendaciones_por_deteccion(
    edad: str = Query(..., description="Rango de edad: 18-25, 26-35, 36-45, 46-55, 55+"),
    color: str = Query(..., description="Color detectado: blanco, negro, azul, rojo, etc."),
    estilo: str = Query(..., description="Estilo: casual, formal, deportivo, elegante"),
    prenda: str = Query(None, description="Prenda detectada"),
    session_id: str = Query(None, description="ID de sesión"),
    limit: int = Query(8, ge=1, le=20, description="Número de recomendaciones"),
    db: Session = Depends(database.get_db)
):
    """Endpoint optimizado para el frontend - recomendaciones basadas en detección"""
    engine = get_recommendation_engine(db)
    
    # Estrategia de recomendación basada en datos detectados
    strategy = "detection_based"
    
    # Mapeo de prendas detectadas a categorías
    clothing_to_category = {
        'camiseta': 'Poleras',
        'pantalon': 'Pantalones', 
        'chaqueta': 'Chaquetas',
        'zapatillas': 'Zapatillas',
        'vestido': 'Vestidos',
        'gorro': 'Gorros',
        'gafas': 'Gafas',
        'gafas_sol': 'Gafas',
        'bolso': 'Accesorios',
        'bolso_cruzado': 'Accesorios',
        'mochila': 'Accesorios',
        'cartera': 'Accesorios'
    }
    
    # Obtener categoría específica si se detectó prenda
    specific_category = None
    if prenda and prenda in clothing_to_category:
        specific_category = clothing_to_category[prenda]
    
    # Generar recomendaciones
    all_recommendations = []
    
    # 1. Productos del color detectado (prioridad alta)
    if color and color != "desconocido":
        color_products = engine.get_products_by_color(color, limit=4, session_id=None)
        all_recommendations.extend(color_products)
    
    # 2. Productos de la categoría específica detectada
    if specific_category:
        category_products = engine.get_products_by_category(specific_category, limit=3, session_id=None)
        all_recommendations.extend(category_products)
    
    # 3. Recomendaciones personalizadas por edad y estilo
    personalized = engine.get_personalized_recommendations(
        age_range=edad,
        clothing_style=estilo,
        color_preference=color,
        limit=limit,
        session_id=session_id
    )
    all_recommendations.extend(personalized)
    
    # Eliminar duplicados y limitar
    unique_products = []
    seen_ids = set()
    for product in all_recommendations:
        if product.get('id_variante') not in seen_ids:
            unique_products.append(product)
            seen_ids.add(product.get('id_variante'))
            if len(unique_products) >= limit:
                break
    
    return {
        "recommendations": unique_products,
        "detection_summary": {
            "age_range": edad,
            "detected_color": color,
            "detected_style": estilo,
            "detected_clothing": prenda,
            "specific_category": specific_category
        },
        "strategy": strategy,
        "total_found": len(unique_products),
        "confidence": "high" if prenda and color != "desconocido" else "medium"
    }

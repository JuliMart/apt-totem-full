"""
Router para detalles de productos y compra rápida
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from database import database, models
from services.recommendation_tracker import get_recommendation_tracker
from typing import Optional
from datetime import datetime
import json
# QR ficticio para demostración

router = APIRouter(prefix="/product", tags=["Product Detail"])

@router.get("/{variant_id}/detail")
def get_product_detail(
    variant_id: int,
    session_id: Optional[str] = Query(None, description="ID de sesión para tracking"),
    db: Session = Depends(database.get_db)
):
    """Obtener detalles completos de un producto"""
    try:
        # Obtener la variante del producto
        variante = db.query(models.ProductoVariante).filter(
            models.ProductoVariante.id_variante == variant_id
        ).first()
        
        if not variante:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Obtener el producto
        producto = db.query(models.Producto).filter(
            models.Producto.id_producto == variante.id_producto
        ).first()
        
        # Obtener la categoría
        categoria = db.query(models.Categoria).filter(
            models.Categoria.id_categoria == producto.id_categoria
        ).first()
        
        # Obtener otras variantes del mismo producto
        otras_variantes = db.query(models.ProductoVariante).filter(
            models.ProductoVariante.id_producto == producto.id_producto,
            models.ProductoVariante.id_variante != variant_id
        ).limit(5).all()
        
        # QR ficticio para compra rápida
        qr_data = {
            "producto": producto.nombre,
            "variante_id": variant_id,
            "sku": variante.sku,
            "precio": variante.precio,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # QR ficticio (imagen base64 de demostración)
        qr_code = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        # Registrar interacción si hay session_id
        if session_id:
            try:
                tracker = get_recommendation_tracker(db)
                tracker.track_user_interaction(
                    session_id=session_id,
                    interaction_type="product_detail_view",
                    variant_id=variant_id,
                    metadata={"product_name": producto.nombre, "action": "view_detail"},
                    duration_seconds=None
                )
            except Exception as e:
                print(f"⚠️ Error registrando interacción: {e}")
        
        return {
            "producto": {
                "id_variante": variante.id_variante,
                "id_producto": producto.id_producto,
                "nombre": producto.nombre,
                "marca": producto.marca,
                "categoria": categoria.nombre,
                "sku": variante.sku,
                "color": variante.color,
                "talla": variante.talla,
                "precio": variante.precio,
                "image_url": variante.image_url,
                "created_at": variante.created_at.isoformat() if variante.created_at else None
            },
            "otras_variantes": [
                {
                    "id_variante": v.id_variante,
                    "color": v.color,
                    "talla": v.talla,
                    "precio": v.precio,
                    "image_url": v.image_url
                }
                for v in otras_variantes
            ],
            "qr_compra": {
                "data": qr_data,
                "qr_code": qr_code,
                "message": "Escanea este QR para compra rápida"
            },
            "compra_rapida": {
                "url_pago": f"https://tienda.neototem.com/pagar/{variant_id}",
                "metodos_pago": ["tarjeta", "transferencia", "efectivo"],
                "despacho": "Disponible en 24-48 horas"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo detalles: {str(e)}")

@router.post("/{variant_id}/click")
def track_product_click(
    variant_id: int,
    session_id: str = Body(..., description="ID de sesión"),
    recommendation_id: Optional[int] = Body(None, description="ID de recomendación"),
    position: Optional[int] = Body(None, description="Posición en la lista"),
    db: Session = Depends(database.get_db)
):
    """Registrar click en producto recomendado"""
    try:
        # Verificar que la variante existe
        variante = db.query(models.ProductoVariante).filter(
            models.ProductoVariante.id_variante == variant_id
        ).first()
        
        if not variante:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Registrar la interacción
        tracker = get_recommendation_tracker(db)
        interaction_id = tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="product_click",
            variant_id=variant_id,
            metadata={
                "recommendation_id": recommendation_id,
                "position": position,
                "product_name": variante.producto.nombre if hasattr(variante, 'producto') else "Unknown"
            },
            duration_seconds=None
        )
        
        return {
            "success": True,
            "interaction_id": interaction_id,
            "message": "Click registrado correctamente",
            "product_name": variante.producto.nombre if hasattr(variante, 'producto') else "Unknown"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando click: {str(e)}")

@router.get("/{variant_id}/similar")
def get_similar_products(
    variant_id: int,
    limit: int = Query(5, ge=1, le=10, description="Número de productos similares"),
    db: Session = Depends(database.get_db)
):
    """Obtener productos similares"""
    try:
        # Obtener la variante actual
        variante = db.query(models.ProductoVariante).filter(
            models.ProductoVariante.id_variante == variant_id
        ).first()
        
        if not variante:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Buscar productos similares (misma categoría, marca, o color)
        similares = db.query(models.ProductoVariante).join(models.Producto).filter(
            models.Producto.id_categoria == variante.producto.id_categoria,
            models.ProductoVariante.id_variante != variant_id
        ).limit(limit).all()
        
        return [
            {
                "id_variante": v.id_variante,
                "producto": v.producto.nombre,
                "marca": v.producto.marca,
                "color": v.color,
                "talla": v.talla,
                "precio": v.precio,
                "image_url": v.image_url
            }
            for v in similares
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo similares: {str(e)}")

def generate_qr_code(data: str) -> str:
    """Generar QR ficticio para demostración"""
    # QR ficticio (imagen base64 de 1x1 pixel transparente)
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

@router.get("/qr/{variant_id}")
def get_qr_payment(
    variant_id: int,
    session_id: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    """Obtener QR específico para pago"""
    try:
        variante = db.query(models.ProductoVariante).filter(
            models.ProductoVariante.id_variante == variant_id
        ).first()
        
        if not variante:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Datos para el QR de pago
        payment_data = {
            "action": "payment",
            "product_id": variante.id_variante,
            "product_name": variante.producto.nombre,
            "price": variante.precio,
            "currency": "CLP",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # QR ficticio para pago
        qr_code = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        return {
            "qr_code": qr_code,
            "payment_data": payment_data,
            "product_info": {
                "nombre": variante.producto.nombre,
                "marca": variante.producto.marca,
                "precio": variante.precio,
                "sku": variante.sku
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando QR de pago: {str(e)}")

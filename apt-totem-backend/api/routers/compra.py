from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import database
from database.models import ProductoVariante, Producto, RecomendacionSesion
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/compra", tags=["Compra"])

# Modelos Pydantic
class OpcionCompra(BaseModel):
    id_variante: int
    producto: str
    marca: str
    precio: float
    puede_comprar_directo: bool
    razon: str
    opciones_disponibles: List[str]

class SolicitudCompra(BaseModel):
    id_sesion: str
    id_recomendacion: int
    id_variante: int
    cantidad: int = 1

class SolicitudVendedor(BaseModel):
    id_sesion: str
    id_recomendacion: int
    id_variante: int
    motivo: str = "Producto de alto valor"
    contacto_preferido: Optional[str] = None

@router.get("/verificar-precio/{id_recomendacion}")
def verificar_precio_y_opciones(
    id_recomendacion: int,
    db: Session = Depends(database.get_db)
):
    """Verificar precio de producto recomendado y determinar opciones de compra"""
    try:
        # Obtener la recomendación
        recomendacion = db.query(RecomendacionSesion).filter(
            RecomendacionSesion.id_recomendacion == id_recomendacion
        ).first()
        
        if not recomendacion:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # Buscar variantes del producto recomendado
        variantes = db.query(ProductoVariante).join(Producto).filter(
            Producto.nombre.ilike(f"%{recomendacion.producto}%")
        ).all()
        
        if not variantes:
            raise HTTPException(status_code=404, detail="Producto no encontrado en inventario")
        
        # Usar la primera variante disponible (en producción se podría mejorar la lógica)
        variante = variantes[0]
        producto = variante.producto
        
        # Determinar si se puede comprar directamente
        precio_maximo_directo = 1000000  # $1,000,000
        puede_comprar_directo = variante.precio < precio_maximo_directo
        
        # Definir opciones disponibles
        if puede_comprar_directo:
            opciones_disponibles = [
                "Comprar ahora",
                "Agregar al carrito",
                "Ver detalles",
                "Comparar con otros productos"
            ]
            razon = f"Producto disponible para compra directa (${variante.precio:,.0f})"
        else:
            opciones_disponibles = [
                "Llamar vendedor",
                "Solicitar información",
                "Programar cita",
                "Ver detalles del producto"
            ]
            razon = f"Producto de alto valor requiere asistencia de vendedor (${variante.precio:,.0f})"
        
        return {
            "id_recomendacion": id_recomendacion,
            "producto": producto.nombre,
            "marca": producto.marca,
            "precio": variante.precio,
            "puede_comprar_directo": puede_comprar_directo,
            "razon": razon,
            "opciones_disponibles": opciones_disponibles,
            "variante": {
                "id_variante": variante.id_variante,
                "sku": variante.sku,
                "talla": variante.talla,
                "color": variante.color,
                "precio": variante.precio,
                "image_url": variante.image_url
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando precio: {str(e)}")

@router.post("/comprar-directo")
def comprar_directo(
    solicitud: SolicitudCompra,
    db: Session = Depends(database.get_db)
):
    """Procesar compra directa de producto < $1M"""
    try:
        # Verificar que la variante existe y el precio es correcto
        variante = db.query(ProductoVariante).filter(
            ProductoVariante.id_variante == solicitud.id_variante
        ).first()
        
        if not variante:
            raise HTTPException(status_code=404, detail="Variante de producto no encontrada")
        
        # Verificar que el precio permite compra directa
        if variante.precio >= 1000000:
            raise HTTPException(
                status_code=400, 
                detail=f"Este producto (${variante.precio:,.0f}) requiere asistencia de vendedor"
            )
        
        # Verificar que la recomendación existe
        recomendacion = db.query(RecomendacionSesion).filter(
            RecomendacionSesion.id_recomendacion == solicitud.id_recomendacion
        ).first()
        
        if not recomendacion:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # Calcular total
        total = variante.precio * solicitud.cantidad
        
        # En producción aquí se integraría con el sistema de pagos
        # Por ahora simulamos la compra exitosa
        
        return {
            "compra_exitosa": True,
            "id_compra": f"COMP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "producto": variante.producto.nombre,
            "marca": variante.producto.marca,
            "variante": {
                "sku": variante.sku,
                "talla": variante.talla,
                "color": variante.color
            },
            "cantidad": solicitud.cantidad,
            "precio_unitario": variante.precio,
            "total": total,
            "metodo_pago": "Por definir",
            "estado": "Procesando",
            "mensaje": "Compra procesada exitosamente. Recibirás confirmación por email.",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando compra: {str(e)}")

@router.post("/solicitar-vendedor")
def solicitar_vendedor(
    solicitud: SolicitudVendedor,
    db: Session = Depends(database.get_db)
):
    """Solicitar asistencia de vendedor para producto > $1M"""
    try:
        # Verificar que la variante existe
        variante = db.query(ProductoVariante).filter(
            ProductoVariante.id_variante == solicitud.id_variante
        ).first()
        
        if not variante:
            raise HTTPException(status_code=404, detail="Variante de producto no encontrada")
        
        # Verificar que la recomendación existe
        recomendacion = db.query(RecomendacionSesion).filter(
            RecomendacionSesion.id_recomendacion == solicitud.id_recomendacion
        ).first()
        
        if not recomendacion:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # En producción aquí se integraría con el sistema de CRM
        # Por ahora simulamos la solicitud exitosa
        
        return {
            "solicitud_exitosa": True,
            "id_solicitud": f"VEND-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "producto": variante.producto.nombre,
            "marca": variante.producto.marca,
            "precio": variante.precio,
            "motivo": solicitud.motivo,
            "contacto_preferido": solicitud.contacto_preferido,
            "vendedor_asignado": "Por asignar",
            "tiempo_estimado": "5-10 minutos",
            "mensaje": "Un vendedor especializado se pondrá en contacto contigo pronto.",
            "opciones_contacto": [
                "Llamada telefónica",
                "WhatsApp",
                "Email",
                "Video llamada"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solicitando vendedor: {str(e)}")

@router.get("/historial-compras/{id_sesion}")
def obtener_historial_compras(
    id_sesion: str,
    db: Session = Depends(database.get_db)
):
    """Obtener historial de compras de una sesión"""
    try:
        # En producción esto vendría de una tabla de compras real
        # Por ahora simulamos datos
        
        compras_simuladas = [
            {
                "id_compra": "COMP-20251027120000",
                "producto": "Nike Air Max 270",
                "marca": "Nike",
                "precio": 450000,
                "cantidad": 1,
                "total": 450000,
                "fecha": "2025-10-27T12:00:00",
                "estado": "Completada"
            },
            {
                "id_compra": "COMP-20251027110000",
                "producto": "Adidas Ultraboost 22",
                "marca": "Adidas", 
                "precio": 380000,
                "cantidad": 1,
                "total": 380000,
                "fecha": "2025-10-27T11:00:00",
                "estado": "Completada"
            }
        ]
        
        return {
            "id_sesion": id_sesion,
            "total_compras": len(compras_simuladas),
            "compras": compras_simuladas,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo historial: {str(e)}")

@router.get("/estadisticas-ventas")
def obtener_estadisticas_ventas(
    dias: int = Query(7, ge=1, le=30, description="Días para analizar"),
    db: Session = Depends(database.get_db)
):
    """Obtener estadísticas de ventas"""
    try:
        # En producción esto vendría de datos reales de ventas
        # Por ahora simulamos estadísticas
        
        return {
            "periodo_dias": dias,
            "ventas_directas": {
                "total": 45,
                "monto_total": 18500000,
                "productos_mas_vendidos": [
                    {"producto": "Nike Air Max 270", "ventas": 12, "monto": 5400000},
                    {"producto": "Adidas Ultraboost 22", "ventas": 10, "monto": 3800000},
                    {"producto": "Puma RS-X Reinvention", "ventas": 8, "monto": 2400000}
                ]
            },
            "solicitudes_vendedor": {
                "total": 8,
                "productos_alto_valor": [
                    {"producto": "Rolex Submariner", "precio": 15000000, "solicitudes": 3},
                    {"producto": "Omega Speedmaster", "precio": 12000000, "solicitudes": 2},
                    {"producto": "Cartier Santos", "precio": 18000000, "solicitudes": 3}
                ]
            },
            "conversion_rate": 0.23,  # 23% de recomendaciones resultan en compra
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")


from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import database
from database.models import RecomendacionSesion, Sesion, Producto
from typing import List, Dict, Optional
from datetime import datetime
import random

router = APIRouter(prefix="/demo", tags=["Demo"])

@router.get("/generar-recomendacion")
def generar_recomendacion_demo(
    session_id: str = Query("demo-session", description="ID de la sesión"),
    db: Session = Depends(database.get_db)
):
    """Generar una recomendación de demo y abrir modal de calificación"""
    try:
        # Obtener o crear sesión
        sesion = db.query(Sesion).filter(Sesion.id_sesion == session_id).first()
        if not sesion:
            sesion = Sesion(
                id_sesion=session_id,
                inicio=datetime.utcnow(),
                canal="demo"
            )
            db.add(sesion)
            db.commit()
        
        # Obtener productos aleatorios para demo
        productos = db.query(Producto).limit(10).all()
        
        if not productos:
            # Si no hay productos, crear uno de demo
            producto_demo = Producto(
                nombre="Nike Air Max 270",
                marca="Nike",
                id_categoria=1
            )
            db.add(producto_demo)
            db.commit()
            productos = [producto_demo]
        
        # Seleccionar producto aleatorio
        producto_seleccionado = random.choice(productos)
        
        # Crear recomendación
        recomendacion = RecomendacionSesion(
            id_sesion=session_id,
            producto=producto_seleccionado.nombre,
            marca=producto_seleccionado.marca,
            categoria="zapatillas",
            fecha_hora=datetime.utcnow(),
            confianza=random.uniform(0.7, 0.95),
            razon_recomendacion="Basado en tus preferencias y tendencias actuales"
        )
        
        db.add(recomendacion)
        db.commit()
        db.refresh(recomendacion)
        
        # URL del modal de calificación
        modal_url = f"/modal-calificar?session_id={session_id}&recommendation_id={recomendacion.id_recomendacion}"
        
        return {
            "recomendacion_generada": True,
            "id_recomendacion": recomendacion.id_recomendacion,
            "producto": recomendacion.producto,
            "marca": recomendacion.marca,
            "confianza": recomendacion.confianza,
            "razon": recomendacion.razon_recomendacion,
            "modal_calificacion_url": modal_url,
            "instrucciones": {
                "mensaje": "Recomendación generada exitosamente",
                "accion": "El modal de calificación se abrirá automáticamente",
                "url": modal_url
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando recomendación: {str(e)}")

@router.get("/simular-flujo-completo")
def simular_flujo_completo(
    session_id: str = Query("demo-session", description="ID de la sesión"),
    db: Session = Depends(database.get_db)
):
    """Simular el flujo completo: recomendación -> calificación -> compra"""
    try:
        # Paso 1: Generar recomendación
        recomendacion_response = generar_recomendacion_demo(session_id, db)
        
        # Paso 2: URLs para el flujo completo
        modal_calificacion_url = recomendacion_response["modal_calificacion_url"]
        opciones_compra_url = f"/opciones-compra?session_id={session_id}&recommendation_id={recomendacion_response['id_recomendacion']}"
        
        return {
            "flujo_completo": True,
            "pasos": {
                "1_recomendacion": {
                    "estado": "completado",
                    "producto": recomendacion_response["producto"],
                    "marca": recomendacion_response["marca"],
                    "confianza": recomendacion_response["confianza"]
                },
                "2_calificacion": {
                    "estado": "pendiente",
                    "url": modal_calificacion_url,
                    "descripcion": "Modal automático para calificar la recomendación"
                },
                "3_compra": {
                    "estado": "pendiente",
                    "url": opciones_compra_url,
                    "descripcion": "Opciones de compra basadas en precio"
                }
            },
            "urls": {
                "modal_calificacion": modal_calificacion_url,
                "opciones_compra": opciones_compra_url,
                "dashboard": "/dashboard"
            },
            "instrucciones": {
                "mensaje": "Flujo completo simulado exitosamente",
                "pasos": [
                    "1. Recomendación generada",
                    "2. Abrir modal de calificación automáticamente",
                    "3. Después de calificar, mostrar opciones de compra",
                    "4. Ver métricas actualizadas en el dashboard"
                ]
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulando flujo: {str(e)}")

@router.get("/abrir-modal-calificacion")
def abrir_modal_calificacion(
    session_id: str = Query("demo-session", description="ID de la sesión"),
    recommendation_id: int = Query(1, description="ID de la recomendación"),
    db: Session = Depends(database.get_db)
):
    """Abrir modal de calificación para una recomendación específica"""
    try:
        # Verificar que la recomendación existe
        recomendacion = db.query(RecomendacionSesion).filter(
            RecomendacionSesion.id_recomendacion == recommendation_id
        ).first()
        
        if not recomendacion:
            raise HTTPException(status_code=404, detail="Recomendación no encontrada")
        
        # URL del modal
        modal_url = f"/modal-calificar?session_id={session_id}&recommendation_id={recommendation_id}"
        
        return {
            "modal_abierto": True,
            "id_recomendacion": recommendation_id,
            "producto": recomendacion.producto,
            "marca": recomendacion.marca,
            "modal_url": modal_url,
            "instrucciones": {
                "mensaje": "Modal de calificación listo para abrir",
                "accion": "Redirigir a la URL del modal",
                "url": modal_url
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error abriendo modal: {str(e)}")

@router.get("/estado-flujo")
def obtener_estado_flujo(
    session_id: str = Query("demo-session", description="ID de la sesión"),
    db: Session = Depends(database.get_db)
):
    """Obtener el estado actual del flujo de recomendaciones"""
    try:
        # Obtener sesión
        sesion = db.query(Sesion).filter(Sesion.id_sesion == session_id).first()
        
        if not sesion:
            return {
                "sesion_existe": False,
                "estado": "sesion_no_encontrada",
                "mensaje": "La sesión no existe"
            }
        
        # Obtener recomendaciones de la sesión
        recomendaciones = db.query(RecomendacionSesion).filter(
            RecomendacionSesion.id_sesion == session_id
        ).order_by(RecomendacionSesion.fecha_hora.desc()).limit(5).all()
        
        # Obtener calificaciones de la sesión
        from database.models import CalificacionRecomendacion
        calificaciones = db.query(CalificacionRecomendacion).filter(
            CalificacionRecomendacion.id_sesion == session_id
        ).all()
        
        return {
            "sesion_existe": True,
            "id_sesion": session_id,
            "inicio_sesion": sesion.inicio.isoformat() if sesion.inicio else None,
            "total_recomendaciones": len(recomendaciones),
            "total_calificaciones": len(calificaciones),
            "recomendaciones_recientes": [
                {
                    "id": r.id_recomendacion,
                    "producto": r.producto,
                    "marca": r.marca,
                    "fecha": r.fecha_hora.isoformat(),
                    "confianza": r.confianza
                }
                for r in recomendaciones
            ],
            "calificaciones": [
                {
                    "id": c.id_calificacion,
                    "calificacion": c.calificacion,
                    "comentario": c.comentario,
                    "fecha": c.fecha_hora.isoformat()
                }
                for c in calificaciones
            ],
            "estado": "activo",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")


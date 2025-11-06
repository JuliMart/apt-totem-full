from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import database
from database.models import CalificacionRecomendacion, RecomendacionSesion, Sesion
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])

# Modelos Pydantic
class CalificacionRequest(BaseModel):
    id_sesion: str
    id_recomendacion: int
    calificacion: int  # 1-5 estrellas
    comentario: Optional[str] = None

class CalificacionResponse(BaseModel):
    id_calificacion: int
    calificacion: int
    comentario: Optional[str]
    fecha_hora: datetime
    producto: str

class EstadisticasCalificaciones(BaseModel):
    promedio_calificacion: float
    total_calificaciones: int
    distribucion_calificaciones: Dict[int, int]
    calificaciones_recientes: List[CalificacionResponse]

@router.post("/calificar")
def calificar_recomendacion(
    calificacion: CalificacionRequest,
    db: Session = Depends(database.get_db)
):
    """Calificar una recomendación del tótem"""
    try:
        # Validar que la calificación esté en el rango correcto
        if not (1 <= calificacion.calificacion <= 5):
            raise HTTPException(
                status_code=400, 
                detail="La calificación debe estar entre 1 y 5 estrellas"
            )
        
        # Verificar que la sesión existe o crear una temporal
        sesion = db.query(Sesion).filter(
            Sesion.id_sesion == calificacion.id_sesion
        ).first()
        
        if not sesion:
            # Crear sesión temporal para calificaciones
            sesion = Sesion(
                id_sesion=calificacion.id_sesion,
                canal="calificacion",
                inicio=datetime.utcnow()
            )
            db.add(sesion)
            db.commit()
            db.refresh(sesion)
        
        # Verificar que la recomendación existe o crear una temporal
        recomendacion = db.query(RecomendacionSesion).filter(
            RecomendacionSesion.id_recomendacion == calificacion.id_recomendacion
        ).first()
        
        if not recomendacion:
            # Usar un ID más pequeño para evitar problemas de rango
            simple_id = abs(hash(calificacion.id_sesion + str(calificacion.id_recomendacion))) % 1000000
            recomendacion = RecomendacionSesion(
                id_recomendacion=simple_id,
                id_sesion=calificacion.id_sesion,
                tipo_recomendacion="frontend",
                filtros_aplicados='{"frontend": true}',
                algoritmo_usado="frontend",
                total_productos_recomendados=1,
                tiempo_generacion_ms=100,
                fecha_hora=datetime.utcnow()
            )
            db.add(recomendacion)
            db.commit()
            db.refresh(recomendacion)
        
        # Crear nueva calificación
        nueva_calificacion = CalificacionRecomendacion(
            id_sesion=calificacion.id_sesion,
            id_recomendacion=recomendacion.id_recomendacion,
            calificacion=calificacion.calificacion,
            comentario=calificacion.comentario,
            fecha_hora=datetime.utcnow()
        )
        
        db.add(nueva_calificacion)
        db.commit()
        db.refresh(nueva_calificacion)
        
        return {
            "id_calificacion": nueva_calificacion.id_calificacion,
            "calificacion": nueva_calificacion.calificacion,
            "comentario": nueva_calificacion.comentario,
            "fecha_hora": nueva_calificacion.fecha_hora,
            "tipo_recomendacion": recomendacion.tipo_recomendacion,
            "mensaje": "Calificación registrada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al calificar: {str(e)}")

@router.get("/estadisticas")
def obtener_estadisticas_calificaciones(
    dias: int = Query(7, ge=1, le=30, description="Días para analizar"),
    db: Session = Depends(database.get_db)
):
    """Obtener estadísticas de calificaciones"""
    try:
        from sqlalchemy import func
        
        # Fecha de inicio
        fecha_inicio = datetime.utcnow() - datetime.timedelta(days=dias)
        
        # Calcular promedio
        promedio = db.query(func.avg(CalificacionRecomendacion.calificacion)).filter(
            CalificacionRecomendacion.fecha_hora >= fecha_inicio
        ).scalar() or 0.0
        
        # Total de calificaciones
        total = db.query(func.count(CalificacionRecomendacion.id_calificacion)).filter(
            CalificacionRecomendacion.fecha_hora >= fecha_inicio
        ).scalar() or 0
        
        # Distribución de calificaciones
        distribucion = {}
        for i in range(1, 6):
            count = db.query(func.count(CalificacionRecomendacion.id_calificacion)).filter(
                CalificacionRecomendacion.calificacion == i,
                CalificacionRecomendacion.fecha_hora >= fecha_inicio
            ).scalar() or 0
            distribucion[i] = count
        
        # Calificaciones recientes
        calificaciones_recientes = db.query(
            CalificacionRecomendacion,
            RecomendacionSesion.producto
        ).join(
            RecomendacionSesion,
            CalificacionRecomendacion.id_recomendacion == RecomendacionSesion.id_recomendacion
        ).filter(
            CalificacionRecomendacion.fecha_hora >= fecha_inicio
        ).order_by(
            CalificacionRecomendacion.fecha_hora.desc()
        ).limit(10).all()
        
        return {
            "periodo_dias": dias,
            "promedio_calificacion": round(promedio, 2),
            "total_calificaciones": total,
            "distribucion_calificaciones": distribucion,
            "calificaciones_recientes": [
                {
                    "id_calificacion": c.id_calificacion,
                    "calificacion": c.calificacion,
                    "comentario": c.comentario,
                    "fecha_hora": c.fecha_hora,
                    "producto": producto
                }
                for c, producto in calificaciones_recientes
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/por-sesion/{id_sesion}")
def obtener_calificaciones_sesion(
    id_sesion: str,
    db: Session = Depends(database.get_db)
):
    """Obtener calificaciones de una sesión específica"""
    try:
        calificaciones = db.query(
            CalificacionRecomendacion,
            RecomendacionSesion.producto
        ).join(
            RecomendacionSesion,
            CalificacionRecomendacion.id_recomendacion == RecomendacionSesion.id_recomendacion
        ).filter(
            CalificacionRecomendacion.id_sesion == id_sesion
        ).order_by(
            CalificacionRecomendacion.fecha_hora.desc()
        ).all()
        
        return {
            "id_sesion": id_sesion,
            "total_calificaciones": len(calificaciones),
            "calificaciones": [
                {
                    "id_calificacion": c.id_calificacion,
                    "calificacion": c.calificacion,
                    "comentario": c.comentario,
                    "fecha_hora": c.fecha_hora,
                    "producto": producto
                }
                for c, producto in calificaciones
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener calificaciones: {str(e)}")

@router.get("/promedio-hoy")
def obtener_promedio_calificaciones_hoy(
    db: Session = Depends(database.get_db)
):
    """Obtener promedio de calificaciones del día actual"""
    try:
        from sqlalchemy import func
        
        today = datetime.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        
        promedio = db.query(func.avg(CalificacionRecomendacion.calificacion)).filter(
            CalificacionRecomendacion.fecha_hora >= start_of_day
        ).scalar() or 0.0
        
        total = db.query(func.count(CalificacionRecomendacion.id_calificacion)).filter(
            CalificacionRecomendacion.fecha_hora >= start_of_day
        ).scalar() or 0
        
        return {
            "fecha": today.isoformat(),
            "promedio_calificacion": round(promedio, 2),
            "total_calificaciones": total,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener promedio: {str(e)}")

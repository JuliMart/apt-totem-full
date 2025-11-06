from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import models, database
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import json

router = APIRouter(prefix="/calificaciones-grupo", tags=["Calificaciones de Grupos"])

# --- Modelos Pydantic ---
class CalificacionGrupoRequest(BaseModel):
    id_sesion: str
    tipo_grupo: str  # categoria, marca, color, estilo, etc.
    nombre_grupo: str  # nombre específico del grupo
    productos_incluidos: List[int]  # IDs de productos incluidos
    calificacion_general: int  # 1-5 estrellas
    comentario_grupo: Optional[str] = None

class CalificacionGrupoResponse(BaseModel):
    id_calificacion_grupo: int
    tipo_grupo: str
    nombre_grupo: str
    calificacion_general: int
    comentario_grupo: Optional[str]
    fecha_hora: datetime
    total_productos: int

class EstadisticasGrupos(BaseModel):
    total_calificaciones: int
    promedio_general: float
    grupos_mas_calificados: List[dict]
    calificaciones_recientes: List[CalificacionGrupoResponse]

@router.post("/calificar-grupo")
def calificar_grupo_recomendacion(
    calificacion: CalificacionGrupoRequest,
    db: Session = Depends(database.get_db)
):
    """Calificar un grupo de recomendaciones del tótem"""
    try:
        # Validar que la calificación esté en el rango correcto
        if not (1 <= calificacion.calificacion_general <= 5):
            raise HTTPException(
                status_code=400, 
                detail="La calificación debe estar entre 1 y 5 estrellas"
            )
        
        # Verificar que la sesión existe o crear una temporal
        sesion = db.query(models.Sesion).filter(
            models.Sesion.id_sesion == calificacion.id_sesion
        ).first()
        
        if not sesion:
            # Crear sesión temporal para calificaciones
            sesion = models.Sesion(
                id_sesion=calificacion.id_sesion,
                canal="calificacion_grupo",
                inicio=datetime.utcnow()
            )
            db.add(sesion)
            db.commit()
            db.refresh(sesion)
        
        # Crear nueva calificación de grupo
        nueva_calificacion = models.CalificacionGrupoRecomendacion(
            id_sesion=calificacion.id_sesion,
            tipo_grupo=calificacion.tipo_grupo,
            nombre_grupo=calificacion.nombre_grupo,
            productos_incluidos=json.dumps(calificacion.productos_incluidos),
            calificacion_general=calificacion.calificacion_general,
            comentario_grupo=calificacion.comentario_grupo,
            fecha_hora=datetime.utcnow()
        )
        
        db.add(nueva_calificacion)
        db.commit()
        db.refresh(nueva_calificacion)
        
        return {
            "id_calificacion_grupo": nueva_calificacion.id_calificacion_grupo,
            "tipo_grupo": nueva_calificacion.tipo_grupo,
            "nombre_grupo": nueva_calificacion.nombre_grupo,
            "calificacion_general": nueva_calificacion.calificacion_general,
            "comentario_grupo": nueva_calificacion.comentario_grupo,
            "fecha_hora": nueva_calificacion.fecha_hora,
            "total_productos": len(calificacion.productos_incluidos),
            "mensaje": "Calificación de grupo registrada exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al calificar grupo: {str(e)}")

@router.get("/estadisticas-grupos")
def obtener_estadisticas_grupos(
    dias: int = Query(7, ge=1, le=30, description="Días para analizar"),
    db: Session = Depends(database.get_db)
):
    """Obtener estadísticas de calificaciones por grupos"""
    try:
        # Calcular fecha límite
        fecha_limite = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_limite = fecha_limite.replace(day=fecha_limite.day - dias)
        
        # Obtener todas las calificaciones del período
        calificaciones = db.query(models.CalificacionGrupoRecomendacion).filter(
            models.CalificacionGrupoRecomendacion.fecha_hora >= fecha_limite
        ).all()
        
        if not calificaciones:
            return {
                "total_calificaciones": 0,
                "promedio_general": 0.0,
                "grupos_mas_calificados": [],
                "calificaciones_recientes": [],
                "periodo_dias": dias
            }
        
        # Calcular estadísticas generales
        total_calificaciones = len(calificaciones)
        promedio_general = sum(c.calificacion_general for c in calificaciones) / total_calificaciones
        
        # Agrupar por tipo y nombre de grupo
        grupos_stats = {}
        for cal in calificaciones:
            key = f"{cal.tipo_grupo}:{cal.nombre_grupo}"
            if key not in grupos_stats:
                grupos_stats[key] = {
                    "tipo_grupo": cal.tipo_grupo,
                    "nombre_grupo": cal.nombre_grupo,
                    "total_calificaciones": 0,
                    "promedio": 0.0,
                    "calificaciones": []
                }
            
            grupos_stats[key]["total_calificaciones"] += 1
            grupos_stats[key]["calificaciones"].append(cal.calificacion_general)
        
        # Calcular promedios por grupo
        grupos_mas_calificados = []
        for key, stats in grupos_stats.items():
            stats["promedio"] = sum(stats["calificaciones"]) / len(stats["calificaciones"])
            grupos_mas_calificados.append({
                "tipo_grupo": stats["tipo_grupo"],
                "nombre_grupo": stats["nombre_grupo"],
                "total_calificaciones": stats["total_calificaciones"],
                "promedio": round(stats["promedio"], 2)
            })
        
        # Ordenar por total de calificaciones
        grupos_mas_calificados.sort(key=lambda x: x["total_calificaciones"], reverse=True)
        
        # Obtener calificaciones recientes (últimas 10)
        calificaciones_recientes = []
        for cal in sorted(calificaciones, key=lambda x: x.fecha_hora, reverse=True)[:10]:
            productos_incluidos = json.loads(cal.productos_incluidos) if cal.productos_incluidos else []
            calificaciones_recientes.append(CalificacionGrupoResponse(
                id_calificacion_grupo=cal.id_calificacion_grupo,
                tipo_grupo=cal.tipo_grupo,
                nombre_grupo=cal.nombre_grupo,
                calificacion_general=cal.calificacion_general,
                comentario_grupo=cal.comentario_grupo,
                fecha_hora=cal.fecha_hora,
                total_productos=len(productos_incluidos)
            ))
        
        return EstadisticasGrupos(
            total_calificaciones=total_calificaciones,
            promedio_general=round(promedio_general, 2),
            grupos_mas_calificados=grupos_mas_calificados[:10],  # Top 10
            calificaciones_recientes=calificaciones_recientes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

@router.get("/grupos-disponibles")
def obtener_grupos_disponibles(
    tipo_grupo: Optional[str] = Query(None, description="Filtrar por tipo: categoria, marca, color, estilo"),
    db: Session = Depends(database.get_db)
):
    """Obtener grupos disponibles para calificar"""
    try:
        # Obtener grupos únicos de las calificaciones existentes
        query = db.query(
            models.CalificacionGrupoRecomendacion.tipo_grupo,
            models.CalificacionGrupoRecomendacion.nombre_grupo
        ).distinct()
        
        if tipo_grupo:
            query = query.filter(models.CalificacionGrupoRecomendacion.tipo_grupo == tipo_grupo)
        
        grupos = query.all()
        
        # Formatear respuesta
        grupos_disponibles = []
        for grupo in grupos:
            grupos_disponibles.append({
                "tipo_grupo": grupo.tipo_grupo,
                "nombre_grupo": grupo.nombre_grupo,
                "display_name": f"{grupo.tipo_grupo.title()}: {grupo.nombre_grupo}"
            })
        
        return {
            "grupos_disponibles": grupos_disponibles,
            "total_grupos": len(grupos_disponibles),
            "tipos_disponibles": list(set(g.tipo_grupo for g in grupos))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener grupos: {str(e)}")

@router.get("/historial-grupo/{nombre_grupo}")
def obtener_historial_grupo(
    nombre_grupo: str,
    tipo_grupo: str = Query(..., description="Tipo del grupo"),
    limit: int = Query(20, ge=1, le=100, description="Número de registros"),
    db: Session = Depends(database.get_db)
):
    """Obtener historial de calificaciones para un grupo específico"""
    try:
        calificaciones = db.query(models.CalificacionGrupoRecomendacion).filter(
            models.CalificacionGrupoRecomendacion.tipo_grupo == tipo_grupo,
            models.CalificacionGrupoRecomendacion.nombre_grupo == nombre_grupo
        ).order_by(models.CalificacionGrupoRecomendacion.fecha_hora.desc()).limit(limit).all()
        
        historial = []
        for cal in calificaciones:
            productos_incluidos = json.loads(cal.productos_incluidos) if cal.productos_incluidos else []
            historial.append({
                "id_calificacion_grupo": cal.id_calificacion_grupo,
                "id_sesion": cal.id_sesion,
                "calificacion_general": cal.calificacion_general,
                "comentario_grupo": cal.comentario_grupo,
                "fecha_hora": cal.fecha_hora,
                "total_productos": len(productos_incluidos),
                "productos_incluidos": productos_incluidos
            })
        
        # Calcular estadísticas del grupo
        if historial:
            promedio = sum(h["calificacion_general"] for h in historial) / len(historial)
            total_calificaciones = len(historial)
        else:
            promedio = 0.0
            total_calificaciones = 0
        
        return {
            "grupo": {
                "tipo_grupo": tipo_grupo,
                "nombre_grupo": nombre_grupo,
                "total_calificaciones": total_calificaciones,
                "promedio": round(promedio, 2)
            },
            "historial": historial
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")


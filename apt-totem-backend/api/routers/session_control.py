from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from database.models import Sesion
from typing import Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/session-control", tags=["Session Control"])

# Modelos Pydantic
class SessionStartRequest(BaseModel):
    canal: str = "manual"  # manual, automatic, demo
    id_dispositivo: int = 1

class SessionEndRequest(BaseModel):
    id_sesion: str

class SessionStatusResponse(BaseModel):
    id_sesion: str
    estado: str  # activa, finalizada, pausada
    inicio: datetime
    termino: Optional[datetime]
    duracion_segundos: Optional[float]
    canal: str
    id_dispositivo: int

@router.post("/iniciar")
def iniciar_sesion(
    request: SessionStartRequest,
    db: Session = Depends(database.get_db)
):
    """Iniciar una nueva sesión controlada del tótem"""
    try:
        # Verificar si ya hay una sesión activa
        sesion_activa = db.query(Sesion).filter(
            Sesion.termino.is_(None)
        ).first()
        
        if sesion_activa:
            return {
                "mensaje": "Ya existe una sesión activa",
                "sesion_activa": {
                    "id_sesion": sesion_activa.id_sesion,
                    "inicio": sesion_activa.inicio,
                    "canal": sesion_activa.canal
                },
                "accion": "finalizar_primero"
            }
        
        # Crear nueva sesión
        nueva_sesion = Sesion(
            id_sesion=str(uuid.uuid4()),
            id_dispositivo=request.id_dispositivo,
            canal=request.canal,
            inicio=datetime.utcnow()
        )
        
        db.add(nueva_sesion)
        db.commit()
        db.refresh(nueva_sesion)
        
        return {
            "mensaje": "Sesión iniciada exitosamente",
            "sesion": {
                "id_sesion": nueva_sesion.id_sesion,
                "inicio": nueva_sesion.inicio,
                "canal": nueva_sesion.canal,
                "id_dispositivo": nueva_sesion.id_dispositivo
            },
            "accion": "iniciada"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error iniciando sesión: {str(e)}")

@router.post("/finalizar")
def finalizar_sesion(
    request: SessionEndRequest,
    db: Session = Depends(database.get_db)
):
    """Finalizar una sesión activa del tótem"""
    try:
        # Buscar la sesión
        sesion = db.query(Sesion).filter(
            Sesion.id_sesion == request.id_sesion
        ).first()
        
        if not sesion:
            raise HTTPException(
                status_code=404, 
                detail="Sesión no encontrada"
            )
        
        if sesion.termino is not None:
            return {
                "mensaje": "La sesión ya estaba finalizada",
                "sesion": {
                    "id_sesion": sesion.id_sesion,
                    "inicio": sesion.inicio,
                    "termino": sesion.termino,
                    "duracion_segundos": (sesion.termino - sesion.inicio).total_seconds()
                },
                "accion": "ya_finalizada"
            }
        
        # Finalizar la sesión
        sesion.termino = datetime.utcnow()
        duracion = (sesion.termino - sesion.inicio).total_seconds()
        
        db.commit()
        db.refresh(sesion)
        
        return {
            "mensaje": "Sesión finalizada exitosamente",
            "sesion": {
                "id_sesion": sesion.id_sesion,
                "inicio": sesion.inicio,
                "termino": sesion.termino,
                "duracion_segundos": duracion,
                "duracion_minutos": round(duracion / 60, 2)
            },
            "accion": "finalizada"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error finalizando sesión: {str(e)}")

@router.get("/estado")
def obtener_estado_sesion(
    db: Session = Depends(database.get_db)
):
    """Obtener el estado actual de las sesiones"""
    try:
        # Sesión activa
        sesion_activa = db.query(Sesion).filter(
            Sesion.termino.is_(None)
        ).first()
        
        # Última sesión finalizada
        ultima_sesion = db.query(Sesion).filter(
            Sesion.termino.isnot(None)
        ).order_by(Sesion.termino.desc()).first()
        
        # Estadísticas generales
        total_sesiones = db.query(Sesion).count()
        sesiones_hoy = db.query(Sesion).filter(
            Sesion.inicio >= datetime.now().date()
        ).count()
        
        resultado = {
            "hay_sesion_activa": sesion_activa is not None,
            "total_sesiones": total_sesiones,
            "sesiones_hoy": sesiones_hoy,
            "timestamp": datetime.now().isoformat()
        }
        
        if sesion_activa:
            resultado["sesion_activa"] = {
                "id_sesion": sesion_activa.id_sesion,
                "inicio": sesion_activa.inicio,
                "canal": sesion_activa.canal,
                "id_dispositivo": sesion_activa.id_dispositivo,
                "duracion_actual_segundos": (datetime.utcnow() - sesion_activa.inicio).total_seconds()
            }
        
        if ultima_sesion:
            resultado["ultima_sesion"] = {
                "id_sesion": ultima_sesion.id_sesion,
                "inicio": ultima_sesion.inicio,
                "termino": ultima_sesion.termino,
                "duracion_segundos": (ultima_sesion.termino - ultima_sesion.inicio).total_seconds()
            }
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")

@router.post("/reiniciar-sistema")
def reiniciar_sistema(
    db: Session = Depends(database.get_db)
):
    """Reiniciar el sistema finalizando todas las sesiones activas"""
    try:
        # Finalizar todas las sesiones activas
        sesiones_activas = db.query(Sesion).filter(
            Sesion.termino.is_(None)
        ).all()
        
        sesiones_finalizadas = []
        for sesion in sesiones_activas:
            sesion.termino = datetime.utcnow()
            duracion = (sesion.termino - sesion.inicio).total_seconds()
            sesiones_finalizadas.append({
                "id_sesion": sesion.id_sesion,
                "duracion_segundos": duracion
            })
        
        db.commit()
        
        return {
            "mensaje": f"Sistema reiniciado. {len(sesiones_finalizadas)} sesiones finalizadas.",
            "sesiones_finalizadas": sesiones_finalizadas,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error reiniciando sistema: {str(e)}")

@router.get("/estadisticas")
def obtener_estadisticas_sesiones(
    dias: int = 7,
    db: Session = Depends(database.get_db)
):
    """Obtener estadísticas de sesiones de los últimos N días"""
    try:
        desde = datetime.now() - timedelta(days=dias)
        
        # Sesiones del período
        sesiones = db.query(Sesion).filter(
            Sesion.inicio >= desde
        ).all()
        
        if not sesiones:
            return {
                "periodo_dias": dias,
                "total_sesiones": 0,
                "duracion_promedio_minutos": 0,
                "sesiones_por_dia": {},
                "canales_mas_usados": {}
            }
        
        # Calcular estadísticas
        sesiones_con_duracion = [s for s in sesiones if s.termino is not None]
        
        if sesiones_con_duracion:
            duracion_promedio = sum(
                (s.termino - s.inicio).total_seconds() 
                for s in sesiones_con_duracion
            ) / len(sesiones_con_duracion)
        else:
            duracion_promedio = 0
        
        # Sesiones por día
        sesiones_por_dia = {}
        for sesion in sesiones:
            dia = sesion.inicio.date().isoformat()
            sesiones_por_dia[dia] = sesiones_por_dia.get(dia, 0) + 1
        
        # Canales más usados
        canales = {}
        for sesion in sesiones:
            canal = sesion.canal or "desconocido"
            canales[canal] = canales.get(canal, 0) + 1
        
        return {
            "periodo_dias": dias,
            "total_sesiones": len(sesiones),
            "duracion_promedio_minutos": round(duracion_promedio / 60, 2),
            "sesiones_por_dia": sesiones_por_dia,
            "canales_mas_usados": canales,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

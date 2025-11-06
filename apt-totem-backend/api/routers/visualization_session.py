from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models, database
from datetime import datetime
import uuid

router = APIRouter(prefix="/visualization-session", tags=["Sesión Visualización"])

@router.post("/create")
def create_visualization_session(db: Session = Depends(database.get_db)):
    """Crear una sesión para la página de visualización"""
    try:
        # Crear sesión con ID específico para visualización
        session_id = "visualization-session"
        
        # Verificar si ya existe
        existing_session = db.query(models.Sesion).filter(
            models.Sesion.id_sesion == session_id
        ).first()
        
        if existing_session:
            return {
                "id_sesion": existing_session.id_sesion,
                "inicio": existing_session.inicio.isoformat(),
                "message": "Sesión ya existe"
            }
        
        # Crear nueva sesión
        sesion = models.Sesion(
            id_sesion=session_id,
            canal="visualization",
            inicio=datetime.utcnow()
        )
        
        db.add(sesion)
        db.commit()
        db.refresh(sesion)
        
        return {
            "id_sesion": sesion.id_sesion,
            "inicio": sesion.inicio.isoformat(),
            "message": "Sesión creada exitosamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando sesión: {str(e)}")

@router.get("/status")
def get_session_status(db: Session = Depends(database.get_db)):
    """Obtener el estado de la sesión de visualización"""
    try:
        session_id = "visualization-session"
        
        sesion = db.query(models.Sesion).filter(
            models.Sesion.id_sesion == session_id
        ).first()
        
        if not sesion:
            return {
                "exists": False,
                "message": "Sesión no encontrada"
            }
        
        return {
            "exists": True,
            "id_sesion": sesion.id_sesion,
            "inicio": sesion.inicio.isoformat(),
            "termino": sesion.termino.isoformat() if sesion.termino else None,
            "canal": sesion.canal,
            "message": "Sesión activa"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")


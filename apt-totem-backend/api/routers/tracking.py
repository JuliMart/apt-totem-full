"""
Router para tracking de interacciones del frontend
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import database, models
from services.recommendation_tracker import get_recommendation_tracker
from typing import Dict, Optional
from datetime import datetime
import json

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.post("/interaction")
async def track_interaction(
    session_id: str = Body(..., description="ID de sesión"),
    interaction_type: str = Body(..., description="Tipo de interacción: view, click, hover, scroll, search, voice, camera"),
    variant_id: Optional[int] = Body(None, description="ID de variante si aplica"),
    metadata: Optional[Dict] = Body(None, description="Metadatos adicionales"),
    duration_seconds: Optional[float] = Body(None, description="Duración de la interacción"),
    db: Session = Depends(database.get_db)
):
    """Registrar interacción del usuario"""
    try:
        # Verificar que la sesión existe o crear una temporal
        sesion = db.query(models.Sesion).filter(
            models.Sesion.id_sesion == session_id
        ).first()
        
        if not sesion:
            # Crear sesión temporal para tracking
            sesion = models.Sesion(
                id_sesion=session_id,
                canal="tracking",
                inicio=datetime.utcnow()
            )
            db.add(sesion)
            db.commit()
            db.refresh(sesion)
            print(f"✅ Sesión temporal creada para tracking: {session_id}")
        
        tracker = get_recommendation_tracker(db)
        
        # Registrar la interacción
        interaction_id = tracker.track_user_interaction(
            session_id=session_id,
            interaction_type=interaction_type,
            variant_id=variant_id,
            metadata=metadata,
            duration_seconds=duration_seconds
        )
        
        return {
            "success": True,
            "interaction_id": interaction_id,
            "message": "Interacción registrada correctamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando interacción: {str(e)}")

@router.post("/recommendation/viewed")
async def track_recommendation_viewed(
    session_id: str = Body(..., description="ID de sesión"),
    variant_id: int = Body(..., description="ID de variante mostrada"),
    recommendation_type: str = Body(..., description="Tipo de recomendación"),
    position: Optional[int] = Body(None, description="Posición en la lista"),
    metadata: Optional[Dict] = Body(None, description="Metadatos adicionales"),
    db: Session = Depends(database.get_db)
):
    """Registrar que se mostró una recomendación"""
    try:
        # Verificar que la sesión existe o crear una temporal
        sesion = db.query(models.Sesion).filter(
            models.Sesion.id_sesion == session_id
        ).first()
        
        if not sesion:
            # Crear sesión temporal para tracking
            sesion = models.Sesion(
                id_sesion=session_id,
                canal="tracking",
                inicio=datetime.utcnow()
            )
            db.add(sesion)
            db.commit()
            db.refresh(sesion)
            print(f"✅ Sesión temporal creada para tracking: {session_id}")
        
        # Registrar interacción de vista
        tracker = get_recommendation_tracker(db)
        tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="recommendation_viewed",
            variant_id=variant_id,
            metadata={
                "recommendation_type": recommendation_type,
                "position": position,
                "screen": "recommendations",
                **(metadata or {})
            }
        )
        
        db.commit()
        
        return {
            "success": True,
            "message": "Recomendación vista registrada"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registrando vista: {str(e)}")

@router.post("/recommendation/clicked")
async def track_recommendation_clicked(
    session_id: str = Body(..., description="ID de sesión"),
    recommendation_id: int = Body(..., description="ID de recomendación"),
    variant_id: int = Body(..., description="ID de variante clicada"),
    position: int = Body(..., description="Posición en la lista"),
    db: Session = Depends(database.get_db)
):
    """Registrar clic en recomendación"""
    try:
        # Buscar el item de recomendación
        item = db.query(models.RecomendacionItem).filter(
            models.RecomendacionItem.id_recomendacion == recommendation_id,
            models.RecomendacionItem.id_variante == variant_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item de recomendación no encontrado")
        
        # Marcar como clicado
        item.fue_clicado = True
        item.fecha_clic = datetime.utcnow()
        
        # Registrar interacción de clic
        tracker = get_recommendation_tracker(db)
        tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="click",
            variant_id=variant_id,
            metadata={
                "recommendation_id": recommendation_id,
                "position": position,
                "screen": "recommendations"
            }
        )
        
        db.commit()
        
        return {
            "success": True,
            "message": "Clic registrado correctamente"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error registrando clic: {str(e)}")

@router.post("/product/click")
async def track_product_click(
    session_id: str = Body(..., description="ID de sesión"),
    variant_id: int = Body(..., description="ID de variante clicada"),
    recommendation_id: Optional[int] = Body(None, description="ID de recomendación asociada"),
    click_position: Optional[int] = Body(None, description="Posición del clic"),
    db: Session = Depends(database.get_db)
):
    """Registrar clic en producto"""
    try:
        tracker = get_recommendation_tracker(db)
        
        tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="product_click",
            variant_id=variant_id,
            metadata={
                "recommendation_id": recommendation_id,
                "click_position": click_position,
                "screen": "recommendations"
            }
        )
        
        return {
            "success": True,
            "message": "Clic en producto registrado"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando clic: {str(e)}")

@router.post("/search")
async def track_search(
    session_id: str = Body(..., description="ID de sesión"),
    query: str = Body(..., description="Término de búsqueda"),
    results_count: int = Body(..., description="Número de resultados"),
    search_time_ms: Optional[int] = Body(None, description="Tiempo de búsqueda en ms"),
    db: Session = Depends(database.get_db)
):
    """Registrar búsqueda del usuario"""
    try:
        tracker = get_recommendation_tracker(db)
        
        tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="search",
            metadata={
                "query": query,
                "results_count": results_count,
                "search_time_ms": search_time_ms,
                "screen": "search"
            }
        )
        
        return {
            "success": True,
            "message": "Búsqueda registrada correctamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando búsqueda: {str(e)}")

@router.post("/voice")
async def track_voice_interaction(
    session_id: str = Body(..., description="ID de sesión"),
    transcription: str = Body(..., description="Transcripción"),
    intent: str = Body(..., description="Intención detectada"),
    confidence: float = Body(..., description="Confianza de la intención"),
    processing_time_ms: Optional[int] = Body(None, description="Tiempo de procesamiento"),
    db: Session = Depends(database.get_db)
):
    """Registrar interacción de voz"""
    try:
        tracker = get_recommendation_tracker(db)
        
        tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="voice",
            metadata={
                "transcription": transcription,
                "intent": intent,
                "confidence": confidence,
                "processing_time_ms": processing_time_ms,
                "screen": "voice"
            }
        )
        
        return {
            "success": True,
            "message": "Interacción de voz registrada"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando voz: {str(e)}")

@router.post("/camera")
async def track_camera_detection(
    session_id: str = Body(..., description="ID de sesión"),
    detected_item: str = Body(..., description="Item detectado"),
    color: str = Body(..., description="Color detectado"),
    confidence: float = Body(..., description="Confianza de detección"),
    processing_time_ms: Optional[int] = Body(None, description="Tiempo de procesamiento"),
    db: Session = Depends(database.get_db)
):
    """Registrar detección de cámara"""
    try:
        tracker = get_recommendation_tracker(db)
        
        tracker.track_user_interaction(
            session_id=session_id,
            interaction_type="camera_detection",
            metadata={
                "detected_item": detected_item,
                "color": color,
                "confidence": confidence,
                "processing_time_ms": processing_time_ms,
                "screen": "camera"
            }
        )
        
        return {
            "success": True,
            "message": "Detección de cámara registrada"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando cámara: {str(e)}")

@router.get("/session/{session_id}/metrics")
async def get_session_metrics(
    session_id: str,
    db: Session = Depends(database.get_db)
):
    """Obtener métricas de una sesión específica"""
    try:
        tracker = get_recommendation_tracker(db)
        metrics = tracker.calculate_session_metrics(session_id)
        
        return {
            "session_id": session_id,
            "metrics": metrics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")

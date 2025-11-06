"""
Router para gestión de turnos y análisis de detecciones
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.database import get_db
from services.shift_manager import ShiftManager
from database.models import Turno, ResumenTurno, DeteccionBuffer
from datetime import datetime, timedelta
from typing import List, Optional
import json

router = APIRouter(prefix="/shifts", tags=["Turnos y Detecciones"])


@router.get("/current")
def get_current_shift(db: Session = Depends(get_db)):
    """Obtiene el turno activo actual"""
    manager = ShiftManager(db)
    turno = manager.get_current_shift()
    
    if not turno:
        raise HTTPException(status_code=404, detail="No hay turno activo")
    
    return {
        "id_turno": turno.id_turno,
        "nombre": turno.nombre_turno,
        "fecha": turno.fecha.isoformat() if turno.fecha else None,
        "hora_inicio": turno.hora_inicio.isoformat() if turno.hora_inicio else None,
        "hora_fin": turno.hora_fin.isoformat() if turno.hora_fin else None,
        "estado": turno.estado,
        "total_detecciones": turno.total_detecciones,
        "total_clientes": turno.total_clientes_detectados
    }


@router.post("/create")
def create_shift(
    nombre_turno: str = Query(..., description="Nombre del turno (matutino, vespertino, nocturno)"),
    db: Session = Depends(get_db)
):
    """Crea un nuevo turno manualmente"""
    manager = ShiftManager(db)
    turno = manager.create_shift(nombre_turno)
    
    return {
        "message": f"Turno {nombre_turno} creado exitosamente",
        "id_turno": turno.id_turno,
        "nombre": turno.nombre_turno,
        "hora_inicio": turno.hora_inicio.isoformat()
    }


@router.post("/{id_turno}/close")
def close_shift(id_turno: int, db: Session = Depends(get_db)):
    """Cierra un turno y genera su resumen"""
    manager = ShiftManager(db)
    turno = manager.close_shift(id_turno)
    
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    return {
        "message": f"Turno {turno.nombre_turno} cerrado exitosamente",
        "id_turno": turno.id_turno,
        "total_detecciones": turno.total_detecciones,
        "total_clientes": turno.total_clientes_detectados,
        "hora_fin": turno.hora_fin.isoformat()
    }


@router.get("/{id_turno}/stats")
def get_shift_stats(id_turno: int, db: Session = Depends(get_db)):
    """Obtiene estadísticas completas de un turno"""
    manager = ShiftManager(db)
    stats = manager.get_shift_stats(id_turno)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    return stats


@router.get("/{id_turno}/summary")
def get_shift_summary(id_turno: int, db: Session = Depends(get_db)):
    """Obtiene el resumen de un turno"""
    resumen = db.query(ResumenTurno).filter(
        ResumenTurno.id_turno == id_turno
    ).first()
    
    if not resumen:
        raise HTTPException(status_code=404, detail="Resumen no encontrado")
    
    return {
        "id_resumen": resumen.id_resumen,
        "id_turno": resumen.id_turno,
        "fecha_generacion": resumen.fecha_generacion.isoformat(),
        "estadisticas": {
            "total_detecciones": resumen.total_detecciones,
            "total_personas": resumen.total_personas_detectadas,
            "total_prendas": resumen.total_prendas_detectadas,
            "total_accesorios": resumen.total_accesorios_detectados,
            "confianza_promedio": round(resumen.confianza_promedio, 2)
        },
        "demografía": {
            "distribucion_edad": json.loads(resumen.distribucion_edad)
        },
        "preferencias": {
            "estilos": json.loads(resumen.estilos_detectados),
            "colores": json.loads(resumen.colores_predominantes),
            "prendas": json.loads(resumen.prendas_mas_vistas),
            "accesorios": json.loads(resumen.accesorios_mas_vistos)
        },
        "insights": {
            "perfil_predominante": json.loads(resumen.perfil_cliente_predominante),
            "recomendaciones_inventario": json.loads(resumen.recomendaciones_inventario)
        }
    }


@router.get("/list")
def list_shifts(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    estado: Optional[str] = Query(None, description="Filtrar por estado (activo, cerrado)"),
    db: Session = Depends(get_db)
):
    """Lista todos los turnos con paginación"""
    query = db.query(Turno)
    
    if estado:
        query = query.filter(Turno.estado == estado)
    
    total = query.count()
    turnos = query.order_by(Turno.fecha.desc(), Turno.hora_inicio.desc()).offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "turnos": [
            {
                "id_turno": t.id_turno,
                "nombre": t.nombre_turno,
                "fecha": t.fecha.isoformat() if t.fecha else None,
                "hora_inicio": t.hora_inicio.isoformat() if t.hora_inicio else None,
                "hora_fin": t.hora_fin.isoformat() if t.hora_fin else None,
                "estado": t.estado,
                "total_detecciones": t.total_detecciones,
                "total_clientes": t.total_clientes_detectados
            }
            for t in turnos
        ]
    }


@router.get("/{id_turno}/detections")
def get_shift_detections(
    id_turno: int,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Obtiene las detecciones individuales de un turno"""
    query = db.query(DeteccionBuffer).filter(DeteccionBuffer.id_turno == id_turno)
    
    total = query.count()
    detecciones = query.order_by(DeteccionBuffer.fecha_hora.desc()).offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "detecciones": [
            {
                "id": d.id_buffer,
                "fecha_hora": d.fecha_hora.isoformat(),
                "persona_detectada": d.persona_detectada,
                "rango_edad": d.rango_edad,
                "estilo": d.estilo_ropa,
                "color_principal": d.color_principal,
                "color_secundario": d.color_secundario,
                "prenda": d.prenda_detectada,
                "accesorio": d.accesorio_cabeza,
                "confianza": round(d.confianza_deteccion, 2),
                "motor": d.motor_deteccion,
                "fuente": d.fuente_camara
            }
            for d in detecciones
        ]
    }


@router.get("/analytics/today")
def get_today_analytics(db: Session = Depends(get_db)):
    """Obtiene analytics del día actual"""
    hoy = datetime.utcnow().date()
    
    # Obtener todos los turnos de hoy
    turnos_hoy = db.query(Turno).filter(
        Turno.fecha >= hoy
    ).all()
    
    total_detecciones = sum(t.total_detecciones for t in turnos_hoy)
    total_clientes = sum(t.total_clientes_detectados for t in turnos_hoy)
    
    # Obtener resumenes
    resumenes = []
    for turno in turnos_hoy:
        resumen = db.query(ResumenTurno).filter(
            ResumenTurno.id_turno == turno.id_turno
        ).first()
        if resumen:
            resumenes.append(resumen)
    
    # Consolidar datos
    todos_colores = {}
    todas_prendas = {}
    todas_edades = {}
    
    for resumen in resumenes:
        if resumen.colores_predominantes:
            colores = json.loads(resumen.colores_predominantes)
            for color, count in colores.items():
                todos_colores[color] = todos_colores.get(color, 0) + count
        
        if resumen.prendas_mas_vistas:
            prendas = json.loads(resumen.prendas_mas_vistas)
            for prenda, count in prendas.items():
                todas_prendas[prenda] = todas_prendas.get(prenda, 0) + count
        
        if resumen.distribucion_edad:
            edades = json.loads(resumen.distribucion_edad)
            for edad, count in edades.items():
                todas_edades[edad] = todas_edades.get(edad, 0) + count
    
    return {
        "fecha": hoy.isoformat(),
        "total_turnos": len(turnos_hoy),
        "total_detecciones": total_detecciones,
        "total_clientes": total_clientes,
        "colores_del_dia": dict(sorted(todos_colores.items(), key=lambda x: x[1], reverse=True)[:5]),
        "prendas_del_dia": dict(sorted(todas_prendas.items(), key=lambda x: x[1], reverse=True)[:5]),
        "demografia_del_dia": todas_edades,
        "turnos": [
            {
                "nombre": t.nombre_turno,
                "hora_inicio": t.hora_inicio.isoformat() if t.hora_inicio else None,
                "hora_fin": t.hora_fin.isoformat() if t.hora_fin else None,
                "detecciones": t.total_detecciones,
                "clientes": t.total_clientes_detectados,
                "estado": t.estado
            }
            for t in turnos_hoy
        ]
    }


@router.post("/{id_turno}/regenerate-summary")
def regenerate_summary(id_turno: int, db: Session = Depends(get_db)):
    """Regenera el resumen de un turno manualmente"""
    manager = ShiftManager(db)
    resumen = manager.generate_shift_summary(id_turno)
    
    if not resumen:
        raise HTTPException(
            status_code=404,
            detail="No se pudo generar el resumen (turno no encontrado o sin detecciones)"
        )
    
    return {
        "message": "Resumen regenerado exitosamente",
        "id_resumen": resumen.id_resumen,
        "total_detecciones": resumen.total_detecciones,
        "total_personas": resumen.total_personas_detectadas
    }


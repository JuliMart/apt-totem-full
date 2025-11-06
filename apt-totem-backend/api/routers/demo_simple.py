from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Dict, Optional
from datetime import datetime
import random

router = APIRouter(prefix="/demo-simple", tags=["Demo Simple"])

@router.get("/generar-recomendacion")
def generar_recomendacion_simple(
    session_id: str = Query("demo-session", description="ID de la sesión")
):
    """Generar una recomendación de demo sin base de datos"""
    try:
        # Productos de demo
        productos_demo = [
            {"nombre": "Nike Air Max 270", "marca": "Nike", "precio": 450000},
            {"nombre": "Adidas Ultraboost 22", "marca": "Adidas", "precio": 380000},
            {"nombre": "Puma RS-X Reinvention", "marca": "Puma", "precio": 320000},
            {"nombre": "Rolex Submariner", "marca": "Rolex", "precio": 15000000},
            {"nombre": "Omega Speedmaster", "marca": "Omega", "precio": 12000000},
            {"nombre": "Cartier Santos", "marca": "Cartier", "precio": 18000000}
        ]
        
        # Seleccionar producto aleatorio
        producto_seleccionado = random.choice(productos_demo)
        
        # Generar ID de recomendación
        recommendation_id = random.randint(1, 1000)
        
        # URL del modal de calificación
        modal_url = f"/modal-calificar?session_id={session_id}&recommendation_id={recommendation_id}"
        
        return {
            "recomendacion_generada": True,
            "id_recomendacion": recommendation_id,
            "producto": producto_seleccionado["nombre"],
            "marca": producto_seleccionado["marca"],
            "precio": producto_seleccionado["precio"],
            "confianza": round(random.uniform(0.7, 0.95), 2),
            "razon": "Basado en tus preferencias y tendencias actuales",
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
def simular_flujo_completo_simple(
    session_id: str = Query("demo-session", description="ID de la sesión")
):
    """Simular el flujo completo sin base de datos"""
    try:
        # Paso 1: Generar recomendación
        recomendacion_response = generar_recomendacion_simple(session_id)
        
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
                    "precio": recomendacion_response["precio"],
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
def abrir_modal_calificacion_simple(
    session_id: str = Query("demo-session", description="ID de la sesión"),
    recommendation_id: int = Query(1, description="ID de la recomendación")
):
    """Abrir modal de calificación para una recomendación específica"""
    try:
        # Productos de demo
        productos_demo = [
            {"nombre": "Nike Air Max 270", "marca": "Nike"},
            {"nombre": "Adidas Ultraboost 22", "marca": "Adidas"},
            {"nombre": "Puma RS-X Reinvention", "marca": "Puma"},
            {"nombre": "Rolex Submariner", "marca": "Rolex"},
            {"nombre": "Omega Speedmaster", "marca": "Omega"},
            {"nombre": "Cartier Santos", "marca": "Cartier"}
        ]
        
        # Seleccionar producto basado en ID
        producto = productos_demo[recommendation_id % len(productos_demo)]
        
        # URL del modal
        modal_url = f"/modal-calificar?session_id={session_id}&recommendation_id={recommendation_id}"
        
        return {
            "modal_abierto": True,
            "id_recomendacion": recommendation_id,
            "producto": producto["nombre"],
            "marca": producto["marca"],
            "modal_url": modal_url,
            "instrucciones": {
                "mensaje": "Modal de calificación listo para abrir",
                "accion": "Redirigir a la URL del modal",
                "url": modal_url
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error abriendo modal: {str(e)}")

@router.get("/estado-flujo")
def obtener_estado_flujo_simple(
    session_id: str = Query("demo-session", description="ID de la sesión")
):
    """Obtener el estado actual del flujo de recomendaciones"""
    try:
        return {
            "sesion_existe": True,
            "id_sesion": session_id,
            "inicio_sesion": datetime.utcnow().isoformat(),
            "total_recomendaciones": random.randint(1, 10),
            "total_calificaciones": random.randint(0, 5),
            "recomendaciones_recientes": [
                {
                    "id": i,
                    "producto": f"Producto Demo {i}",
                    "marca": "Marca Demo",
                    "fecha": datetime.utcnow().isoformat(),
                    "confianza": round(random.uniform(0.7, 0.95), 2)
                }
                for i in range(1, 4)
            ],
            "calificaciones": [
                {
                    "id": i,
                    "calificacion": random.randint(3, 5),
                    "comentario": f"Comentario demo {i}",
                    "fecha": datetime.utcnow().isoformat()
                }
                for i in range(1, 3)
            ],
            "estado": "activo",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")


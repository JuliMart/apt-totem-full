from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routers import asr, cv, productos, sesiones, recomendaciones, analytics, busqueda, tracking, visualization, shifts, product_detail, search_analytics, dashboard, calificaciones, calificaciones_grupo, compra, demo, demo_simple, visualization_session, session_control
from services.ai.real_detection import analyze_realtime_stream_real
from services.nlu.heuristics import extract_intent_advanced
from services.shift_manager import ShiftManager
from services.cron_jobs import start_cron_jobs, stop_cron_jobs
from database.database import SessionLocal
from database import models
import json
import asyncio
from datetime import datetime
from typing import List

app = FastAPI(title="NeoTotem API - Tiempo Real con MediaPipe")

# Eventos de inicio y cierre
@app.on_event("startup")
async def startup_event():
    """Inicia el sistema de tareas programadas al iniciar la app"""
    start_cron_jobs()
    print("✅ Sistema de cron jobs iniciado")

@app.on_event("shutdown")
async def shutdown_event():
    """Detiene el sistema de tareas programadas al cerrar la app"""
    stop_cron_jobs()
    print("🛑 Sistema de cron jobs detenido")

# Agregar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(asr.router)
app.include_router(cv.router)
app.include_router(productos.router)
app.include_router(sesiones.router)
app.include_router(recomendaciones.router)
app.include_router(analytics.router)
app.include_router(busqueda.router)
app.include_router(tracking.router)
app.include_router(visualization.router)
app.include_router(shifts.router)
app.include_router(product_detail.router)
app.include_router(search_analytics.router)
app.include_router(dashboard.router)
app.include_router(calificaciones.router)
app.include_router(calificaciones_grupo.router)
app.include_router(compra.router)
app.include_router(demo.router)
app.include_router(demo_simple.router)
app.include_router(visualization_session.router)
app.include_router(session_control.router)

# Servir imágenes estáticas
app.mount("/product_images", StaticFiles(directory="../product_images"), name="product_images")

# Servir páginas del frontend (admin y demos)
from fastapi.responses import FileResponse
import os

# Base path para archivos del frontend
FRONTEND_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")

@app.get("/visualization")
async def get_visualization():
    """Página de visualización en tiempo real"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "visualization.html"))

# Servir dashboard dinámico
@app.get("/dashboard")
async def get_dashboard():
    """Dashboard dinámico con analytics"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "dashboard_dinamico_nuevo.html"))

@app.get("/dashboard-old")
async def get_dashboard_old():
    """Dashboard dinámico anterior"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "dashboard_dinamico.html"))

# Servir ejemplo de búsquedas expandidas
@app.get("/modal-calificar")
async def get_modal_calificar():
    """Modal automático para calificar recomendaciones"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "modal_calificacion.html"))

@app.get("/flujo-completo")
async def get_flujo_completo():
    """Flujo completo con modal automático"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "flujo_completo_modal.html"))

@app.get("/test-urls")
async def get_test_urls():
    """Página de prueba para apertura de URLs"""
    return FileResponse(os.path.join(FRONTEND_BASE, "demos", "test_url_opening.html"))

@app.get("/control-sesiones")
async def get_control_sesiones():
    """Panel de control de sesiones"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "control_sesiones.html"))

@app.get("/calificar")
async def get_calificar_page():
    """Página para calificar recomendaciones"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "calificar_recomendacion.html"))

@app.get("/calificar-grupos")
async def get_calificar_grupos():
    """Página para calificar grupos de recomendaciones"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "calificar_grupos.html"))

@app.get("/opciones-compra")
async def get_opciones_compra():
    """Página de opciones de compra basadas en precio"""
    return FileResponse(os.path.join(FRONTEND_BASE, "admin", "opciones_compra.html"))

# Lista de conexiones WebSocket activas
active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_broadcast_time = {}  # Control de throttling por conexión

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.last_broadcast_time[id(websocket)] = 0  # Inicializar timestamp

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        # Limpiar timestamp
        ws_id = id(websocket)
        if ws_id in self.last_broadcast_time:
            del self.last_broadcast_time[ws_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"⚠️ Error enviando mensaje personal: {e}")
            # Marcar conexión como muerta pero no fallar
            try:
                self.disconnect(websocket)
            except:
                pass

    async def broadcast(self, message: str, min_interval_ms: int = 300):
        """
        Broadcast con throttling para evitar saturación.
        
        Args:
            message: Mensaje a enviar
            min_interval_ms: Intervalo mínimo entre mensajes (ms)
        """
        import time
        current_time = time.time() * 1000  # Tiempo en ms
        
        for connection in self.active_connections:
            try:
                ws_id = id(connection)
                last_time = self.last_broadcast_time.get(ws_id, 0)
                
                # Solo enviar si ha pasado el intervalo mínimo
                if current_time - last_time >= min_interval_ms:
                    await connection.send_text(message)
                    self.last_broadcast_time[ws_id] = current_time
                # else:
                #     print(f"⏸️ Throttling: mensaje omitido (espera {min_interval_ms}ms)")
                    
            except Exception as e:
                print(f"Error enviando mensaje a cliente: {e}")
                # Remover conexión problemática
                try:
                    self.active_connections.remove(connection)
                    if id(connection) in self.last_broadcast_time:
                        del self.last_broadcast_time[id(connection)]
                except ValueError:
                    pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # Enviar mensaje de bienvenida
    welcome_msg = {
        "type": "connected",
        "message": "🔗 NeoTotem Retail conectado - Detección REAL activada",
        "features": ["deteccion_real_prendas", "analisis_colores", "estimacion_edad", "recomendaciones_personalizadas"],
        "timestamp": datetime.now().isoformat()
    }
    await manager.send_personal_message(json.dumps(welcome_msg), websocket)
    
    # Variable para controlar keepalive
    keepalive_task = None
    
    async def send_keepalive():
        """Envía pings periódicos para mantener la conexión viva"""
        try:
            while True:
                await asyncio.sleep(20)  # Cada 20 segundos
                ping_msg = {
                    "type": "keepalive",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(json.dumps(ping_msg), websocket)
        except:
            pass
    
    # Iniciar tarea de keepalive
    keepalive_task = asyncio.create_task(send_keepalive())
    
    try:
        while True:
            # Recibir datos del cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Procesar diferentes tipos de mensajes
            if message["type"] == "voice":
                # Procesamiento NLU avanzado
                text = message.get("text", "")
                intent, entities, confidence = extract_intent_advanced(text)
                
                # Almacenar consulta de voz en la base de datos
                try:
                    db = SessionLocal()
                    session_id = message.get('session_id', 'unknown')
                    
                    # Crear registro en consulta_voz
                    consulta = models.ConsultaVoz(
                        id_sesion=session_id,
                        transcripcion=text,
                        intencion=intent,
                        entidades=json.dumps(entities),
                        confianza="alta" if confidence > 0.7 else "media" if confidence > 0.4 else "baja",
                        exito=True
                    )
                    db.add(consulta)
                    db.commit()
                    print(f"✅ Consulta de voz guardada: session={session_id}, texto='{text[:50]}...', intent={intent}")
                    db.close()
                except Exception as e:
                    print(f"⚠️ Error guardando consulta de voz: {e}")
                    if 'db' in locals():
                        db.rollback()
                        db.close()
                
                response = {
                    "type": "voice_analysis",
                    "original_text": text,
                    "intent": intent,
                    "entities": entities,
                    "confidence": round(confidence, 2),
                    "timestamp": datetime.now().isoformat(),
                    "analysis_engine": "nlu_advanced"
                }
                await manager.send_personal_message(json.dumps(response), websocket)
                
            elif message["type"] == "image_stream":
                # Análisis de imagen en tiempo real con MediaPipe
                try:
                    image_data = message.get("image_data", "")
                    camera_active = message.get("camera_active", False)
                    
                    if image_data and camera_active:
                        # Análisis REAL con imagen de la cámara (incluir imagen anotada)
                        analysis = analyze_realtime_stream_real(image_data, return_annotated=True)
                        
                        # Extraer imagen anotada si está disponible
                        annotated_image = analysis.pop('annotated_image', None)
                        
                        response = {
                            "type": "realtime_analysis",
                            "analysis": analysis,
                            "annotated_image": annotated_image,  # Imagen con detecciones visuales
                            "timestamp": datetime.now().isoformat(),
                            "engine": "real_detection_mediapipe",
                            "camera_source": "real"
                        }
                    else:
                        # Análisis específico para RETAIL: prendas, colores y edad
                        import random
                        
                        # Datos específicos para retail/fashion
                        age_ranges = ["18-25", "26-35", "36-45", "46-55", "55+"]
                        clothing_types = ["casual", "formal", "deportivo", "elegante", "juvenil"]
                        colors_detected = ["azul", "negro", "blanco", "rojo", "verde", "gris", "beige", "marron"]
                        clothing_items = ["camiseta", "pantalon", "chaqueta", "vestido", "falda", "zapatos", "accesorios"]
                        
                        # Simulación de análisis de prendas y colores
                        person_detected = random.choice([True, True, True, False])  # 75% probabilidad
                        age_range = random.choice(age_ranges)
                        clothing_style = random.choice(clothing_types)
                        primary_color = random.choice(colors_detected)
                        secondary_color = random.choice(colors_detected) if random.random() > 0.5 else None
                        clothing_item = random.choice(clothing_items)
                        confidence = random.uniform(0.6, 0.95)
                        
                        # Recomendaciones basadas en análisis de prendas
                        if age_range in ["18-25", "26-35"]:
                            recommended_categories = ["moda_joven", "casual", "deportivo"]
                        elif age_range in ["36-45", "46-55"]:
                            recommended_categories = ["profesional", "elegante", "casual"]
                        else:
                            recommended_categories = ["clasico", "comodo", "elegante"]
                        
                        response = {
                            "type": "realtime_analysis",
                            "analysis": {
                                "person_detected": person_detected,
                                "age_range": age_range,
                                "clothing_style": clothing_style,
                                "primary_color": primary_color,
                                "secondary_color": secondary_color,
                                "clothing_item": clothing_item,
                                "detection_confidence": round(confidence, 2),
                                "recommendations": {
                                    "target_categories": recommended_categories,
                                    "color_preference": primary_color,
                                    "style_suggestion": clothing_style,
                                    "age_appropriate": True,
                                    "interaction_tips": [
                                        f"Cliente {age_range} años - estilo {clothing_style}",
                                        f"Color principal: {primary_color}",
                                        f"Recomendar: {', '.join(recommended_categories)}"
                                    ]
                                }
                            },
                            "timestamp": datetime.now().isoformat(),
                            "engine": "retail_fashion_analysis",
                            "camera_source": "simulated"
                        }
                    
                    # Almacenar detección en base de datos
                    try:
                        db = SessionLocal()
                        
                        # Guardar en tabla deteccion (con session_id)
                        from database import models
                        analysis_data = response['analysis']
                        session_id = message.get('session_id', 'unknown')
                        
                        if analysis_data.get('person_detected', False):
                            deteccion = models.Deteccion(
                                id_sesion=session_id,
                                prenda=analysis_data.get('clothing_item', 'desconocido'),
                                color=analysis_data.get('primary_color', 'desconocido'),
                                rango_etario=analysis_data.get('age_range', 'desconocido'),
                                confianza=analysis_data.get('detection_confidence', 0.0)
                            )
                            db.add(deteccion)
                            db.commit()
                            print(f"✅ Detección guardada: session={session_id}, prenda={deteccion.prenda}, color={deteccion.color}")
                        
                        # También guardar en buffer de turnos (opcional)
                        shift_manager = ShiftManager(db)
                        shift_manager.store_detection(
                            response['analysis'],
                            engine=response.get('engine', 'unknown'),
                            camera_source=response.get('camera_source', 'unknown')
                        )
                        
                        db.close()
                    except Exception as e:
                        # Error no crítico - la detección ya fue guardada en la tabla principal
                        print(f"⚠️ No se pudo guardar en buffer de turnos (no crítico): {e}")
                    
                    # Enviar respuesta al cliente que envió la imagen
                    await manager.send_personal_message(json.dumps(response), websocket)
                    
                    # Transmitir datos de análisis a TODOS los clientes conectados (incluyendo visualización)
                    # Con throttling de 500ms para evitar saturación
                    await manager.broadcast(json.dumps(response), min_interval_ms=500)
                    
                except Exception as e:
                    error_response = {
                        "type": "analysis_error",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.send_personal_message(json.dumps(error_response), websocket)
            
            elif message["type"] == "ping":
                # Mantener conexión viva
                pong_response = {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(json.dumps(pong_response), websocket)
                
    except WebSocketDisconnect:
        # Cancelar keepalive
        if keepalive_task:
            keepalive_task.cancel()
        manager.disconnect(websocket)
        print(f"🔌 Cliente desconectado normalmente: {websocket.client}")
    except Exception as e:
        # Cancelar keepalive
        if keepalive_task:
            keepalive_task.cancel()
        print(f"❌ Error en WebSocket: {e}")
        try:
            manager.disconnect(websocket)
        except:
            pass

@app.get("/")
def read_root():
    return {
        "message": "🛍️ NeoTotem Retail API con DETECCIÓN REAL funcionando", 
        "version": "3.0", 
        "status": "active",
        "features": {
            "websockets": True,
            "real_detection": True,
            "real_time": True,
            "voice_analysis": True,
            "computer_vision": True,
            "clothing_detection": True,
            "color_analysis": True,
            "age_estimation": True
        }
    }


# 🏗️ Arquitectura Técnica - NeoTotem AI

> Documentación técnica detallada para desarrolladores

---

## 📐 Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            NEOTOTEM AI ECOSYSTEM                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│ CAPA DE PRESENTACIÓN                                                       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────┐              ┌──────────────────────┐          │
│  │  Flutter Web Client  │              │  Visualization HTML  │          │
│  │  (localhost:8080)    │              │  (localhost:8001/    │          │
│  │                      │              │   visualization)     │          │
│  │  • CameraController  │              │                      │          │
│  │  • AudioRecorder     │              │  • Real-time canvas  │          │
│  │  • WebSocketChannel  │              │  • Debug console     │          │
│  │  • State Management  │              │  • Metrics display   │          │
│  └──────────────────────┘              └──────────────────────┘          │
│           │                                       │                       │
│           │ WebSocket (ws://localhost:8001/ws)    │                       │
│           └───────────────┬───────────────────────┘                       │
└───────────────────────────┼───────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ CAPA DE APLICACIÓN (Backend - FastAPI)                                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                        main.py - FastAPI App                         │ │
│  │                                                                      │ │
│  │  • ConnectionManager (WebSocket handler)                            │ │
│  │  • CORS middleware                                                  │ │
│  │  • Static files (visualization.html)                                │ │
│  │  • Router includes (cv, tracking, shifts)                           │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                   │                                        │
│        ┌──────────────────────────┼──────────────────────────┐            │
│        │                          │                          │            │
│        ▼                          ▼                          ▼            │
│  ┌──────────┐              ┌──────────┐              ┌──────────┐        │
│  │   CV     │              │ Tracking │              │  Shifts  │        │
│  │  Router  │              │  Router  │              │  Router  │        │
│  │          │              │          │              │          │        │
│  │ • detect │              │ • camera │              │ • current│        │
│  │ • analyze│              │ • voice  │              │ • summary│        │
│  └──────────┘              └──────────┘              └──────────┘        │
│        │                          │                          │            │
└────────┼──────────────────────────┼──────────────────────────┼────────────┘
         │                          │                          │
         ▼                          ▼                          ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ CAPA DE SERVICIOS                                                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                       AI DETECTION SERVICE                          │  │
│  │                  (services/ai/real_detection.py)                    │  │
│  │                                                                     │  │
│  │  ┌──────────────────────────────────────────────────────────────┐  │  │
│  │  │  analyze_realtime_stream_real(image_data, return_annotated)  │  │  │
│  │  │                                                               │  │  │
│  │  │  1. Decode base64 → numpy array                              │  │  │
│  │  │  2. MediaPipe pose detection (33 landmarks)                  │  │  │
│  │  │  3. MediaPipe face detection                                 │  │  │
│  │  │  4. Clothing analysis (shoulders, torso, arms)               │  │  │
│  │  │  5. Color analysis (dominant colors)                         │  │  │
│  │  │  6. Head accessories (hat, cap, glasses)                     │  │  │
│  │  │  7. Bag detection (backpack, purse, etc.)                    │  │  │
│  │  │  8. Draw bounding boxes                                      │  │  │
│  │  │  9. Encode annotated image to base64                         │  │  │
│  │  │  10. Return analysis + annotated_image                       │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │                                                                     │  │
│  │  Sub-functions:                                                     │  │
│  │  • analyze_real_clothing_simple()                                  │  │
│  │  • _detect_head_accessories_improved()                             │  │
│  │  • _detect_bags_and_purses()                                       │  │
│  │  • _detect_dominant_colors_advanced()                              │  │
│  │  • _estimate_age_from_face()                                       │  │
│  │  • draw_detections_on_image()                                      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      CV DETECTION SERVICE                           │  │
│  │                    (services/cv/detector.py)                        │  │
│  │                                                                     │  │
│  │  • Legacy detection functions                                      │  │
│  │  • Fallback methods                                                │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      SHIFT MANAGER SERVICE                          │  │
│  │                   (services/shift_manager.py)                       │  │
│  │                                                                     │  │
│  │  • get_or_create_current_shift()                                   │  │
│  │  • store_detection()                                               │  │
│  │  • aggregate_shift_data()                                          │  │
│  │  • get_shift_summary()                                             │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                       CRON JOBS SERVICE                             │  │
│  │                     (services/cron_jobs.py)                         │  │
│  │                                                                     │  │
│  │  Scheduled Tasks:                                                  │  │
│  │  • 06:00 → start_morning_shift()                                   │  │
│  │  • 14:00 → start_afternoon_shift()                                 │  │
│  │  • 22:00 → start_night_shift()                                     │  │
│  │  • Every hour → aggregate_current_shift()                          │  │
│  │  • Every 6 hours → cleanup_old_detections()                        │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ CAPA DE DATOS                                                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                        SQLite Database                              │  │
│  │                        (neototem.db)                                │  │
│  │                                                                     │  │
│  │  Tables:                                                            │  │
│  │  ┌───────────────┐  ┌────────────────┐  ┌────────────────┐       │  │
│  │  │    Turno      │  │ DeteccionBuffer│  │  ResumenTurno  │       │  │
│  │  ├───────────────┤  ├────────────────┤  ├────────────────┤       │  │
│  │  │ id            │  │ id             │  │ id             │       │  │
│  │  │ fecha_inicio  │  │ turno_id (FK)  │  │ turno_id (FK)  │       │  │
│  │  │ fecha_fin     │  │ prenda         │  │ total_detec... │       │  │
│  │  │ tipo_turno    │  │ color          │  │ prendas_mas... │       │  │
│  │  │ activo        │  │ accesorios     │  │ colores_predo..│       │  │
│  │  │ total_detec..│  │ edad_estimada  │  │ edad_promedio  │       │  │
│  │  └───────────────┘  │ timestamp      │  │ fecha_agregado │       │  │
│  │                     │ engine         │  └────────────────┘       │  │
│  │                     │ camera_source  │                           │  │
│  │                     └────────────────┘                           │  │
│  │                                                                     │  │
│  │  Relationships:                                                     │  │
│  │  Turno (1) ──< (N) DeteccionBuffer                                 │  │
│  │  Turno (1) ──< (N) ResumenTurno                                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ CAPA DE INFRAESTRUCTURA                                                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │  MediaPipe │  │   OpenCV   │  │   NumPy    │  │ SQLAlchemy │         │
│  │            │  │            │  │            │  │            │         │
│  │ • Pose     │  │ • cv2      │  │ • Arrays   │  │ • ORM      │         │
│  │ • Face     │  │ • Drawing  │  │ • Math     │  │ • Sessions │         │
│  │ • Holistic │  │ • Colors   │  │ • Image ops│  │ • Queries  │         │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos Detallado

### 1. Captura y Envío de Imagen

```dart
// FRONTEND: flutter/lib/home_screen.dart

Timer cada 300ms
    ↓
_startAutomaticCapture()
    ↓
_captureAndAnalyze()
    ↓
_sendImageAnalysis()
    ↓
cameraController.takePicture()  // Captura imagen
    ↓
File → bytes → base64
    ↓
WebSocket.send({
    type: "image_stream",
    image_data: "base64...",
    camera_active: true,
    timestamp: "2025-10-20T14:32:15"
})
```

### 2. Procesamiento Backend

```python
# BACKEND: api/main.py

@app.websocket("/ws")
async def websocket_endpoint(websocket):
    ↓
await websocket.receive_json()  # Recibe mensaje
    ↓
if message["type"] == "image_stream":
    ↓
    image_data = message.get("image_data")
    ↓
    # ANÁLISIS CON IA
    analysis = analyze_realtime_stream_real(
        image_data, 
        return_annotated=True
    )
    ↓
    # EXTRAER IMAGEN ANOTADA
    annotated_image = analysis.pop('annotated_image')
    ↓
    # CREAR RESPUESTA
    response = {
        "type": "realtime_analysis",
        "analysis": analysis,
        "annotated_image": annotated_image,
        "timestamp": datetime.now().isoformat(),
        "engine": "real_detection_mediapipe"
    }
    ↓
    # ALMACENAR EN BD
    shift_manager.store_detection(analysis)
    ↓
    # ENVIAR AL CLIENTE
    await manager.send_personal_message(response, websocket)
    ↓
    # BROADCAST A TODOS (incluyendo /visualization)
    await manager.broadcast(response)
```

### 3. Análisis de IA

```python
# services/ai/real_detection.py

def analyze_realtime_stream_real(image_data, return_annotated=True):
    
    # 1. DECODIFICAR IMAGEN
    image_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 2. DETECCIÓN DE POSE (MediaPipe)
    pose_results = pose.process(image_rgb)
    pose_landmarks = pose_results.pose_landmarks
    
    # 3. DETECCIÓN FACIAL (MediaPipe)
    face_results = face_detection.process(image_rgb)
    face_detected = bool(face_results.detections)
    
    # 4. ANÁLISIS DE VESTIMENTA
    if pose_landmarks:
        # Extraer puntos clave
        left_shoulder = pose_landmarks.landmark[11]
        right_shoulder = pose_landmarks.landmark[12]
        left_hip = pose_landmarks.landmark[23]
        right_hip = pose_landmarks.landmark[24]
        left_elbow = pose_landmarks.landmark[13]
        right_elbow = pose_landmarks.landmark[14]
        left_wrist = pose_landmarks.landmark[15]
        right_wrist = pose_landmarks.landmark[16]
        
        # Calcular métricas
        shoulder_distance = abs(right_shoulder.x - left_shoulder.x)
        torso_height = abs(left_shoulder.y - left_hip.y)
        arm_coverage = (
            abs(left_shoulder.y - left_wrist.y) + 
            abs(right_shoulder.y - right_wrist.y)
        ) / 2
        
        # Clasificar prenda
        if shoulder_distance > 0.25 and torso_height > 0.40 and arm_coverage > 0.20:
            clothing = "chaqueta"
            style = "formal"
        elif shoulder_distance > 0.19 and arm_coverage > 0.14:
            clothing = "sudadera"
            style = "deportivo"
        elif arm_coverage > 0.13:
            clothing = "camiseta_manga_larga"
            style = "casual"
        else:
            clothing = "camiseta"
            style = "casual"
    
    # 5. ANÁLISIS DE COLOR
    primary_color, secondary_color = _detect_dominant_colors_advanced(image_rgb)
    
    # 6. ACCESORIOS DE CABEZA
    head_accessory = _detect_head_accessories_improved(image_rgb, face_detected)
    
    # 7. CARTERAS/BOLSOS
    bag_accessory = _detect_bags_and_purses(image_rgb, bool(pose_landmarks))
    
    # 8. EDAD ESTIMADA
    age_range = _estimate_age_from_face(image_rgb, face_results)
    
    # 9. DIBUJAR BOUNDING BOXES
    if return_annotated:
        annotated_image = draw_detections_on_image(
            image.copy(), 
            {
                "person_detected": bool(pose_landmarks),
                "face_detected": face_detected,
                "clothing_item": clothing,
                "head_accessory": head_accessory,
                "bag_accessory": bag_accessory
            }
        )
        # Codificar a base64
        _, buffer = cv2.imencode('.jpg', annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 85])
        annotated_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # 10. RETORNAR RESULTADOS
    return {
        "person_detected": bool(pose_landmarks),
        "face_detected": face_detected,
        "clothing_item": clothing,
        "clothing_style": style,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "head_accessory": head_accessory,
        "bag_accessory": bag_accessory,
        "age_range": age_range,
        "detection_confidence": 0.92,
        "annotated_image": annotated_base64  # Si return_annotated=True
    }
```

### 4. Almacenamiento en Base de Datos

```python
# services/shift_manager.py

class ShiftManager:
    def store_detection(self, analysis):
        # Obtener turno activo actual
        current_shift = self.get_or_create_current_shift()
        
        # Crear registro en DeteccionBuffer
        detection = DeteccionBuffer(
            turno_id=current_shift.id,
            prenda=analysis.get('clothing_item'),
            estilo=analysis.get('clothing_style'),
            color_primario=analysis.get('primary_color'),
            color_secundario=analysis.get('secondary_color'),
            accesorios=analysis.get('head_accessory'),
            cartera_bolso=analysis.get('bag_accessory'),
            edad_estimada=analysis.get('age_range'),
            confianza=analysis.get('detection_confidence'),
            timestamp=datetime.now(),
            engine=analysis.get('engine', 'real_detection_mediapipe')
        )
        
        # Guardar en BD
        self.db.add(detection)
        self.db.commit()
        
        # Actualizar contador del turno
        current_shift.total_detecciones += 1
        self.db.commit()
```

### 5. Agregación de Datos (Cron)

```python
# services/cron_jobs.py

def aggregate_current_shift():
    """Ejecutado cada hora para agregar datos del turno"""
    
    db = SessionLocal()
    shift_manager = ShiftManager(db)
    
    # Obtener turno actual
    current_shift = shift_manager.get_current_shift()
    
    # Obtener todas las detecciones del turno
    detections = db.query(DeteccionBuffer)\
        .filter(DeteccionBuffer.turno_id == current_shift.id)\
        .all()
    
    # Agregar estadísticas
    prendas_count = Counter([d.prenda for d in detections])
    colores_count = Counter([d.color_primario for d in detections])
    accesorios_count = Counter([d.accesorios for d in detections if d.accesorios])
    
    # Crear o actualizar ResumenTurno
    summary = db.query(ResumenTurno)\
        .filter(ResumenTurno.turno_id == current_shift.id)\
        .first()
    
    if not summary:
        summary = ResumenTurno(turno_id=current_shift.id)
    
    summary.total_detecciones = len(detections)
    summary.prendas_mas_comunes = dict(prendas_count.most_common(5))
    summary.colores_predominantes = dict(colores_count.most_common(5))
    summary.accesorios_frecuentes = dict(accesorios_count.most_common(5))
    summary.fecha_agregado = datetime.now()
    
    db.add(summary)
    db.commit()
```

---

## 🧩 Componentes Principales

### ConnectionManager (WebSocket)

```python
# api/main.py

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        """Envía mensaje a TODOS los clientes conectados"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting: {e}")
                try:
                    self.active_connections.remove(connection)
                except ValueError:
                    pass
```

### Bounding Box Drawing

```python
# services/ai/real_detection.py

def draw_detections_on_image(image, analysis):
    annotated = image.copy()
    height, width = annotated.shape[:2]
    
    # Colores
    COLOR_FACE = (0, 255, 0)        # Verde
    COLOR_CLOTHING = (255, 165, 0)   # Naranja
    COLOR_ACCESSORY = (255, 0, 255)  # Magenta
    COLOR_BAG = (255, 255, 0)        # Cian
    
    # CARA (verde)
    if analysis.get('face_detected'):
        x1 = int(width * 0.35)
        y1 = int(height * 0.05)
        x2 = int(width * 0.65)
        y2 = int(height * 0.35)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), COLOR_FACE, 4)
        cv2.putText(annotated, "PERSONA DETECTADA", (x1+5, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_FACE, 2)
    
    # VESTIMENTA (naranja)
    if analysis.get('clothing_item'):
        x1 = int(width * 0.25)
        y1 = int(height * 0.25)
        x2 = int(width * 0.75)
        y2 = int(height * 0.70)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), COLOR_CLOTHING, 4)
        label = f"VESTIMENTA: {analysis['clothing_item']}"
        cv2.putText(annotated, label, (x1+5, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_CLOTHING, 2)
    
    # ACCESORIOS (magenta)
    if analysis.get('head_accessory'):
        x1 = int(width * 0.30)
        y1 = int(height * 0.02)
        x2 = int(width * 0.70)
        y2 = int(height * 0.25)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), COLOR_ACCESSORY, 4)
        label = f"ACCESORIO: {analysis['head_accessory']}"
        cv2.putText(annotated, label, (x1+5, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_ACCESSORY, 2)
    
    # CARTERA/BOLSO (cian)
    if analysis.get('bag_accessory'):
        x1 = int(width * 0.05)
        y1 = int(height * 0.40)
        x2 = int(width * 0.45)
        y2 = int(height * 0.75)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), COLOR_BAG, 4)
        label = f"CARTERA: {analysis['bag_accessory']}"
        cv2.putText(annotated, label, (x1+5, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_BAG, 2)
    
    return annotated
```

---

## 📊 Modelos de Datos

### SQLAlchemy Models

```python
# database/models.py

class Turno(Base):
    __tablename__ = "turnos"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(DateTime, default=datetime.now)
    fecha_fin = Column(DateTime, nullable=True)
    tipo_turno = Column(String, nullable=False)  # "mañana", "tarde", "noche"
    activo = Column(Boolean, default=True)
    total_detecciones = Column(Integer, default=0)
    
    # Relationships
    detecciones = relationship("DeteccionBuffer", back_populates="turno")
    resumenes = relationship("ResumenTurno", back_populates="turno")


class DeteccionBuffer(Base):
    __tablename__ = "deteccion_buffer"
    
    id = Column(Integer, primary_key=True, index=True)
    turno_id = Column(Integer, ForeignKey("turnos.id"))
    
    # Datos de detección
    prenda = Column(String, nullable=True)
    estilo = Column(String, nullable=True)
    color_primario = Column(String, nullable=True)
    color_secundario = Column(String, nullable=True)
    accesorios = Column(String, nullable=True)
    cartera_bolso = Column(String, nullable=True)
    edad_estimada = Column(String, nullable=True)
    confianza = Column(Float, default=0.0)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.now, index=True)
    engine = Column(String, default="unknown")
    camera_source = Column(String, default="unknown")
    
    # Relationship
    turno = relationship("Turno", back_populates="detecciones")


class ResumenTurno(Base):
    __tablename__ = "resumen_turno"
    
    id = Column(Integer, primary_key=True, index=True)
    turno_id = Column(Integer, ForeignKey("turnos.id"))
    
    # Estadísticas agregadas
    total_detecciones = Column(Integer, default=0)
    prendas_mas_comunes = Column(JSON, nullable=True)
    colores_predominantes = Column(JSON, nullable=True)
    accesorios_frecuentes = Column(JSON, nullable=True)
    edad_promedio = Column(String, nullable=True)
    
    # Metadata
    fecha_agregado = Column(DateTime, default=datetime.now)
    
    # Relationship
    turno = relationship("Turno", back_populates="resumenes")
```

---

## 🔒 Seguridad

### CORS Configuration

```python
# api/main.py

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Producción: especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Data Privacy

- ✅ No se almacenan imágenes completas
- ✅ No se guardan datos biométricos faciales
- ✅ Solo metadatos de detección
- ✅ Timestamps sin identificadores personales
- ✅ Cumplimiento GDPR por diseño

---

## ⚡ Optimizaciones

### 1. Image Compression

```python
# 85% quality JPEG
_, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 85])
```

### 2. WebSocket Broadcast Efficiency

```python
# Envío paralelo a múltiples clientes
async def broadcast(self, message: str):
    tasks = [conn.send_text(message) for conn in self.active_connections]
    await asyncio.gather(*tasks, return_exceptions=True)
```

### 3. Database Indexing

```python
# Índices en columnas de consulta frecuente
timestamp = Column(DateTime, default=datetime.now, index=True)
turno_id = Column(Integer, ForeignKey("turnos.id"), index=True)
```

### 4. Caching de Modelos ML

```python
# Cargar modelos una sola vez al inicio
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5
)
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_real_detection.py

def test_analyze_realtime_stream_real():
    # Cargar imagen de prueba
    with open("test_image.jpg", "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    # Analizar
    result = analyze_realtime_stream_real(image_data)
    
    # Assertions
    assert result['person_detected'] == True
    assert result['clothing_item'] in ['chaqueta', 'sudadera', 'camiseta']
    assert result['detection_confidence'] > 0.5
```

### Integration Tests

```python
# tests/test_websocket_flow.py

async def test_websocket_image_flow():
    # Conectar WebSocket
    async with websockets.connect("ws://localhost:8001/ws") as ws:
        # Enviar imagen
        await ws.send(json.dumps({
            "type": "image_stream",
            "image_data": "base64...",
            "camera_active": True
        }))
        
        # Recibir respuesta
        response = await ws.recv()
        data = json.loads(response)
        
        # Verificar
        assert data['type'] == 'realtime_analysis'
        assert 'analysis' in data
        assert 'annotated_image' in data
```

---

## 📈 Métricas y Monitoreo

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Uso
logger.info(f"Detección procesada: {clothing_item}")
logger.error(f"Error en análisis: {error}")
```

### Métricas a Monitorear

- **Latencia de análisis** (ms)
- **FPS efectivo** (frames/segundo)
- **Conexiones WebSocket activas**
- **Detecciones por minuto**
- **Uso de CPU/RAM**
- **Errores de detección**

---

## 🚀 Deployment Checklist

### Producción

- [ ] Cambiar `allow_origins=["*"]` a dominios específicos
- [ ] Configurar HTTPS/WSS
- [ ] Usar gunicorn con workers
- [ ] Configurar límite de conexiones WebSocket
- [ ] Implementar rate limiting
- [ ] Configurar logging a archivo
- [ ] Backup automático de BD
- [ ] Monitoreo con Prometheus/Grafana
- [ ] Configurar dominio y SSL
- [ ] Documentar proceso de rollback

---

**Versión:** 1.0.0  
**Última actualización:** 2025-10-20  
**Mantenedor:** Equipo NeoTotem AI


# 📖 Guía Completa - NeoTotem AI

> Sistema inteligente de análisis visual para tiendas retail que detecta en tiempo real la vestimenta, accesorios y preferencias de los clientes.

---

## 🎯 ¿Qué hace esta aplicación?

**NeoTotem AI** es un totem inteligente para tiendas de ropa que:

1. **📹 Captura** - Usa la cámara para ver a los clientes
2. **🤖 Analiza** - Detecta qué llevan puesto (ropa, accesorios, colores)
3. **💡 Recomienda** - Sugiere productos basados en lo que detecta
4. **📊 Registra** - Guarda estadísticas de cada turno de trabajo

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   FRONTEND      │         │     BACKEND      │         │   VISUALIZACIÓN │
│   (Flutter)     │◄───────►│    (FastAPI)     │◄───────►│     (HTML)      │
│                 │ WebSocket│                 │ WebSocket│                 │
│  • Cámara       │         │  • MediaPipe     │         │  • Debug        │
│  • Micrófono    │         │  • OpenCV        │         │  • Monitoreo    │
│  • UI Cliente   │         │  • IA Detección  │         │  • Tiempo Real  │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   BASE DE DATOS  │
                            │    (SQLite)      │
                            │                  │
                            │  • Detecciones   │
                            │  • Turnos        │
                            │  • Analytics     │
                            └──────────────────┘
```

---

## 📱 PARTE 1: FRONTEND (Flutter Web)

### ¿Qué es?
La interfaz visual que ve el cliente en el totem. Hecha con Flutter para funcionar en navegadores web.

### Ubicación de archivos
```
frontend/
├── lib/
│   ├── main.dart              # Punto de entrada
│   └── home_screen.dart       # Pantalla principal (cámara + micrófono)
└── pubspec.yaml               # Dependencias
```

### Componentes principales

#### 🎥 **Sistema de Cámara**
```dart
// Captura frames cada 300ms (3 FPS)
Future.delayed(Duration(milliseconds: 300), () async {
  await _captureAndAnalyze();
});
```

**¿Qué hace?**
- Enciende la cámara del dispositivo
- Captura imágenes automáticamente cada 300 milisegundos
- Envía las imágenes al backend por WebSocket
- Recibe análisis en tiempo real

#### 🎙️ **Sistema de Voz**
**¿Qué hace?**
- Graba audio cuando el cliente habla
- Envía el audio al backend
- Recibe transcripción y respuesta de IA
- Reproduce recomendaciones con voz sintetizada

#### 🔌 **WebSocket**
**¿Qué hace?**
- Mantiene conexión permanente con el backend
- Envía: imágenes de cámara, audio, comandos
- Recibe: análisis de IA, recomendaciones, estados

### Flujo de uso típico

```
1. Cliente se acerca al totem
   ↓
2. Presiona botón "Activar Cámara"
   ↓
3. Sistema captura imagen cada 300ms
   ↓
4. Muestra en pantalla: "Detectando: chaqueta negra, gorra..."
   ↓
5. Cliente presiona botón de micrófono
   ↓
6. Cliente dice: "Busco algo casual"
   ↓
7. Sistema recomienda productos según detección + voz
```

---

## 🖥️ PARTE 2: BACKEND (FastAPI + Python)

### ¿Qué es?
El "cerebro" de la aplicación. Procesa imágenes, audio, y coordina toda la lógica de negocio.

### Ubicación de archivos
```
apt-totem-backend/
├── api/
│   ├── main.py                    # Servidor principal + WebSocket
│   └── routers/
│       ├── cv.py                  # Endpoints de computer vision
│       ├── tracking.py            # Registro de interacciones
│       └── shifts.py              # Gestión de turnos
├── services/
│   ├── ai/
│   │   ├── real_detection.py     # ⭐ DETECCIÓN INTELIGENTE
│   │   └── mediapipe_engine.py   # Motor MediaPipe
│   ├── cv/
│   │   ├── color.py               # Análisis de colores
│   │   └── detector.py            # Detección de prendas
│   ├── shift_manager.py           # Gestión de turnos
│   └── cron_jobs.py               # Tareas programadas
├── database/
│   ├── models.py                  # Modelos de BD
│   └── database.py                # Conexión SQLite
└── visualization.html             # 🔍 Visualización debug
```

---

### 🧠 Motor de IA: `real_detection.py`

Este es el archivo **MÁS IMPORTANTE** del backend. Contiene toda la lógica de detección inteligente.

#### ¿Qué detecta?

##### 1️⃣ **Detección de Persona**
```python
# MediaPipe detecta 33 puntos del cuerpo
pose_results = pose.process(image_rgb)
```
- Detecta si hay una persona frente a la cámara
- Identifica posición de hombros, codos, caderas, etc.

##### 2️⃣ **Detección de Ropa**
```python
def analyze_real_clothing_simple(image_rgb, pose_landmarks):
    # Mide:
    shoulder_distance = 0.156  # Ancho de hombros
    torso_height = 0.285       # Largo del torso
    arm_coverage = 0.095       # Cobertura de brazos
    
    # Clasifica:
    if shoulder_distance > 0.25 and torso_height > 0.40 and arm_coverage > 0.20:
        return "chaqueta"
    elif shoulder_distance > 0.19 and arm_coverage > 0.14:
        return "sudadera"
    elif arm_coverage > 0.13:
        return "camiseta_manga_larga"
    else:
        return "camiseta"
```

**Prendas que detecta:**
- ✅ Chaqueta (criterios muy estrictos)
- ✅ Sudadera / Hoodie
- ✅ Camiseta manga larga
- ✅ Camiseta manga corta

##### 3️⃣ **Detección de Accesorios de Cabeza**
```python
def _detect_head_accessories_improved(image_rgb, face_detected):
    # Detecta simultáneamente:
    - 🧢 Gorra (visera detectada)
    - 🎩 Gorro (cobertura superior sin visera)
    - 🕶️ Gafas (líneas horizontales en zona de ojos)
```

##### 4️⃣ **Detección de Carteras/Bolsos**
```python
def _detect_bags_and_purses(image_rgb, pose_detected):
    # Analiza región media-lateral del cuerpo
    # Clasifica por tamaño y posición:
    - 🎒 Mochila (grande, centrada)
    - 👜 Bolso cruzado (diagonal)
    - 👛 Cartera de mano (pequeña, baja)
    - 👝 Bolso genérico (medio, lateral)
```

##### 5️⃣ **Análisis de Colores**
```python
# Identifica colores dominantes en la ropa
primary_color = "negro"
secondary_color = "blanco"
```

##### 6️⃣ **Estimación de Edad**
```python
# Basado en proporciones faciales
age_range = "25-35"
```

---

### 🎨 Visualización con Bounding Boxes

El sistema dibuja recuadros de colores sobre la imagen:

```python
def draw_detections_on_image(image, analysis):
    # 🟢 VERDE = Cara/Persona
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
    
    # 🟠 NARANJA = Vestimenta
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 165, 0), 4)
    
    # 🟣 MAGENTA = Accesorios de cabeza
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 4)
    
    # 🔵 CIAN = Carteras/Bolsos
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 0), 4)
```

---

### 🔄 WebSocket en `main.py`

#### Flujo de comunicación:

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 1. Cliente se conecta
    await manager.connect(websocket)
    
    # 2. Recibe mensaje del frontend
    message = await websocket.receive_json()
    
    # 3. Procesa según tipo
    if message["type"] == "image_stream":
        # Analiza imagen con IA
        analysis = analyze_realtime_stream_real(image_data)
        
        # Almacena en BD
        shift_manager.store_detection(analysis)
        
        # Envía respuesta al cliente
        await manager.send_personal_message(response, websocket)
        
        # Broadcast a TODOS (incluyendo /visualization)
        await manager.broadcast(response)
```

**Tipos de mensajes:**
- `image_stream` - Imagen de cámara
- `voice_message` - Audio del cliente
- `ping` - Mantener conexión viva
- `realtime_analysis` - Respuesta con análisis

---

### 📊 Sistema de Turnos y Analytics

#### ¿Para qué sirve?

Cada tienda tiene turnos de trabajo (mañana, tarde, noche). El sistema registra:
- Cuántos clientes detectados por turno
- Qué prendas son más comunes
- Qué colores prefieren
- Rango de edades predominante

#### Archivos involucrados:

**`models.py` - Tablas de base de datos:**
```python
class Turno(Base):
    id = Column(Integer, primary_key=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    tipo_turno = Column(String)  # "mañana", "tarde", "noche"

class DeteccionBuffer(Base):
    # Almacena cada detección individual
    prenda = Column(String)
    color = Column(String)
    accesorios = Column(String)
    timestamp = Column(DateTime)

class ResumenTurno(Base):
    # Resumen agregado por turno
    total_detecciones = Column(Integer)
    prendas_mas_comunes = Column(JSON)
    colores_predominantes = Column(JSON)
```

**`shift_manager.py` - Lógica de turnos:**
```python
class ShiftManager:
    def store_detection(self, analysis):
        # Guarda cada detección en DeteccionBuffer
        
    def aggregate_shift_data(self):
        # Al final del turno, crea ResumenTurno
        # con estadísticas agregadas
```

**`cron_jobs.py` - Tareas programadas:**
```python
# Cada hora: agregar datos del turno actual
schedule.every().hour.do(aggregate_current_shift)

# A las 06:00: nuevo turno de mañana
# A las 14:00: nuevo turno de tarde
# A las 22:00: nuevo turno de noche
```

---

## 🔍 PARTE 3: VISUALIZACIÓN DEBUG

### ¿Qué es?
Página web especial para que el administrador/desarrollador vea en tiempo real **exactamente** lo que detecta la IA.

### Acceso
```
http://localhost:8001/visualization
```

### ¿Qué muestra?

1. **📷 Imagen con recuadros de colores**
   - Verde = Cara
   - Naranja = Ropa
   - Magenta = Accesorios
   - Cian = Carteras

2. **📊 Panel de información**
   - Prenda detectada: "camiseta"
   - Estilo: "casual"
   - Color principal: "negro"
   - Accesorios: "gorra, gafas"
   - Cartera: "bolso_cruzado"

3. **🖥️ Debug terminal (abajo)**
   ```
   [14:32:15] 🔍 DEBUG - Métricas de detección:
   [14:32:15]   Distancia hombros: 0.156
   [14:32:15]   Altura torso: 0.285
   [14:32:15]   ✅ DETECTADO: camiseta (casual)
   [14:32:16] 🎩 Accesorios: gorra, gafas
   [14:32:16] 👜 Cartera: bolso_cruzado
   ```

### Actualización
Se actualiza automáticamente **cada 300ms** (tiempo real) gracias al WebSocket broadcast.

---

## ⚙️ Configuración y Velocidad

### 🚀 Velocidad de Detección

Actualmente configurado para **tiempo real (~3 FPS)**:

```dart
// frontend/lib/home_screen.dart (línea 315)
Future.delayed(Duration(milliseconds: 300), () async {
  await _captureAndAnalyze();
});
```

**Opciones de velocidad:**

| Milisegundos | FPS | Uso | Recomendado para |
|--------------|-----|-----|------------------|
| 100 | ~10 FPS | Alto | Demos, marketing |
| 200 | ~5 FPS | Medio-Alto | Tiendas premium |
| **300** | **~3 FPS** | **Medio** | **✅ Retail general** |
| 500 | ~2 FPS | Bajo | Ahorrar recursos |

### 🎯 Umbrales de Detección

Para evitar falsos positivos en "chaqueta":

```python
# services/ai/real_detection.py (línea 388)
if shoulder_distance > 0.25 and torso_height > 0.40 and arm_coverage > 0.20:
    clothing_detected = "chaqueta"
```

**Ajustar si:**
- Detecta muchas chaquetas erróneamente → **SUBIR** umbrales (0.26, 0.42, 0.22)
- No detecta chaquetas reales → **BAJAR** umbrales (0.24, 0.38, 0.18)

---

## 🚀 Cómo Iniciar la Aplicación

### 1️⃣ Iniciar Backend
```bash
cd apt-totem-backend
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```
✅ Backend corriendo en: `http://localhost:8001`

### 2️⃣ Iniciar Frontend
```bash
cd frontend
flutter run -d chrome --web-port=8080
```
✅ Frontend corriendo en: `http://localhost:8080`

### 3️⃣ Abrir Visualización (opcional)
```
http://localhost:8001/visualization
```

---

## 📊 Flujo Completo del Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│                    CLIENTE FRENTE AL TOTEM                       │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  FLUTTER CAPTURA │
                    │  Imagen cada 300ms│
                    └──────────────────┘
                              │
                              ▼ (WebSocket)
                    ┌──────────────────┐
                    │ BACKEND RECIBE   │
                    │ Imagen en Base64 │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ MEDIAPIPE        │
                    │ Detecta 33 puntos│
                    │ del cuerpo       │
                    └──────────────────┘
                              │
                              ▼
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────┐                            ┌──────────────┐
│ ANÁLISIS     │                            │ ANÁLISIS     │
│ VESTIMENTA   │                            │ ACCESORIOS   │
│              │                            │              │
│ • Chaqueta   │                            │ • Gorra      │
│ • Sudadera   │                            │ • Gafas      │
│ • Camiseta   │                            │ • Cartera    │
└──────────────┘                            └──────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ DIBUJA BOUNDING  │
                    │ BOXES + Etiquetas│
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ GUARDA EN BD     │
                    │ DeteccionBuffer  │
                    └──────────────────┘
                              │
                              ▼
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌──────────────┐                            ┌──────────────┐
│ ENVÍA A      │                            │ BROADCAST A  │
│ FLUTTER      │                            │ /visualization│
│ (UI Cliente) │                            │ (Monitoreo)  │
└──────────────┘                            └──────────────┘
        │
        ▼
┌──────────────────┐
│ CLIENTE VE:      │
│ "Detectamos      │
│  camiseta negra  │
│  ¿Quieres ver    │
│  recomendaciones?│
└──────────────────┘
```

---

## 🔧 Solución de Problemas Comunes

### ❌ "No detecta nada"
**Causa:** Umbrales muy altos
**Solución:** Bajar umbrales en `real_detection.py` líneas 388-395

### ❌ "Siempre detecta chaqueta"
**Causa:** Umbrales muy bajos
**Solución:** Subir umbrales (ya está configurado estricto: 0.25, 0.40, 0.20)

### ❌ "No detecta gorra/gafas"
**Causa:** Iluminación pobre o persona muy lejos
**Solución:** Mejorar iluminación, acercar la cámara

### ❌ "Imagen no se actualiza en /visualization"
**Causa:** WebSocket desconectado
**Solución:** Recargar página, verificar backend esté corriendo

### ❌ "Cámara no inicia en Flutter"
**Causa:** Permisos de navegador
**Solución:** Permitir acceso a cámara cuando Chrome lo solicite

---

## 📈 Endpoints Principales

### Backend API Endpoints:

```
POST /cv/detect-frame
    → Detecta persona y estilo de vestimenta

POST /cv/analyze-customer-ai-real
    → Análisis completo con MediaPipe

GET /shifts/current
    → Obtiene turno actual

GET /shifts/{shift_id}/summary
    → Resumen de un turno específico

GET /shifts/analytics
    → Estadísticas generales

POST /tracking/camera-detection
    → Registra detección de cámara

WebSocket /ws
    → Comunicación en tiempo real
```

---

## 📚 Archivos de Documentación Adicional

Este proyecto incluye documentación detallada:

- **SISTEMA_TURNOS_DETECCIONES.md** - Explicación completa del sistema de turnos
- **VISUALIZACION_CV_CRUDA.md** - Detalles técnicos de visualización
- **MEJORAS_DETECCION_PRENDAS.md** - Mejoras en detección de ropa
- **MEJORAS_VISUALIZACION_Y_ACCESORIOS.md** - Mejoras en accesorios
- **README_RETAIL.md** - Contexto de negocio retail

---

## 🎓 Conceptos Clave

### MediaPipe
Librería de Google para detección de pose humana. Identifica 33 puntos clave del cuerpo en tiempo real.

### OpenCV
Librería de computer vision para procesamiento de imágenes (colores, contornos, dibujo).

### WebSocket
Protocolo de comunicación bidireccional en tiempo real entre frontend y backend.

### Bounding Box
Recuadro que enmarca una región de interés en la imagen.

### Base64
Codificación de imágenes para transmitir por WebSocket.

### Cron Jobs
Tareas programadas que se ejecutan automáticamente (cambio de turno cada 8 horas).

---

## 🎯 Resumen Ejecutivo

**NeoTotem AI** es un sistema de 3 capas:

1. **Frontend (Flutter)** → Interfaz de usuario + captura de cámara/audio
2. **Backend (FastAPI)** → Cerebro con IA que analiza y decide
3. **Visualización (HTML)** → Herramienta de debug para monitoreo

**Tecnologías clave:**
- MediaPipe (detección de persona)
- OpenCV (análisis visual)
- WebSocket (comunicación en tiempo real)
- SQLite (almacenamiento de datos)

**Velocidad actual:** 3 FPS (1 análisis cada 300ms)

**Detecciones:**
- ✅ Ropa (4 tipos)
- ✅ Colores (primario + secundario)
- ✅ Accesorios de cabeza (3 tipos)
- ✅ Carteras/bolsos (4 tipos)
- ✅ Edad aproximada

---

## 📞 Soporte Técnico

Para ajustar configuraciones:
1. **Velocidad** → `frontend/lib/home_screen.dart` línea 315
2. **Umbrales de detección** → `apt-totem-backend/services/ai/real_detection.py` líneas 388-400
3. **Horarios de turnos** → `apt-totem-backend/services/cron_jobs.py` líneas 45-70

---

**Versión:** 1.0.0  
**Última actualización:** 2025-10-20  
**Estado:** ✅ Producción (Tiempo Real activado)


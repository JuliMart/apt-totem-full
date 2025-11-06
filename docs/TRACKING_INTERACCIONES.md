# 🆔 Sistema de Tracking de Interacciones - NeoTotem

## 📋 Resumen

**TODAS las interacciones con el NeoTotem se almacenan en la base de datos** para análisis y mejora continua.

---

## 🔑 Session ID

Cada vez que un usuario inicia la aplicación, se genera un **Session ID único**:

```dart
sessionId = 'session_${DateTime.now().millisecondsSinceEpoch}_${random}'
```

**Ejemplo:** `session_1729620345678_4523`

Este ID se usa para **trackear todas las interacciones** del usuario durante esa sesión.

---

## ✅ Interacciones que SE Registran en Base de Datos

### 1. 📸 **Detecciones en Tiempo Real (CV/IA)**

**Dónde:** `apt-totem-backend/api/main.py` (líneas 258-268)

**Qué se guarda:**
```python
{
  'age_range': '36-45',
  'clothing_item': 'chaqueta',
  'primary_color': 'blanco',
  'clothing_style': 'formal',
  'detection_confidence': 0.78,
  'head_accessory': 'gafas',
  'bag_accessory': 'mochila',
  'engine': 'real_detection_mediapipe',
  'camera_source': 'webcam',
  'session_id': 'session_...',
  'timestamp': '2025-10-22T17:40:13'
}
```

**Tabla:** `detecciones` o `detecciones_turno`

**Cuándo:** Cada vez que se analiza un frame de video (cada 500ms aprox.)

---

### 2. 🎙️ **Interacciones de Voz**

**Dónde:** 
- Frontend: `home_screen.dart` (líneas 195-200)
- Backend: `apt-totem-backend/api/routers/tracking.py` (endpoint `/tracking/voice`)

**Qué se guarda:**
```python
{
  'session_id': 'session_...',
  'transcription': 'zapatillas azules',
  'intent': 'buscar',
  'confidence': 0.85,
  'processing_time_ms': 1200,
  'timestamp': '2025-10-22T17:41:30'
}
```

**Tabla:** `interacciones_voz`

**Cuándo:** Cada vez que el usuario habla al NeoTotem y se procesa el audio.

---

### 3. 🔍 **Búsquedas**

**Dónde:** `apt-totem-backend/api/routers/busqueda.py`

**Qué se guarda:**
```python
{
  'session_id': 'session_...',
  'query': 'zapatillas nike',
  'results_count': 15,
  'filters_applied': {'brand': 'Nike', 'category': 'Zapatillas'},
  'timestamp': '2025-10-22T17:42:00'
}
```

**Tabla:** `busquedas` o `tracking_interacciones`

**Cuándo:** Cada vez que el usuario realiza una búsqueda (texto o voz).

---

### 4. 👁️ **Recomendaciones Vistas**

**Dónde:** `ApiService.trackRecommendationViewed()` (api_service.dart)

**Qué se guarda:**
```python
{
  'session_id': 'session_...',
  'variant_id': 123,
  'recommendation_type': 'voice',  # 'voice', 'image', 'smart'
  'position': 2,  # Posición en la lista
  'metadata': {
    'age_detected': '36-45',
    'color_detected': 'blanco',
    'voice_intent': 'buscar'
  },
  'timestamp': '2025-10-22T17:43:15'
}
```

**Tabla:** `recomendaciones_vistas` o `tracking_recomendaciones`

**Cuándo:** Cada vez que se carga la pestaña de recomendaciones con productos.

---

### 5. 🖱️ **Clics en Productos**

**Dónde:** `ApiService.trackProductClick()` (api_service.dart)

**Qué se guarda:**
```python
{
  'session_id': 'session_...',
  'variant_id': 456,
  'recommendation_id': 789,
  'click_position': 3,
  'timestamp': '2025-10-22T17:44:00'
}
```

**Tabla:** `tracking_clics` o `interacciones_productos`

**Cuándo:** Cada vez que el usuario hace clic en un producto.

---

### 6. 📊 **Interacciones Genéricas**

**Dónde:** `ApiService.trackInteraction()` (api_service.dart)

**Tipos:**
- `view`: Vista de pestaña
- `click`: Clic en botón
- `hover`: Hover sobre elemento
- `scroll`: Scroll en lista
- `search`: Búsqueda
- `voice`: Interacción de voz
- `camera`: Activación de cámara

**Qué se guarda:**
```python
{
  'session_id': 'session_...',
  'interaction_type': 'camera',
  'variant_id': None,
  'metadata': {'camera_enabled': True},
  'duration_seconds': 45.3,
  'timestamp': '2025-10-22T17:45:00'
}
```

**Tabla:** `tracking_interacciones`

**Cuándo:** En eventos específicos de la aplicación.

---

## 📊 Tablas de Base de Datos

### Tabla: `detecciones`
```sql
CREATE TABLE detecciones (
  id_deteccion INT PRIMARY KEY AUTO_INCREMENT,
  id_sesion VARCHAR(255),
  prenda VARCHAR(100),
  color VARCHAR(50),
  rango_etario VARCHAR(20),
  confianza DECIMAL(3,2),
  fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `interacciones_voz`
```sql
CREATE TABLE interacciones_voz (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id VARCHAR(255),
  transcription TEXT,
  intent VARCHAR(100),
  confidence DECIMAL(3,2),
  processing_time_ms INT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `tracking_interacciones`
```sql
CREATE TABLE tracking_interacciones (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id VARCHAR(255),
  interaction_type VARCHAR(50),
  variant_id INT,
  metadata JSON,
  duration_seconds DECIMAL(10,2),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `tracking_recomendaciones`
```sql
CREATE TABLE tracking_recomendaciones (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id VARCHAR(255),
  variant_id INT,
  recommendation_type VARCHAR(50),
  position INT,
  metadata JSON,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `tracking_clics`
```sql
CREATE TABLE tracking_clics (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id VARCHAR(255),
  variant_id INT,
  recommendation_id INT,
  click_position INT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔄 Flujo Completo de Tracking

```
Usuario inicia app
  ↓
🆔 Se genera Session ID único
  ↓
┌─────────────────────────────────────────────┐
│  TODAS las interacciones usan este ID      │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│  PESTAÑA DETECCIÓN                          │
├─────────────────────────────────────────────┤
│  • Cámara activa                            │
│    → trackInteraction('camera')             │
│  • Frame analizado (cada 500ms)             │
│    → store_detection() en DB               │
│  • Botón "Ver Recomendaciones"              │
│    → trackInteraction('view')               │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│  PESTAÑA BÚSQUEDA                           │
├─────────────────────────────────────────────┤
│  • Usuario habla                            │
│    → trackVoiceInteraction()                │
│  • Búsqueda de texto                        │
│    → trackInteraction('search')             │
│  • Clic en producto                         │
│    → trackProductClick()                    │
└─────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────┐
│  PESTAÑA RECOMENDACIONES                    │
├─────────────────────────────────────────────┤
│  • Productos cargados                       │
│    → trackRecommendationViewed() (cada uno) │
│  • Clic en producto                         │
│    → trackProductClick()                    │
│  • Cambio de modo (IA/Voz/Smart)            │
│    → trackInteraction('view')               │
└─────────────────────────────────────────────┘
```

---

## 📈 Métricas que se Pueden Obtener

### 1. **Por Sesión:**
- Duración total de la sesión
- Número de detecciones de IA
- Número de búsquedas por voz
- Productos vistos
- Productos clickeados
- Recomendaciones más efectivas

### 2. **Por Turno de Trabajo:**
- Clientes atendidos (sesiones únicas)
- Detecciones totales
- Interacciones de voz totales
- Productos más vistos
- Conversión (visitas → clics)

### 3. **Análisis de Comportamiento:**
- Tiempo promedio en cada pestaña
- Ruta más común (detección → búsqueda → recomendaciones)
- Eficacia de cada tipo de recomendación (IA vs Voz vs Smart)
- Productos más populares por rango de edad

---

## 🛠️ Verificar Tracking en Tiempo Real

### Consola del Frontend (Chrome DevTools):
```
🆔 Session ID generado: session_1729620345678_4523
✅ Interacción de voz trackeada
✅ Recomendación vista trackeada
✅ Clic en producto trackeado
```

### Logs del Backend:
```bash
[2025-10-22 17:40:13] Detección almacenada: session_..., prenda=chaqueta
[2025-10-22 17:41:30] Interacción de voz: session_..., intent=buscar
[2025-10-22 17:43:15] Recomendación vista: session_..., variant_id=123
```

### Consulta SQL directa:
```sql
-- Ver todas las interacciones de una sesión
SELECT * FROM tracking_interacciones 
WHERE session_id = 'session_1729620345678_4523'
ORDER BY timestamp DESC;

-- Ver detecciones de IA de la última hora
SELECT * FROM detecciones 
WHERE fecha_hora > NOW() - INTERVAL 1 HOUR;

-- Ver búsquedas por voz
SELECT * FROM interacciones_voz 
ORDER BY timestamp DESC 
LIMIT 20;
```

---

## ✅ Checklist de Implementación

- [x] Session ID generado al iniciar app
- [x] Detecciones en tiempo real → DB
- [x] Interacciones de voz → DB
- [x] Método `trackVoiceInteraction()` en ApiService
- [x] Método `trackRecommendationViewed()` en ApiService
- [x] Método `trackProductClick()` en ApiService
- [x] Método `trackInteraction()` en ApiService
- [ ] Integrar tracking en `RecommendationsWidget` (cuando se cargan productos)
- [ ] Integrar tracking en clics de productos
- [ ] Crear dashboard de analytics

---

## 🚀 Próximos Pasos

1. **Integrar tracking en RecommendationsWidget:** Llamar `trackRecommendationViewed()` cuando se cargan productos
2. **Integrar tracking en clics:** Llamar `trackProductClick()` al hacer clic en un producto
3. **Crear endpoints de analytics:** Para consultar estadísticas agregadas
4. **Dashboard de visualización:** Panel para ver métricas en tiempo real

---

## 📝 Notas Importantes

- **Session ID único por usuario:** Se genera al abrir la app
- **Todas las interacciones llevan Session ID:** Para poder agruparlas
- **Tracking asíncrono:** No bloquea la UI
- **Errores silenciosos:** Si falla el tracking, la app sigue funcionando
- **Privacy:** Session ID es temporal y no identifica al usuario personalmente

---

**Con este sistema, TODAS las interacciones con el NeoTotem quedan registradas en la base de datos para análisis posterior.** 🎯📊✨


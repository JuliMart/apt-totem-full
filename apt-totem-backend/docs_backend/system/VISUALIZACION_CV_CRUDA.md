# 📹 Visualización de Computer Vision en Crudo

## 🎯 Descripción

Sistema de visualización en tiempo real que muestra **exactamente** lo que ve la IA de computer vision, con las detecciones dibujadas directamente sobre la imagen de la cámara.

## ✨ Características

### Detecciones Visuales en Tiempo Real
- 🟢 **Recuadro verde**: Persona/Cara detectada con edad y confianza
- 🟠 **Recuadro naranja**: Vestimenta superior con prenda, estilo y color
- 🟣 **Recuadro magenta**: Accesorios de cabeza (gorros, gafas, etc.)
- ⏰ **Timestamp**: Marca de tiempo en cada frame
- 🏷️ **Marca de agua**: "NeoTotem AI"

### Información Mostrada
Cada detección incluye etiquetas con:
- Tipo de detección
- Nivel de confianza (%)
- Características específicas (edad, color, estilo, etc.)

## 🚀 Cómo Usar

### 1. Iniciar el Backend
```bash
cd apt-totem-backend
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Abrir la Visualización
Abrir en el navegador:
```
http://localhost:8001/visualization
```

### 3. Activar la Cámara en la UI Principal
En la aplicación Flutter principal:
1. Ir a la tab "Detección"
2. Click en "📹 Activar Cámara"
3. La visualización se actualizará automáticamente

### 4. Ver las Detecciones
La página `/visualization` mostrará:
- **Izquierda**: Imagen en tiempo real con recuadros y etiquetas
- **Derecha**: Panel de información con detalles de cada detección

## 📊 Ejemplo Visual

```
┌──────────────────────────────────────────┐
│  PERSONA DETECTADA                       │
│  Edad: 26-35                             │
│  Conf: 87%                               │
│  ┌────────────────────────────┐         │
│  │                             │         │
│  │      [CARA DETECTADA]       │         │
│  │                             │         │
│  └────────────────────────────┘         │
│                                          │
│  VESTIMENTA                              │
│  Prenda: camiseta                        │
│  Estilo: casual                          │
│  Color: azul                             │
│  ┌────────────────────────────┐         │
│  │                             │         │
│  │       [ROPA DETECTADA]      │         │
│  │                             │         │
│  └────────────────────────────┘         │
│                                          │
│  NeoTotem AI      2024-10-18 15:30:45   │
└──────────────────────────────────────────┘
```

## 🔧 Arquitectura Técnica

### Flujo de Datos

```
Cámara Flutter
    ↓
Captura de imagen (base64)
    ↓
WebSocket → Backend
    ↓
MediaPipe + OpenCV
    ├─ Detección facial
    ├─ Análisis de colores
    ├─ Detección de prendas
    └─ Detección de accesorios
    ↓
draw_detections_on_image()
    ├─ Dibuja recuadros
    ├─ Añade etiquetas
    └─ Codifica a base64
    ↓
WebSocket → Clientes
    ├─ UI Principal (Flutter)
    └─ Visualización Web
    ↓
Renderizado en tiempo real
```

### Componentes

#### 1. Backend - `real_detection.py`

**Función Principal**: `analyze_realtime_stream_real(image_data, return_annotated=True)`
- Analiza la imagen con MediaPipe
- Dibuja las detecciones sobre la imagen
- Devuelve análisis + imagen anotada

**Función de Anotación**: `draw_detections_on_image(image, analysis)`
- Recibe imagen original y análisis
- Dibuja recuadros de colores según tipo
- Añade etiquetas con información
- Devuelve imagen anotada

#### 2. Backend - `main.py`

**WebSocket Handler**:
```python
# Solicita imagen anotada
analysis = analyze_realtime_stream_real(image_data, return_annotated=True)

# Extrae imagen anotada
annotated_image = analysis.pop('annotated_image', None)

# Envía a todos los clientes
response = {
    "type": "realtime_analysis",
    "analysis": analysis,
    "annotated_image": annotated_image,  # ← Imagen con detecciones
    ...
}
await manager.broadcast(json.dumps(response))
```

#### 3. Frontend - `visualization.html`

**Manejo del WebSocket**:
```javascript
case 'realtime_analysis':
    this.displayAnalysis(data.analysis, data.annotated_image);
    break;
```

**Renderizado de Imagen**:
```javascript
displayImage(annotatedImageBase64) {
    if (annotatedImageBase64) {
        imageContainer.innerHTML = `
            <img src="data:image/jpeg;base64,${annotatedImageBase64}">
        `;
    }
}
```

## 🎨 Colores de Detección

| Elemento | Color | RGB | Uso |
|----------|-------|-----|-----|
| Persona/Cara | 🟢 Verde | (0, 255, 0) | Recuadro de detección facial |
| Vestimenta | 🟠 Naranja | (255, 165, 0) | Recuadro de prendas |
| Accesorios | 🟣 Magenta | (255, 0, 255) | Recuadro de accesorios |
| Fondo texto | ⚫ Negro | (0, 0, 0) | Fondo de etiquetas |
| Texto | ⚪ Blanco | (255, 255, 255) | Texto de etiquetas |

## 📈 Rendimiento

### Optimizaciones Implementadas
- **Calidad JPEG**: 85% (balance calidad/tamaño)
- **Codificación**: Base64 (compatible con WebSocket)
- **Broadcast eficiente**: Envío simultáneo a todos los clientes
- **Caching**: No se re-procesa si no hay cambios

### Métricas Típicas
- **Latencia**: ~100-300ms por frame
- **Tamaño imagen**: ~50-150KB por frame (comprimido)
- **FPS**: 3-5 fps (suficiente para detección retail)

## 🔍 Casos de Uso

### 1. Debugging de Detecciones
Verificar visualmente qué está detectando la IA:
- ¿Los recuadros están en el lugar correcto?
- ¿Las etiquetas muestran información precisa?
- ¿La confianza es apropiada?

### 2. Demostración en Vivo
Mostrar a clientes/stakeholders:
- Capacidades reales del sistema
- Precisión de las detecciones
- Velocidad de respuesta

### 3. Análisis de Mejoras
Identificar áreas de mejora:
- Falsos positivos/negativos
- Problemas de iluminación
- Ángulos problemáticos

### 4. Capacitación de Personal
Entrenar al personal de tienda:
- Cómo funciona el sistema
- Qué información captura
- Cómo interpretar los resultados

## 🛠️ Personalización

### Modificar Colores
Editar en `real_detection.py`:
```python
COLOR_FACE = (0, 255, 0)      # Verde
COLOR_CLOTHING = (255, 165, 0)  # Naranja
COLOR_ACCESSORY = (255, 0, 255) # Magenta
```

### Modificar Posiciones de Recuadros
Editar en `draw_detections_on_image()`:
```python
# Recuadro de cara
face_x1 = int(width * 0.25)  # 25% del ancho
face_y1 = int(height * 0.1)  # 10% de la altura
face_x2 = int(width * 0.75)  # 75% del ancho
face_y2 = int(height * 0.4)  # 40% de la altura
```

### Modificar Calidad de Imagen
Editar en `analyze_realtime_stream_real()`:
```python
cv2.imencode('.jpg', annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 85])
#                                                                 ↑
#                                                        Cambiar 85 a otro valor (1-100)
```

## 🐛 Troubleshooting

### Imagen no se muestra
**Problema**: La visualización no muestra la imagen

**Soluciones**:
1. Verificar que la cámara esté activa en Flutter
2. Verificar WebSocket conectado
3. Verificar logs del backend
4. Abrir consola del navegador (F12)

### Imagen muy pesada
**Problema**: La transmisión es lenta

**Soluciones**:
1. Reducir calidad JPEG (de 85 a 70)
2. Reducir frecuencia de captura (de 3s a 5s)
3. Reducir resolución de cámara

### Recuadros mal posicionados
**Problema**: Los recuadros no coinciden con las detecciones

**Soluciones**:
1. Ajustar posiciones relativas en `draw_detections_on_image()`
2. Calibrar detección de MediaPipe
3. Mejorar iluminación de la tienda

## 📱 Comparación con UI Principal

| Característica | UI Principal (Flutter) | Visualización Web |
|----------------|------------------------|-------------------|
| **Propósito** | Interacción del cliente | Monitoreo y debug |
| **Muestra imagen** | ❌ No | ✅ Sí (anotada) |
| **Recuadros visuales** | ❌ No | ✅ Sí |
| **Análisis textual** | ✅ Sí | ✅ Sí |
| **Recomendaciones** | ✅ Sí | ❌ No |
| **Búsqueda** | ✅ Sí | ❌ No |

## 🚀 Mejoras Futuras

- [ ] Grabación de video de las detecciones
- [ ] Exportar frames anotados como imágenes
- [ ] Comparación lado a lado (original vs anotada)
- [ ] Heatmap de detecciones
- [ ] Estadísticas en tiempo real
- [ ] Múltiples cámaras simultáneas
- [ ] Zoom en áreas de interés
- [ ] Modo pantalla completa

## 📞 Soporte

Para acceder a la visualización:
```
http://localhost:8001/visualization
```

Para documentación completa del API:
```
http://localhost:8001/docs
```

## 💡 Tips

1. **Mejor iluminación = mejores detecciones**
2. **Posicionar cliente de frente a la cámara**
3. **Distancia óptima: 1-2 metros**
4. **Evitar fondos con mucho movimiento**
5. **Revisar visualización periódicamente para calibrar**


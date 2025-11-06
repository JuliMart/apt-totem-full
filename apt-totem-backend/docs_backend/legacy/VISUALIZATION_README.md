# 🎯 NeoTotem AI - Visualización en Tiempo Real

## 📋 Descripción
Sistema de visualización que muestra exactamente lo que detecta la IA, con recuadros marcando:
- 👕 **Vestimenta Superior** (verde)
- 🎨 **Análisis de Color** (naranja) 
- 👓 **Accesorios** (magenta)
- 👤 **Análisis Facial** (rojo)

## 🚀 Cómo usar

### 1. Iniciar el backend
```bash
cd apt-totem-backend
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Abrir la visualización
Abrir en el navegador:
```
http://localhost:8001/visualization
```

### 3. Activar la cámara en el frontend
- Ir a la app Flutter
- Activar la cámara
- La visualización se actualizará automáticamente

## 🔧 Endpoints disponibles

### Página de visualización
```
GET /visualization
```
Página web con interfaz de visualización en tiempo real.

### Análisis de imagen con marcado
```
POST /visualization/analyze-image
```
Parámetros:
- `image_data`: Imagen en base64
- `analysis_data`: Datos de análisis en JSON

### Información de detecciones
```
GET /visualization/detection-info
```
Devuelve información sobre los tipos de detección.

## 🧪 Probar el sistema

### Ejecutar test de visualización
```bash
python3 test_visualization.py
```

Esto:
1. ✅ Verifica que el backend esté corriendo
2. 📸 Crea una imagen de prueba
3. 🔍 Envía análisis simulado
4. 💾 Guarda imagen anotada como `test_annotated.jpg`

## 🎨 Tipos de detección

| Tipo | Color | Descripción |
|------|-------|-------------|
| **Vestimenta** | 🟢 Verde | Camisetas, chaquetas, etc. |
| **Color** | 🟠 Naranja | Colores principales y secundarios |
| **Accesorios** | 🟣 Magenta | Gorros, gafas, etc. |
| **Cara** | 🔴 Rojo | Detección facial y edad |

## 📱 Flujo completo

1. **Usuario activa cámara** en Flutter
2. **Imagen se captura** automáticamente cada 3 segundos
3. **Backend analiza** con MediaPipe y OpenCV
4. **Visualización se actualiza** en tiempo real
5. **Recuadros se dibujan** mostrando detecciones

## 🔍 Características técnicas

- **Resolución completa**: La IA analiza la imagen original, no el preview
- **Tiempo real**: Actualización automática cada 3 segundos
- **WebSocket**: Comunicación bidireccional
- **Marcado visual**: Recuadros con etiquetas y confianza
- **Responsive**: Funciona en desktop y móvil

## 🛠️ Desarrollo

### Estructura de archivos
```
apt-totem-backend/
├── visualization.html          # Página de visualización
├── api/routers/visualization.py # Endpoints de visualización
├── test_visualization.py       # Script de prueba
└── VISUALIZATION_README.md     # Esta documentación
```

### Personalizar colores
Editar en `visualization.py`:
```python
colors = {
    'clothing': (0, 255, 0),      # Verde
    'color': (0, 165, 255),       # Naranja  
    'accessory': (255, 0, 255),   # Magenta
    'face': (255, 0, 0)          # Rojo
}
```

## 🎯 Beneficios

- ✅ **Transparencia**: Ves exactamente lo que detecta la IA
- ✅ **Debugging**: Fácil identificar errores de detección
- ✅ **Confianza**: Verificación visual de resultados
- ✅ **Desarrollo**: Mejorar algoritmos con feedback visual

¡Ahora puedes ver en tiempo real cómo la IA analiza las imágenes! 🚀



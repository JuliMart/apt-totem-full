# Documentación de API

- Base URL local: `http://localhost:8001`
- Swagger/OpenAPI: `http://localhost:8001/docs`
- Redocs: `http://localhost:8001/redoc` (si está habilitado)

## Endpoints clave (por router)

### CV (Computer Vision)
- `POST /cv/analyze-complete` → Análisis integral (MediaPipe + YOLO). Body: file imagen.
- `POST /cv/detect-clothing-real` → Detección real de prendas.

### Recomendaciones
- `POST /recomendaciones/generar` → Genera recomendaciones por filtros.
- `GET /recomendaciones/top` → Recomendados del día.

### Productos
- `GET /productos` → Lista de productos.
- `GET /product-detail/{id}` → Detalle de producto.

### Búsqueda y Analytics
- `GET /busqueda/sugerencias?q=` → Sugerencias.
- `GET /analytics/kpis` → KPIs agregados.
- `GET /dashboard` → HTML del dashboard dinámico.

### Tracking/Interacciones
- `POST /tracking/event` → Registra interacción.
- `GET /search-analytics/top` → Tendencias de búsqueda.

### Sesiones y Turnos
- `POST /sesiones` | `GET /sesiones/{id}`
- `GET /shifts/current` | `POST /shifts/close`

### Utilidades
- `GET /visualization` → Visualización CV.
- `GET /` → Estado API.

## WebSocket
- `GET /ws` → Canal en tiempo real. Eventos: `connected`, `keepalive`, `realtime_analysis`, `analysis_error`.

## Autenticación
- Entorno demo: libre (CORS `*`). En producción: agregar API Key/JWT.

## Ejemplos (curl)
```bash
# Análisis completo CV
curl -X POST http://localhost:8001/cv/analyze-complete \
  -F "file=@/ruta/imagen.jpg"
```

## Colección Postman
- Archivo: `docs/evidence/postman/NeoTotem_API.postman_collection.json`
- Importa el JSON en Postman y ajusta el `baseUrl` si es necesario.

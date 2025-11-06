# Evidencias del Sistema – Aplicación

## Frontend (Totem / Web)
- Capturas sugeridas (guárdalas en `docs/evidence/screenshots/`):
  - Home del tótem (Flutter) con cámara activa y detecciones.
  - Botón de recomendaciones y tarjetas.
  - Dashboard dinámico (`/dashboard`).
- Video opcional del flujo (login si aplica, búsqueda, recomendación).

## Backend
- Postman funcionando (importa `docs/evidence/postman/NeoTotem_API.postman_collection.json`).
- Swagger en `http://localhost:8001/docs`.
- Logs de ejecución (terminal):
  - Arranque `uvicorn api.main:app ...`
  - Logs de análisis en tiempo real (detecciones y guardado en BD).

## Despliegue
- Sugerencia: Render/Fly/VM + Uvicorn.
- Evidencias: captura del servicio corriendo o URL pública.
- Si usas CI/CD: captura del pipeline o consola de deploy.

## Páginas HTML Demo útiles
- `apt-totem-backend/visualization.html` → Visualización CV.
- `apt-totem-backend/dashboard_dinamico_nuevo.html` → Dashboard moderno.
- `apt-totem-backend/opciones_compra.html` → Opciones de compra.
- `apt-totem-backend/calificar_recomendacion.html` → Calificaciones.

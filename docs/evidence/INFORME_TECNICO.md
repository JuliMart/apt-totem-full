# Informe Técnico - NeoTotem AI Retail

## 1. Introducción
NeoTotem AI es un sistema de visión por computadora y analítica en tiempo real para retail. Detecta prendas, colores, edad aproximada y accesorios; genera recomendaciones y expone un dashboard de negocio.

## 2. Objetivos
- Detectar en tiempo real persona, prenda principal, color y accesorios.
- Generar recomendaciones y medir su aceptación.
- Exponer APIs y dashboard con métricas de negocio.

## 3. Metodología
- Backend FastAPI + MediaPipe/OpenCV para CV, SQLAlchemy para ORM.
- Frontend Flutter para tótem; HTML para dashboards y demos.
- Base de datos relacional (SQLite/MySQL) con modelo de sesiones, interacciones y métricas.
- Pruebas unitarias y scripts de semilla de datos.

## 4. Arquitectura (alto nivel)
- App backend (`apt-totem-backend/api/main.py`) con routers por dominio.
- Servicios de AI en `apt-totem-backend/services/ai/`.
- Modelo de datos en `apt-totem-backend/database/models.py` y SQL en `database/sql/`.
- Frontend Flutter en `frontend/`.

Ver diagramas en `docs/evidence/ARQUITECTURA.md`.

## 5. Avances clave
- Detección real mejorada y ultra conservadora para accesorios y bolsos.
- Criterios ultra estrictos para diferenciar chaqueta vs remera.
- Dashboard dinámico con KPIs y gráficos (ver `/dashboard`).
- Sistema de sesiones, tracking y recomendaciones con persistencia.

## 6. Conclusiones
El sistema funciona de extremo a extremo: captura, análisis, API, almacenamiento y visualización de métricas. Se priorizó precisión (casi cero falsos positivos) y trazabilidad con logs, endpoints y seeds de datos.

## 7. Referencias
- API raíz: `apt-totem-backend/api/main.py`
- Servicios CV: `apt-totem-backend/services/ai/real_detection.py`
- Modelo datos: `apt-totem-backend/database/models.py`
- SQL seeds: `database/sql/`
- Dashboard: `apt-totem-backend/dashboard_dinamico_nuevo.html`

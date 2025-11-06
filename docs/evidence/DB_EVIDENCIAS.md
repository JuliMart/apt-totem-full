# Evidencias de Sistema – Base de Datos

## 1) Diagrama ER
- Ver `docs/evidence/MODELO_DATOS.md` (Mermaid ER).

## 2) Modelo ORM
- Archivo principal: `apt-totem-backend/database/models.py` (SQLAlchemy).

## 3) Scripts SQL (DDL/Seeds)
- Carpeta: `database/sql/`
  - `seed_business_metrics.sql` → genera sesiones, recomendaciones, interacciones y detecciones históricas.

## 4) Capturas de datos
- Recomendación: abre tu cliente SQL y captura tablas:
  - `sesion`, `deteccion`, `recomendacion_sesion`, `interaccion_usuario`, `metricas_sesion`.
- Guarda imágenes en `docs/evidence/screenshots/`.

## 5) Ejemplos de consultas
```sql
-- Detecciones del día
SELECT DATE(fecha_hora) d, COUNT(*) total
FROM deteccion
GROUP BY DATE(fecha_hora)
ORDER BY d DESC;

-- Top colores detectados
SELECT color, COUNT(*) c
FROM deteccion
GROUP BY color
ORDER BY c DESC
LIMIT 5;

-- Tasa de aceptación estimada (clics / vistas)
SELECT
  SUM(CASE WHEN tipo_interaccion='click' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN tipo_interaccion='recommendation_viewed' THEN 1 ELSE 0 END),0) AS tasa_aceptacion
FROM interaccion_usuario;
```

## 6) Ejemplo de API que consulta la BD
- `GET /analytics/kpis` (router analytics) y `GET /dashboard` (HTML + datos) leen métricas calculadas desde la BD.

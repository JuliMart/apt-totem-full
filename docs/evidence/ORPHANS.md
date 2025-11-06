# Inventario de posibles archivos huérfanos / redundantes

Este informe lista artefactos que no están referenciados por el runtime del backend ni montados explícitamente, para evaluación antes de borrar o archivar.

Estado: actualizado tras limpieza inicial.

## 1) Routers API
- Montados en `api/main.py` (include_router):
  - asr, cv, productos, sesiones, recomendaciones, analytics, busqueda, tracking,
    visualization, shifts, product_detail, search_analytics, dashboard,
    calificaciones, calificaciones_grupo, compra, demo, demo_simple,
    visualization_session, session_control
- Archivo no montado detectado:
  - `api/routers/retail_api.py` → ✅ ARCHIVADO en `api/routers/_archive/retail_api.py`

## 2) SQL (artefactos estáticos)
- Uso directo desde backend: no se encontraron referencias a `.sql` dentro de `apt-totem-backend/`.
- ✅ REUBICADO: `database/sql/` → `data/sql/` (actualizadas rutas en `data/sql/README_SQL.md`).

## 3) Scripts en `apt-totem-backend/scripts_backend/`
- Utilitarios: `init_db.py, populate_database.py, migrate_shifts.py, start_neototem.py, update_*_images.py, add_accessories_products.py`.
- Ejemplo:
  - `scripts_backend/ejemplo_analisis_imagenes.py` → ✅ MOVIDO a `docs/examples/ejemplo_analisis_imagenes.py`.

## 4) Esquemas Oracle (legacy)
- `apt-totem-backend/database/schema_oracle11g.sql`
- `apt-totem-backend/database/seeds_oracle11g.sql`
- ✅ ARCHIVADOS en `archive/`.

---

## Plan de limpieza (siguiente etapa)
1. Ventana de observación (2-4 semanas) para confirmar que los archivados no se requieren.
2. Si no hay referencias nuevas, proceder a borrar definitivo de `archive/`.

## Cómo validar (comandos)
```bash
# Routers montados
rg -n "include_router\(" apt-totem-backend/api/main.py

# ¿Se usa retail_api?
rg -n "retail_api" apt-totem-backend || echo "retail_api: sin referencias"

# ¿El backend ejecuta .sql en runtime?
rg -n "\.sql['\"]" apt-totem-backend || echo "backend no ejecuta .sql directamente"
```

## 5) HTML y Python sueltos (organizados)
- ✅ HTML servidos por el backend → movidos a `apt-totem-backend/static/` (rutas actualizadas en `api/main.py`).
- ✅ HTML de demo → movidos a `apt-totem-backend/static/demos/`.
- ✅ Scripts Python de utilidad → movidos a `apt-totem-backend/scripts_backend/utils/`.
- ✅ Scripts Python de demo → movidos a `docs/examples/backend/`.
- ✅ Tests sueltos → movidos a `apt-totem-backend/test/`.

Ver detalles en `docs/evidence/ESTRUCTURA_LIMPIA.md`.

## Notas
- Las evidencias técnicas se centralizaron en `docs/evidence/`.
- `data/` contiene artefactos estáticos (SQL, imágenes, colecciones, etc.).
- Estructura limpia documentada en `docs/evidence/ESTRUCTURA_LIMPIA.md`.

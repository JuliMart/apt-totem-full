# Manual de Usuario y Técnico - NeoTotem AI

## 1. Requisitos
- Python 3.9+
- pip / venv
- Node opcional (solo si se desea servir assets)
- Flutter 3.x (para app de tótem)

## 2. Instalación (Backend)
```bash
cd apt-totem-backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Ejecución (Backend)
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```
- Swagger: `http://localhost:8001/docs`
- Dashboard: `http://localhost:8001/dashboard`
- Visualización CV: `http://localhost:8001/visualization`

## 4. Base de datos
- ORM: `apt-totem-backend/database/models.py`
- Scripts SQL y seeds: `database/sql/`
- Seed de métricas demo (MySQL): `database/sql/seed_business_metrics.sql`

## 5. Frontend (Flutter)
```bash
cd frontend
flutter pub get
flutter run -d chrome
```
- Configura el `WS_URL` o `API_URL` si aplica.

## 6. Despliegue sugerido
- Backend: Render/Fly/VM con `uvicorn` + `--proxy-headers`.
- Archivos estáticos y product images: servir `apt-totem-backend/product_images`.
- BD: MySQL 8/XA o SQLite gestionado.

## 7. Uso rápido
1. Abre la visualización en `/visualization` y concede cámara.
2. Observa detección de prenda/color/edad y logs en tiempo real.
3. Abre `/dashboard` para KPIs de negocio.

## 8. Troubleshooting
- Cámara no carga: verifica permisos del navegador.
- BD vacía: ejecuta los seeds de `database/sql/`.
- CORS: ya viene abierto en `api/main.py` (CORS `*`).

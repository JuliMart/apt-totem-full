# Configuración para servir imágenes en desarrollo

## Para el backend (FastAPI)
Agregar en api/main.py:

```python
from fastapi.staticfiles import StaticFiles

# Servir imágenes estáticas
app.mount("/product_images", StaticFiles(directory="product_images"), name="product_images")
```

## Para el frontend (Flutter Web)
Las URLs ya están configuradas como:
- http://127.0.0.1:8000/product_images/nike/nike-air-max-270-negro-40.jpg

## Estructura final:
```
apt-totem/
├── product_images/          # Carpeta de imágenes
│   ├── nike/
│   ├── adidas/
│   └── ...
├── apt-totem-backend/       # Backend
└── frontend/               # Frontend
```

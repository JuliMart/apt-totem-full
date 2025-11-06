# 🧠 NeoTotem AI - Backend

> FastAPI + MediaPipe + OpenCV - Sistema de detección inteligente en tiempo real

---

## 📁 Estructura Organizada

```
apt-totem-backend/
├── 📄 README.md                           ← Este archivo
│
├── 📁 api/                                ← Rutas y endpoints
│   ├── main.py                           ← ⭐⭐⭐ WebSocket + FastAPI
│   └── routers/
│       ├── cv.py                         ← Computer Vision endpoints
│       ├── shifts.py                     ← Gestión de turnos
│       └── tracking.py                   ← Analytics y tracking
│
├── 📁 services/                           ← Lógica de negocio
│   ├── ai/
│   │   ├── real_detection.py            ← ⭐⭐⭐ CORE IA (MUY IMPORTANTE)
│   │   ├── mediapipe_engine.py          ← Motor MediaPipe
│   │   └── simple_ai.py                 ← IA simple (fallback)
│   │
│   ├── cv/                               ← Computer Vision
│   │   ├── color.py                     ← Análisis de colores
│   │   └── detector.py                  ← Detección de prendas
│   │
│   ├── asr/                              ← Speech Recognition
│   │   └── engine.py
│   │
│   ├── nlu/                              ← Natural Language
│   │   └── heuristics.py
│   │
│   ├── shift_manager.py                  ← Gestión de turnos
│   ├── cron_jobs.py                      ← Tareas programadas
│   └── recommendation_engine.py          ← Recomendaciones
│
├── 📁 database/                           ← Base de datos
│   ├── models.py                         ← ⭐ Modelos SQLAlchemy
│   └── database.py                       ← Configuración BD
│
├── 📁 docs_backend/                       ← Documentación técnica
│   ├── system/                           ← Docs del sistema actual
│   │   ├── SISTEMA_TURNOS_DETECCIONES.md
│   │   ├── VISUALIZACION_CV_CRUDA.md
│   │   ├── MEJORAS_DETECCION_PRENDAS.md
│   │   └── MEJORAS_VISUALIZACION_Y_ACCESORIOS.md
│   │
│   ├── legacy/                           ← Docs obsoletas
│   └── README_RETAIL.md                  ← Contexto retail
│
├── 📁 scripts_backend/                    ← Scripts de utilidad
│   ├── init_db.py                        ← Inicializar BD
│   ├── migrate_shifts.py                 ← Migrar turnos
│   ├── populate_database.py              ← Poblar BD
│   ├── start_neototem.py                 ← Iniciar sistema
│   └── ejemplo_analisis_imagenes.py      ← Ejemplo de uso
│
├── 📄 visualization.html                  ← Debug en tiempo real
├── 📄 requirements.txt                    ← ⭐ Dependencias Python
└── 📄 .env                                ← Configuración (crear este)
```

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
cd apt-totem-backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Base de Datos

```bash
# Opción A: Usar scripts en database/sql (recomendado)
mysql -u root -p < ../database/sql/schema_mysql_completo.sql
mysql -u root -p < ../database/sql/populate_mysql_complete.sql

# Opción B: Usar script Python
python scripts_backend/init_db.py
python scripts_backend/populate_database.py
```

### 3. Iniciar Servidor

```bash
# Desarrollo (con reload)
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

# Producción
uvicorn api.main:app --host 0.0.0.0 --port 8001 --workers 4
```

✅ Backend corriendo en: `http://localhost:8001`

---

## 📊 Endpoints Principales

### REST API

```bash
# Health check
GET http://localhost:8001/

# Detectar frame
POST http://localhost:8001/cv/detect-frame
Content-Type: multipart/form-data
Body: file=@image.jpg

# Análisis completo con IA
POST http://localhost:8001/cv/analyze-customer-ai-real
Content-Type: multipart/form-data
Body: file=@image.jpg

# Turno actual
GET http://localhost:8001/shifts/current

# Analytics
GET http://localhost:8001/shifts/analytics
```

### WebSocket

```javascript
// Conectar
const ws = new WebSocket('ws://localhost:8001/ws');

// Enviar imagen
ws.send(JSON.stringify({
  type: "image_stream",
  image_data: "base64_encoded_image",
  camera_active: true
}));

// Recibir análisis
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.analysis);
};
```

---

## 🔧 Scripts Útiles

### Inicializar Sistema

```bash
# Crear tablas de BD
python scripts_backend/init_db.py

# Migrar sistema de turnos
python scripts_backend/migrate_shifts.py

# Poblar con datos de ejemplo
python scripts_backend/populate_database.py

# Iniciar sistema completo
python scripts_backend/start_neototem.py
```

### Testing

```bash
# Tests están en /tests (raíz del proyecto)
cd ..
python tests/test_real_detection.py
python tests/test_shift_system.py
python tests/test_recommendations.py
```

---

## 📚 Documentación

### Documentación del Sistema (Actualizada)

- **[SISTEMA_TURNOS_DETECCIONES.md](docs_backend/system/SISTEMA_TURNOS_DETECCIONES.md)** - Sistema de turnos y almacenamiento
- **[VISUALIZACION_CV_CRUDA.md](docs_backend/system/VISUALIZACION_CV_CRUDA.md)** - Visualización en tiempo real
- **[MEJORAS_DETECCION_PRENDAS.md](docs_backend/system/MEJORAS_DETECCION_PRENDAS.md)** - Algoritmos de detección de ropa
- **[MEJORAS_VISUALIZACION_Y_ACCESORIOS.md](docs_backend/system/MEJORAS_VISUALIZACION_Y_ACCESORIOS.md)** - Detección de accesorios

### Documentación General del Proyecto

Ver carpeta raíz: `../docs/guides/`

---

## 🎯 Archivos Clave

| Archivo | Importancia | Descripción |
|---------|------------|-------------|
| **services/ai/real_detection.py** | ⭐⭐⭐ | CORE - Toda la lógica de IA |
| **api/main.py** | ⭐⭐⭐ | WebSocket + Routing principal |
| **database/models.py** | ⭐⭐ | Modelos de BD |
| **services/shift_manager.py** | ⭐⭐ | Gestión de turnos |
| **services/cron_jobs.py** | ⭐⭐ | Tareas programadas |
| **requirements.txt** | ⭐⭐ | Dependencias |

---

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

```bash
# Verificar que estás en el entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Error: Can't connect to MySQL

```bash
# Verificar que MySQL está corriendo
mysql -u root -p

# Crear base de datos si no existe
mysql -u root -p -e "CREATE DATABASE neototem;"
```

### Error: MediaPipe no funciona

```bash
# Reinstalar MediaPipe
pip uninstall mediapipe
pip install mediapipe==0.10.9
```

---

## 🔄 Actualizar Dependencias

```bash
# Ver dependencias instaladas
pip list

# Actualizar requirements.txt
pip freeze > requirements.txt

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

---

## 📈 Monitoreo

### Visualización en Tiempo Real

Abrir en navegador:
```
http://localhost:8001/visualization
```

### Logs

```bash
# Ver logs en tiempo real
tail -f logs/app.log

# O simplemente ver stdout
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 🚢 Deployment

### Desarrollo

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

### Producción

```bash
# Con Gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

# O con Uvicorn directo
uvicorn api.main:app --host 0.0.0.0 --port 8001 --workers 4
```

---

## 📞 Soporte

- Documentación completa: `../docs/guides/INICIO_AQUI.md`
- Arquitectura técnica: `../docs/guides/ARQUITECTURA_TECNICA.md`
- Issues: Ver troubleshooting arriba

---

**Última actualización:** 2025-10-20  
**Versión:** 1.0.0  
**Stack:** FastAPI + MediaPipe + OpenCV + SQLAlchemy

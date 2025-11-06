# 📁 Estructura del Proyecto - NeoTotem AI

> Guía de organización de archivos y carpetas

---

## 🗂️ Vista General

```
apt-totem/
│
├── 📄 README.md                           ← Empieza aquí
│
├── 📁 docs/                               ← TODA la documentación
│   ├── guides/                            ← Guías principales  
│   └── legacy/                            ← Documentos obsoletos
│
├── 📁 frontend/                           ← App Flutter Web (UI cliente)
├── 📁 apt-totem-backend/                  ← Backend FastAPI (cerebro)
├── 📁 tests/                              ← Tests y debug scripts
├── 📁 scripts/                            ← Scripts auxiliares
└── 📁 database/                           ← SQL y datos
```

---

## 📚 `/docs` - Documentación

### `/docs/guides/` - Guías Principales

| Archivo | Propósito | Audiencia |
|---------|-----------|-----------|
| **INICIO_AQUI.md** | 🎯 **Punto de entrada** - Empieza aquí | Todos |
| **INDICE_DOCUMENTACION.md** | Índice de toda la documentación | Todos |
| **GUIA_COMPLETA_APLICACION.md** | Explicación técnica completa (Frontend + Backend) | Desarrolladores |
| **GUIA_SIMPLE_NO_TECNICOS.md** | Guía sin tecnicismos para uso diario | Gerentes, vendedores |
| **ARQUITECTURA_TECNICA.md** | Diagramas, flujos de datos, código avanzado | Arquitectos, tech leads |

**Orden de lectura recomendado:**
1. `INICIO_AQUI.md` (5 min)
2. Si eres dev: `GUIA_COMPLETA_APLICACION.md` (30 min)
3. Si no eres dev: `GUIA_SIMPLE_NO_TECNICOS.md` (15 min)

### `/docs/legacy/` - Documentos Obsoletos

Documentos de versiones antiguas que ya no se usan pero se mantienen por referencia histórica:
- `IMAGE_GENERATION_INSTRUCTIONS.md`
- `IMAGE_SERVER_CONFIG.md`
- `IMAGE_UPLOAD_GUIDE.md`
- `INTEGRACION_COMPLETA.md`

---

## 🎨 `/frontend` - Flutter Web Application

```
frontend/
├── lib/
│   ├── main.dart                    # Entry point de la app
│   ├── home_screen.dart             # ⭐ IMPORTANTE: Pantalla principal
│   ├── retail_screen.dart           # Pantalla retail
│   │
│   ├── models/                      # Modelos de datos
│   ├── services/                    # Servicios (WebSocket, API)
│   └── widgets/                     # Widgets reutilizables
│
├── web/                             # Recursos web
├── fonts/                           # Fuentes personalizadas
├── pubspec.yaml                     # ⭐ Dependencias Flutter
└── analysis_options.yaml            # Configuración de linter
```

**Archivos clave:**
- `home_screen.dart` - Toda la lógica de cámara, WebSocket, análisis en tiempo real
- `pubspec.yaml` - Si faltan dependencias, revisar aquí

---

## 🧠 `/apt-totem-backend` - FastAPI Backend

```
apt-totem-backend/
├── api/
│   ├── main.py                      # ⭐⭐⭐ IMPORTANTE: WebSocket + Routes
│   └── routers/
│       ├── cv.py                    # Endpoints de computer vision
│       ├── shifts.py                # Endpoints de turnos
│       └── tracking.py              # Endpoints de tracking/analytics
│
├── services/
│   ├── ai/
│   │   ├── real_detection.py        # ⭐⭐⭐ MUY IMPORTANTE: CORE IA
│   │   ├── mediapipe_engine.py      # Motor MediaPipe
│   │   └── simple_ai.py             # IA simple (fallback)
│   │
│   ├── cv/
│   │   ├── color.py                 # Análisis de colores
│   │   └── detector.py              # Detección de prendas
│   │
│   ├── asr/
│   │   └── engine.py                # Reconocimiento de voz
│   │
│   ├── nlu/
│   │   └── heuristics.py            # Procesamiento de lenguaje natural
│   │
│   ├── shift_manager.py             # Gestión de turnos
│   ├── cron_jobs.py                 # Tareas programadas
│   └── recommendation_engine.py     # Motor de recomendaciones
│
├── database/
│   ├── models.py                    # ⭐ Modelos SQLAlchemy (BD)
│   └── database.py                  # Configuración de BD
│
├── visualization.html               # Página de debug en tiempo real
├── requirements.txt                 # ⭐ Dependencias Python
├── init_db.py                       # Script para inicializar BD
├── migrate_shifts.py                # Script para migrar turnos
│
└── Documentación técnica:
    ├── SISTEMA_TURNOS_DETECCIONES.md
    ├── VISUALIZACION_CV_CRUDA.md
    ├── MEJORAS_DETECCION_PRENDAS.md
    └── MEJORAS_VISUALIZACION_Y_ACCESORIOS.md
```

**Archivos clave:**
- `api/main.py` - WebSocket handler, broadcast a todos los clientes
- `services/ai/real_detection.py` - **EL MÁS IMPORTANTE**: toda la lógica de detección con MediaPipe
- `database/models.py` - Estructura de la base de datos
- `requirements.txt` - Si falta alguna librería, instalar desde aquí

---

## 🧪 `/tests` - Testing y Debug

```
tests/
├── debug/
│   ├── backend_debug.py             # Debug del backend
│   ├── debug_analysis.py            # Debug de análisis
│   ├── simple_debug.py              # Debug simple
│   └── debug_frame_*.jpg            # Imágenes de debug
│
├── test_deteccion_realista.py       # Test de detección
├── test_gorro_detection.py          # Test de gorros
├── test_gorro_real.py               # Test de gorros real
└── (otros test_*.py)
```

**Cómo usar:**
```bash
# Ejecutar test específico
python tests/test_deteccion_realista.py

# Debug de análisis
python tests/debug/debug_analysis.py
```

---

## 🔧 `/scripts` - Scripts Auxiliares

```
scripts/
├── generation/
│   ├── generate_with_dalle.py       # Generación de imágenes con DALL-E
│   └── map_generated_images.py      # Mapeo de imágenes generadas
│
└── convert_oracle_to_mysql.py       # Conversión de BD Oracle a MySQL
```

**Uso común:**
```bash
# Generar imágenes de productos
python scripts/generation/generate_with_dalle.py
```

---

## 💾 `/database` - Base de Datos

```
database/
├── sql/
│   ├── populate_mysql_complete.sql  # Poblar BD completa
│   ├── populate_mysql_simple.sql    # Poblar BD simple
│   ├── schema_mysql_completo.sql    # Schema completo
│   └── update_*.sql                 # Scripts de actualización
│
├── product_image_list.json          # Lista de imágenes de productos
└── product_image_prompts.json       # Prompts para generar imágenes
```

**Uso:**
```bash
# Poblar base de datos
mysql -u root -p < database/sql/populate_mysql_complete.sql
```

---

## 🎯 Archivos Más Importantes

### Top 5 - Los que DEBES conocer:

| # | Archivo | Por qué es importante |
|---|---------|----------------------|
| 1 | **apt-totem-backend/services/ai/real_detection.py** | 🥇 **CORE IA** - Toda la lógica de detección (MediaPipe, OpenCV) |
| 2 | **apt-totem-backend/api/main.py** | 🥈 WebSocket, broadcasting, routing |
| 3 | **frontend/lib/home_screen.dart** | 🥉 UI principal, cámara, WebSocket client |
| 4 | **apt-totem-backend/database/models.py** | Estructura de BD (turnos, detecciones, etc.) |
| 5 | **docs/guides/GUIA_COMPLETA_APLICACION.md** | Explicación de TODO el sistema |

---

## 📍 ¿Dónde está...?

### "¿Dónde está la documentación?"
→ `docs/guides/INICIO_AQUI.md` (empieza aquí)

### "¿Dónde está la lógica de detección de IA?"
→ `apt-totem-backend/services/ai/real_detection.py`

### "¿Dónde está el WebSocket?"
→ `apt-totem-backend/api/main.py` (servidor)  
→ `frontend/lib/home_screen.dart` (cliente)

### "¿Dónde está la página de visualización?"
→ `apt-totem-backend/visualization.html`

### "¿Dónde están los modelos de BD?"
→ `apt-totem-backend/database/models.py`

### "¿Dónde están los tests?"
→ `tests/` (raíz del proyecto)

### "¿Dónde están los scripts SQL?"
→ `database/sql/`

### "¿Dónde está la configuración de turnos?"
→ `apt-totem-backend/services/shift_manager.py`  
→ `apt-totem-backend/services/cron_jobs.py`

---

## 🗑️ Archivos Ignorados

Los siguientes NO están en Git (configurado en `.gitignore`):

```
# Python
__pycache__/
*.pyc
.venv/
venv/

# Flutter
build/
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies

# Base de datos
*.db
*.sqlite

# Imágenes generadas
generated_images/
debug_frame_*.jpg

# Configuración local
.env
```

---

## 📋 Checklist de Archivos Requeridos

Antes de deployment, verifica que existan:

### Backend:
- [x] `apt-totem-backend/requirements.txt`
- [x] `apt-totem-backend/api/main.py`
- [x] `apt-totem-backend/services/ai/real_detection.py`
- [x] `apt-totem-backend/database/models.py`
- [x] `apt-totem-backend/visualization.html`

### Frontend:
- [x] `frontend/pubspec.yaml`
- [x] `frontend/lib/main.dart`
- [x] `frontend/lib/home_screen.dart`

### Documentación:
- [x] `README.md` (raíz)
- [x] `docs/guides/INICIO_AQUI.md`
- [x] `docs/guides/GUIA_COMPLETA_APLICACION.md`

### Base de Datos:
- [x] `database/sql/schema_mysql_completo.sql`
- [x] `database/sql/populate_mysql_complete.sql`

---

## 🔄 Cómo Navegar el Proyecto

### Nuevo en el proyecto:
1. Lee `README.md` (raíz)
2. Lee `docs/guides/INICIO_AQUI.md`
3. Elige tu camino:
   - Dev → `docs/guides/GUIA_COMPLETA_APLICACION.md`
   - No-dev → `docs/guides/GUIA_SIMPLE_NO_TECNICOS.md`

### Trabajar en Frontend:
```
frontend/lib/home_screen.dart ← Empieza aquí
```

### Trabajar en Backend/IA:
```
apt-totem-backend/services/ai/real_detection.py ← Empieza aquí
```

### Trabajar en BD:
```
apt-totem-backend/database/models.py ← Empieza aquí
```

### Debuggear:
```
apt-totem-backend/visualization.html ← Abre en navegador
http://localhost:8001/visualization
```

---

## 📞 Ayuda

¿No encuentras algo?
1. Revisa `docs/guides/INDICE_DOCUMENTACION.md`
2. Busca en el proyecto: `grep -r "texto_buscado" .`
3. Consulta esta guía

---

**Última actualización:** 2025-10-20  
**Versión:** 1.0.0


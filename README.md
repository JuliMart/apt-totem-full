# 🤖 NeoTotem AI - Sistema Inteligente de Análisis Visual para Retail

<div align="center">

![Status](https://img.shields.io/badge/Status-Producción-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-Propietario-red)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Flutter](https://img.shields.io/badge/Flutter-3.7+-blue)

**Sistema de totem inteligente que detecta vestimenta y accesorios en tiempo real usando IA**

[Instalación](#-instalación) • [Uso](#-uso-rápido) • [Documentación](#-documentación) • [Demo](#-demo)

</div>

## 📦 Repositorios

Este es el **monorepo completo** que contiene frontend, backend, datos y documentación.

- **Frontend (Flutter)**: [JuliMart/apt-totem](https://github.com/JuliMart/apt-totem)
- **Backend (FastAPI)**: [JuliMart/apt-totem-backend](https://github.com/JuliMart/apt-totem-backend)
- **Monorepo (Todo junto)**: [JuliMart/apt-totem-full](https://github.com/JuliMart/apt-totem-full) ← Este repo

---

## 📋 Descripción

NeoTotem AI es un sistema completo de análisis visual para tiendas de ropa que utiliza inteligencia artificial (MediaPipe + OpenCV) para:

- 🎯 **Detectar en tiempo real** qué ropa lleva puesto un cliente
- 🎨 **Analizar colores** dominantes y secundarios
- 👓 **Identificar accesorios** (gorras, gafas, carteras, mochilas)
- 💡 **Recomendar productos** basados en lo detectado
- 📊 **Generar analytics** por turnos de trabajo
- 🎤 **Interactuar por voz** con el cliente

---

## 🏗️ Arquitectura

```
┌────────────────────────────────────────────────────────────────────┐
│                         NEOTOTEM AI SYSTEM                          │
└────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐             ┌──────────────────┐
    │   FRONTEND      │◄───────────►│     BACKEND      │
    │   Flutter Web   │  WebSocket  │   FastAPI/Python │
    │                 │             │                  │
    │  • Camera       │             │  • MediaPipe     │
    │  • Microphone   │             │  • OpenCV        │
    │  • UI           │             │  • AI Detection  │
    └─────────────────┘             └──────────────────┘
                                             │
                                             │
                        ┌────────────────────┴────────────────┐
                        │                                     │
                        ▼                                     ▼
              ┌──────────────────┐              ┌──────────────────┐
              │   VISUALIZATION  │              │    DATABASE      │
              │      HTML        │              │     SQLite       │
              │                  │              │                  │
              │  • Debug View    │              │  • Detections    │
              │  • Monitoring    │              │  • Shifts        │
              │  • Metrics       │              │  • Analytics     │
              └──────────────────┘              └──────────────────┘
```

---

## ✨ Características Principales

### 🎯 Detección Inteligente

| Categoría | Qué detecta | Precisión |
|-----------|-------------|-----------|
| **Vestimenta** | Chaqueta, sudadera, camiseta manga larga, camiseta | ~92% |
| **Colores** | Color primario + secundario | ~88% |
| **Accesorios Cabeza** | Gorra, gorro, gafas | ~85% |
| **Carteras/Bolsos** | Mochila, bolso cruzado, cartera, bolso | ~80% |
| **Edad** | Rango estimado (18-25, 26-35, etc.) | ~75% |

### ⚡ Rendimiento

- **FPS:** ~3 frames por segundo (300ms por análisis)
- **Latencia:** <500ms desde captura hasta resultado
- **Tiempo real:** Sí, actualización continua
- **Concurrencia:** Múltiples clientes WebSocket simultáneos

### 📊 Analytics

- ✅ Reportes por turno (mañana/tarde/noche)
- ✅ Estadísticas agregadas (prendas más vistas, colores populares)
- ✅ Tendencias semanales/mensuales
- ✅ Exportación de datos

---

## 🚀 Instalación

### Requisitos Previos

```bash
# Sistema Operativo
- macOS 10.15+ / Windows 10+ / Linux

# Software Requerido
- Python 3.11+
- Flutter 3.7+
- Chrome/Edge (navegador moderno)

# Hardware Recomendado
- CPU: 4 cores+
- RAM: 8GB+
- Cámara HD (720p+)
- Micrófono
```

### 1. Clonar Repositorio

```bash
git clone https://github.com/tu-org/apt-totem.git
cd apt-totem
```

### 2. Configurar Backend

```bash
cd apt-totem-backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python init_db.py
python migrate_shifts.py

# Iniciar servidor
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
flutter pub get

# Iniciar en Chrome
flutter run -d chrome --web-port=8080
```

### 4. Verificar Instalación

```bash
# Backend debe estar en: http://localhost:8001
# Frontend debe estar en: http://localhost:8080
# Visualización: http://localhost:8001/visualization
```

---

## 🎮 Uso Rápido

### Para Usuarios (Cliente)

1. **Acércate al totem**
2. **Presiona "Activar Cámara"**
3. El sistema detecta automáticamente tu ropa
4. **Ver recomendaciones** en pantalla
5. **Habla al micrófono** para búsqueda por voz (opcional)

### Para Administradores

```bash
# Ver monitoreo en tiempo real
http://localhost:8001/visualization

# Ver estadísticas del turno actual
curl http://localhost:8001/shifts/current

# Ver analytics general
curl http://localhost:8001/shifts/analytics
```

---

## 🧪 Testing

```bash
# Backend - Tests unitarios
cd apt-totem-backend
pytest

# Backend - Test específico de detección
python test_real_detection.py

# Backend - Test de sistema de turnos
python test_shift_system.py

# Frontend - Tests
cd frontend
flutter test
```

---

## 📚 Documentación

### Guías Disponibles

| Documento | Audiencia | Descripción |
|-----------|-----------|-------------|
| **[docs/guides/INICIO_AQUI.md](docs/guides/INICIO_AQUI.md)** | Todos | 🎯 **Empieza aquí** - Punto de entrada principal |
| **[docs/guides/GUIA_COMPLETA_APLICACION.md](docs/guides/GUIA_COMPLETA_APLICACION.md)** | Desarrolladores | Guía técnica completa del sistema |
| **[docs/guides/GUIA_SIMPLE_NO_TECNICOS.md](docs/guides/GUIA_SIMPLE_NO_TECNICOS.md)** | Gerentes/Vendedores | Guía sin tecnicismos para uso diario |
| **[apt-totem-backend/SISTEMA_TURNOS_DETECCIONES.md](apt-totem-backend/SISTEMA_TURNOS_DETECCIONES.md)** | Técnicos | Sistema de turnos y almacenamiento |
| **[apt-totem-backend/VISUALIZACION_CV_CRUDA.md](apt-totem-backend/VISUALIZACION_CV_CRUDA.md)** | Técnicos | Visualización en tiempo real |
| **[apt-totem-backend/MEJORAS_DETECCION_PRENDAS.md](apt-totem-backend/MEJORAS_DETECCION_PRENDAS.md)** | Desarrolladores | Detalles de algoritmos de detección |

### Estructura del Proyecto

```
apt-totem/
├── 📄 README.md                           # Este archivo
│
├── 📁 docs/                               # 📚 Documentación
│   ├── guides/                            # Guías principales
│   │   ├── INICIO_AQUI.md                # 🎯 Empieza aquí
│   │   ├── GUIA_COMPLETA_APLICACION.md   # Guía técnica completa
│   │   ├── GUIA_SIMPLE_NO_TECNICOS.md    # Guía para no técnicos
│   │   ├── ARQUITECTURA_TECNICA.md       # Arquitectura detallada
│   │   └── INDICE_DOCUMENTACION.md       # Índice de docs
│   └── legacy/                            # Docs obsoletas
│
├── 📁 frontend/                           # Flutter Web App
│   ├── lib/
│   │   ├── main.dart                     # Entry point
│   │   └── home_screen.dart              # ⭐ Pantalla principal
│   └── pubspec.yaml
│
├── 📁 apt-totem-backend/                  # FastAPI Backend
│   ├── api/
│   │   ├── main.py                       # ⭐ WebSocket + Routes
│   │   └── routers/
│   ├── services/
│   │   ├── ai/
│   │   │   └── real_detection.py         # ⭐⭐⭐ CORE IA
│   │   ├── cv/
│   │   ├── shift_manager.py
│   │   └── cron_jobs.py
│   ├── database/
│   ├── visualization.html
│   └── requirements.txt
│
├── 📁 tests/                              # Tests y debug
│   ├── debug/                             # Scripts de debug
│   └── test_*.py                          # Tests unitarios
│
├── 📁 scripts/                            # Scripts auxiliares
│   └── generation/                        # Generación de imágenes
│
└── 📁 database/                           # Base de datos y SQL
    ├── sql/                               # Scripts SQL
    └── *.json                             # Datos de configuración
```

---

## 🔧 Configuración Avanzada

### Ajustar Velocidad de Detección

```dart
// frontend/lib/home_screen.dart (línea ~315)
Future.delayed(Duration(milliseconds: 300), () async {
  // Opciones:
  // 100ms = 10 FPS (muy rápido, alto CPU)
  // 200ms = 5 FPS (rápido)
  // 300ms = 3 FPS (balanceado) ← Actual
  // 500ms = 2 FPS (conservar recursos)
});
```

### Ajustar Umbrales de Detección

```python
# apt-totem-backend/services/ai/real_detection.py (línea ~388)

# Para detectar "chaqueta" necesita:
if shoulder_distance > 0.25 and torso_height > 0.40 and arm_coverage > 0.20:
    clothing_detected = "chaqueta"
    
# Aumentar valores → Más estricto (menos falsos positivos)
# Disminuir valores → Más permisivo (más detecciones)
```

### Configurar Horarios de Turnos

```python
# apt-totem-backend/services/cron_jobs.py (línea ~45)

# Turno Mañana: 06:00
schedule.every().day.at("06:00").do(start_morning_shift)

# Turno Tarde: 14:00
schedule.every().day.at("14:00").do(start_afternoon_shift)

# Turno Noche: 22:00
schedule.every().day.at("22:00").do(start_night_shift)
```

---

## 🎨 Visualización Debug

La página de visualización muestra en tiempo real qué está detectando la IA:

```
http://localhost:8001/visualization
```

**Bounding Boxes:**
- 🟢 **Verde** = Cara/Persona detectada
- 🟠 **Naranja** = Vestimenta (cuerpo superior)
- 🟣 **Magenta** = Accesorios de cabeza (gorra, gafas)
- 🔵 **Cian** = Carteras/Bolsos

**Panel de Información:**
- Prenda detectada
- Estilo (casual, formal, deportivo)
- Colores (primario + secundario)
- Accesorios
- Edad estimada

**Debug Terminal:**
```
[14:32:15] 🔍 DEBUG - Métricas de detección:
[14:32:15]   Distancia hombros: 0.156
[14:32:15]   Altura torso: 0.285
[14:32:15]   ✅ DETECTADO: camiseta (casual)
[14:32:16] 🎩 Accesorios: gorra, gafas
[14:32:16] 👜 Cartera: bolso_cruzado
```

---

## 📊 API Endpoints

### WebSocket

```javascript
// Conectar
ws://localhost:8001/ws

// Enviar imagen
{
  "type": "image_stream",
  "image_data": "base64_encoded_image",
  "camera_active": true
}

// Respuesta
{
  "type": "realtime_analysis",
  "analysis": {
    "clothing_item": "camiseta",
    "primary_color": "negro",
    "head_accessory": "gorra",
    // ...
  },
  "annotated_image": "base64_image_with_boxes"
}
```

### REST Endpoints

```bash
# Detección de frame
POST /cv/detect-frame
Content-Type: multipart/form-data
Body: file=@image.jpg

# Analytics del turno actual
GET /shifts/current

# Resumen de turno específico
GET /shifts/{shift_id}/summary

# Analytics general
GET /shifts/analytics
```

---

## 🐛 Troubleshooting

### Problema: No detecta nada

**Solución:**
1. Verificar iluminación (necesita luz adecuada)
2. Acercarse más a la cámara (2-3 metros)
3. Verificar que backend esté corriendo
4. Revisar logs en terminal

### Problema: Siempre detecta "chaqueta"

**Solución:**
Los umbrales están muy bajos. Aumentar en `real_detection.py`:
```python
shoulder_distance > 0.26  # Era 0.25
torso_height > 0.42       # Era 0.40
arm_coverage > 0.22       # Era 0.20
```

### Problema: Visualización no actualiza

**Solución:**
1. Recargar página (F5)
2. Verificar que Flutter esté enviando imágenes
3. Verificar WebSocket conectado (icono verde en /visualization)
4. Revicar logs de backend

### Problema: Cámara no funciona

**Solución:**
1. Dar permisos de cámara en el navegador
2. Verificar que ninguna otra app use la cámara
3. Probar con otro navegador (Chrome recomendado)

---

## 🚢 Deployment

### Desarrollo
```bash
# Ya configurado con --reload
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

### Producción

```bash
# Sin --reload, con workers
uvicorn api.main:app --host 0.0.0.0 --port 8001 --workers 4

# O con Gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### Docker (Opcional)

```dockerfile
# Dockerfile próximamente
```

---

## 🔐 Seguridad y Privacidad

### ¿Qué datos almacena?

✅ **SÍ almacena:**
- Análisis de detección (ej: "camiseta negra detectada")
- Timestamp de detección
- Estadísticas agregadas por turno

❌ **NO almacena:**
- Imágenes/fotos de clientes
- Videos
- Datos personales identificables
- Información facial biométrica

### Cumplimiento GDPR

El sistema está diseñado para **no** almacenar datos personales. Solo guarda metadatos de detección que no permiten identificar individuos.

---

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Añade nueva funcionalidad'`
4. Push al branch: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

---

## 📜 Licencia

Copyright © 2025 NeoTotem AI. Todos los derechos reservados.

Este software es propietario y confidencial. No autorizado para distribución pública.

---

## 📞 Soporte

- 📧 Email: soporte@neototem.com
- 📱 WhatsApp: +XX XXX XXX XXXX
- 🌐 Web: www.neototem.com
- 💬 Discord: [Servidor de soporte]

---

## 🎯 Roadmap

### v1.1 (Próximamente)
- [ ] Detección de pantalones/faldas (parte inferior)
- [ ] Múltiples personas simultáneas
- [ ] Integración con sistema de inventario
- [ ] App móvil nativa

### v1.2
- [ ] Reconocimiento de marcas (logos)
- [ ] Detección de patrones (rayas, cuadros, etc.)
- [ ] Recomendaciones con ML personalizado
- [ ] Dashboard web de analytics

### v2.0
- [ ] Reconocimiento facial (opt-in con consentimiento)
- [ ] Historial de cliente recurrente
- [ ] Integración con sistema de pagos
- [ ] Multi-idioma

---

## 📈 Estado del Proyecto

```
Backend:  ████████████████████ 100% ✅
Frontend: ████████████████████ 100% ✅
Testing:  ████████████░░░░░░░░  65% 🔄
Docs:     ████████████████████ 100% ✅
Deploy:   ████████░░░░░░░░░░░░  40% 🔄
```

---

## 🙏 Agradecimientos

- **MediaPipe** - Google's ML solutions
- **OpenCV** - Computer Vision library
- **Flutter** - UI framework
- **FastAPI** - Modern Python web framework

---

<div align="center">

**Hecho con ❤️ para revolucionar la experiencia retail**

[⬆ Volver arriba](#-neototem-ai---sistema-inteligente-de-análisis-visual-para-retail)

</div>


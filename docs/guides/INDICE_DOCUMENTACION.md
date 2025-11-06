# 📚 Índice de Documentación - NeoTotem AI

> **Guía completa para encontrar la documentación que necesitas**

---

## 🎯 ¿Qué documento necesitas?

### 👨‍💼 **Para Gerentes y Personal No Técnico**

**📄 [GUIA_SIMPLE_NO_TECNICOS.md](GUIA_SIMPLE_NO_TECNICOS.md)**
- ✅ Sin términos técnicos complicados
- ✅ Explicación visual con ejemplos
- ✅ Cómo usar el sistema día a día
- ✅ Interpretación de estadísticas
- ✅ Solución de problemas básicos
- ✅ Checklist diario

**👥 Audiencia:** Gerentes de tienda, vendedores, personal operativo

---

### 👨‍💻 **Para Desarrolladores**

**📄 [GUIA_COMPLETA_APLICACION.md](GUIA_COMPLETA_APLICACION.md)**
- ✅ Arquitectura completa del sistema
- ✅ Explicación de cada componente (Frontend, Backend, BD)
- ✅ Flujo de datos detallado
- ✅ Archivos importantes y qué hace cada uno
- ✅ Configuración y ajustes
- ✅ Troubleshooting técnico

**👥 Audiencia:** Desarrolladores full-stack, ingenieros de software

---

**📄 [ARQUITECTURA_TECNICA.md](ARQUITECTURA_TECNICA.md)**
- ✅ Diagramas técnicos detallados
- ✅ Flujo de datos paso a paso (código incluido)
- ✅ Modelos de base de datos
- ✅ Componentes principales con código
- ✅ Estrategia de testing
- ✅ Optimizaciones implementadas
- ✅ Deployment checklist

**👥 Audiencia:** Arquitectos de software, tech leads, DevOps

---

### 🎨 **Para Todos (Inicio Rápido)**

**📄 [README.md](README.md)**
- ✅ Overview del proyecto
- ✅ Instalación rápida
- ✅ Características principales
- ✅ Uso básico
- ✅ API endpoints
- ✅ Troubleshooting común
- ✅ Roadmap

**👥 Audiencia:** Cualquiera que quiera entender el proyecto

---

## 📑 Documentación Especializada

### 🔄 Sistema de Turnos

**📄 [SISTEMA_TURNOS_DETECCIONES.md](apt-totem-backend/SISTEMA_TURNOS_DETECCIONES.md)**
- Cómo funciona el sistema de turnos (mañana/tarde/noche)
- Almacenamiento de detecciones
- Agregación de datos por turno
- Cron jobs automáticos
- API endpoints de turnos

**👥 Para:** Desarrolladores backend, administradores de sistema

---

### 🎥 Visualización en Tiempo Real

**📄 [VISUALIZACION_CV_CRUDA.md](apt-totem-backend/VISUALIZACION_CV_CRUDA.md)**
- Página de visualización debug
- Bounding boxes y colores
- WebSocket streaming
- Imagen anotada en tiempo real
- Monitoreo de detecciones

**👥 Para:** Desarrolladores, QA testers, técnicos de soporte

---

### 👕 Detección de Prendas

**📄 [MEJORAS_DETECCION_PRENDAS.md](apt-totem-backend/MEJORAS_DETECCION_PRENDAS.md)**
- Algoritmos de detección de ropa
- Umbrales y criterios
- Métricas utilizadas (hombros, torso, brazos)
- Ajustes finos
- Historial de mejoras

**👥 Para:** Data scientists, desarrolladores de IA

---

### 👓 Detección de Accesorios

**📄 [MEJORAS_VISUALIZACION_Y_ACCESORIOS.md](apt-totem-backend/MEJORAS_VISUALIZACION_Y_ACCESORIOS.md)**
- Detección de gorras, gafas, carteras
- Algoritmos de accesorios
- Bounding boxes para accesorios
- Mejoras en visualización
- Debug info

**👥 Para:** Desarrolladores de computer vision, ML engineers

---

### 📊 Estado del Sistema

**📄 [ESTADO_SISTEMA.md](apt-totem-backend/ESTADO_SISTEMA.md)**
- Estado actual del proyecto
- Funcionalidades completadas
- Funcionalidades pendientes
- Issues conocidos

**👥 Para:** Project managers, stakeholders

---

## 🗺️ Mapa de Navegación

```
¿Quién eres?
│
├─ 🤵 Gerente/Vendedor
│  └─→ GUIA_SIMPLE_NO_TECNICOS.md
│
├─ 👨‍💻 Desarrollador nuevo en el proyecto
│  ├─→ README.md (primero)
│  └─→ GUIA_COMPLETA_APLICACION.md (después)
│
├─ 🏗️ Arquitecto/Tech Lead
│  └─→ ARQUITECTURA_TECNICA.md
│
├─ 🤖 ML Engineer / Data Scientist
│  ├─→ MEJORAS_DETECCION_PRENDAS.md
│  └─→ MEJORAS_VISUALIZACION_Y_ACCESORIOS.md
│
├─ 🔧 DevOps / SysAdmin
│  ├─→ SISTEMA_TURNOS_DETECCIONES.md
│  └─→ ARQUITECTURA_TECNICA.md (sección Deployment)
│
└─ 🧪 QA / Tester
   └─→ VISUALIZACION_CV_CRUDA.md
```

---

## 🔍 Búsqueda por Tema

### Instalación y Setup
- **README.md** - Instalación paso a paso
- **GUIA_COMPLETA_APLICACION.md** - Sección "Cómo Iniciar"

### Uso del Sistema
- **GUIA_SIMPLE_NO_TECNICOS.md** - Guía de uso diario
- **README.md** - Uso rápido

### Arquitectura y Diseño
- **ARQUITECTURA_TECNICA.md** - Diagramas y flujos
- **GUIA_COMPLETA_APLICACION.md** - Arquitectura del Sistema

### Detección de IA
- **MEJORAS_DETECCION_PRENDAS.md** - Algoritmos de ropa
- **MEJORAS_VISUALIZACION_Y_ACCESORIOS.md** - Algoritmos de accesorios
- **GUIA_COMPLETA_APLICACION.md** - Sección "Motor de IA"

### Base de Datos
- **ARQUITECTURA_TECNICA.md** - Modelos de datos
- **SISTEMA_TURNOS_DETECCIONES.md** - Tablas de turnos

### API y WebSockets
- **ARQUITECTURA_TECNICA.md** - Flujo de datos
- **README.md** - API Endpoints
- **VISUALIZACION_CV_CRUDA.md** - WebSocket streaming

### Configuración
- **GUIA_COMPLETA_APLICACION.md** - Sección "Configuración y Velocidad"
- **README.md** - Configuración Avanzada

### Troubleshooting
- **README.md** - Troubleshooting común
- **GUIA_SIMPLE_NO_TECNICOS.md** - Problemas y soluciones
- **GUIA_COMPLETA_APLICACION.md** - Errores y fixes

### Testing
- **ARQUITECTURA_TECNICA.md** - Testing Strategy
- **README.md** - Testing section

### Deployment
- **ARQUITECTURA_TECNICA.md** - Deployment Checklist
- **README.md** - Deployment section

---

## 📖 Orden de Lectura Recomendado

### Para Principiantes
1. **README.md** - Entender qué es el proyecto
2. **GUIA_SIMPLE_NO_TECNICOS.md** - Ver cómo se usa
3. **GUIA_COMPLETA_APLICACION.md** - Profundizar técnicamente

### Para Desarrolladores Nuevos
1. **README.md** - Overview
2. **GUIA_COMPLETA_APLICACION.md** - Estructura completa
3. **ARQUITECTURA_TECNICA.md** - Detalles técnicos
4. Documentación especializada según área de trabajo

### Para Mantenimiento
1. **ESTADO_SISTEMA.md** - Ver estado actual
2. **GUIA_COMPLETA_APLICACION.md** - Referencia de componentes
3. Documentación específica del área a modificar

---

## 📊 Tabla Comparativa

| Documento | Nivel Técnico | Longitud | Audiencia Principal | Cuándo Leer |
|-----------|---------------|----------|---------------------|-------------|
| **README.md** | Medio | Corto | Todos | Primero |
| **GUIA_SIMPLE_NO_TECNICOS.md** | Bajo | Medio | No técnicos | Para usar el sistema |
| **GUIA_COMPLETA_APLICACION.md** | Alto | Largo | Desarrolladores | Para desarrollar |
| **ARQUITECTURA_TECNICA.md** | Muy Alto | Largo | Arquitectos | Para diseñar/optimizar |
| **SISTEMA_TURNOS...** | Alto | Medio | Backend devs | Trabajar con turnos |
| **VISUALIZACION_CV...** | Alto | Medio | Frontend/CV devs | Trabajar con UI |
| **MEJORAS_DETECCION...** | Muy Alto | Medio | ML engineers | Mejorar detección |
| **MEJORAS_VISUALIZACION...** | Alto | Medio | CV engineers | Mejorar accesorios |

---

## 🎓 Glosario de Iconos

| Icono | Significado |
|-------|-------------|
| ✅ | Característica o información incluida |
| 📄 | Documento |
| 👥 | Audiencia objetivo |
| 🎯 | Objetivo o propósito |
| 🔍 | Búsqueda o referencia |
| 🏗️ | Arquitectura |
| 🤖 | Inteligencia Artificial |
| 🎥 | Visualización |
| 📊 | Datos y analytics |
| 🔧 | Configuración |
| 🐛 | Troubleshooting |
| 🚀 | Deployment |
| 🧪 | Testing |

---

## 📝 Actualizaciones de Documentación

### Última actualización: 2025-10-20

**Documentos añadidos:**
- ✅ GUIA_COMPLETA_APLICACION.md
- ✅ GUIA_SIMPLE_NO_TECNICOS.md
- ✅ ARQUITECTURA_TECNICA.md
- ✅ README.md (renovado)
- ✅ INDICE_DOCUMENTACION.md (este documento)

**Documentos existentes:**
- SISTEMA_TURNOS_DETECCIONES.md
- VISUALIZACION_CV_CRUDA.md
- MEJORAS_DETECCION_PRENDAS.md
- MEJORAS_VISUALIZACION_Y_ACCESORIOS.md

---

## 🔗 Links Rápidos

### Inicio Rápido
- [Instalación](README.md#-instalación)
- [Uso Rápido](README.md#-uso-rápido)
- [Primeros Pasos](GUIA_SIMPLE_NO_TECNICOS.md#-cómo-usar---guía-rápida-para-vendedores)

### Desarrollo
- [Arquitectura](ARQUITECTURA_TECNICA.md#-diagrama-de-arquitectura-general)
- [Flujo de Datos](ARQUITECTURA_TECNICA.md#-flujo-de-datos-detallado)
- [API Endpoints](README.md#-api-endpoints)

### Configuración
- [Velocidad de Detección](GUIA_COMPLETA_APLICACION.md#-configuración-y-velocidad)
- [Umbrales de IA](GUIA_COMPLETA_APLICACION.md#-umbrales-de-detección)
- [Horarios de Turnos](GUIA_COMPLETA_APLICACION.md#-sistema-de-turnos-y-analytics)

### Ayuda
- [Troubleshooting Técnico](README.md#-troubleshooting)
- [Problemas Comunes No Técnicos](GUIA_SIMPLE_NO_TECNICOS.md#-problemas-comunes-y-soluciones)
- [Solución de Errores](GUIA_COMPLETA_APLICACION.md#-solución-de-problemas-comunes)

---

## 💡 Tips de Navegación

### 🔍 Buscar en Documentación

**En VS Code / Cursor:**
```
Cmd/Ctrl + Shift + F
Buscar en: apt-totem/**/*.md
```

**En Terminal:**
```bash
# Buscar texto en todos los .md
grep -r "término_buscado" *.md

# Buscar en carpeta backend
grep -r "término_buscado" apt-totem-backend/*.md
```

### 📑 Lectura Recomendada por Rol

**Product Owner / Manager:**
```
README.md → GUIA_SIMPLE_NO_TECNICOS.md → ESTADO_SISTEMA.md
```

**Full Stack Developer:**
```
README.md → GUIA_COMPLETA_APLICACION.md → ARQUITECTURA_TECNICA.md → Docs especializados
```

**Frontend Developer:**
```
README.md → GUIA_COMPLETA_APLICACION.md (FRONTEND) → VISUALIZACION_CV_CRUDA.md
```

**Backend Developer:**
```
README.md → GUIA_COMPLETA_APLICACION.md (BACKEND) → ARQUITECTURA_TECNICA.md → SISTEMA_TURNOS...
```

**ML Engineer:**
```
README.md → ARQUITECTURA_TECNICA.md → MEJORAS_DETECCION_PRENDAS.md → MEJORAS_VISUALIZACION...
```

**DevOps:**
```
README.md → ARQUITECTURA_TECNICA.md (Deployment) → SISTEMA_TURNOS... (Cron Jobs)
```

---

## ✉️ Contribuir a la Documentación

Si encuentras errores o mejoras:

1. Identifica el documento correcto
2. Edita el archivo .md
3. Mantén el formato consistente
4. Actualiza el índice si es necesario
5. Commit con mensaje descriptivo

---

**Última actualización:** 2025-10-20  
**Versión del índice:** 1.0.0  
**Documentos totales:** 9

---

<div align="center">

📚 **¡Feliz lectura y desarrollo!** 🚀

[⬆ Volver arriba](#-índice-de-documentación---neototem-ai)

</div>


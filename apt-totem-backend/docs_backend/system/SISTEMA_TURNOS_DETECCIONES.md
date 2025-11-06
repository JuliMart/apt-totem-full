# 🕐 Sistema de Turnos y Almacenamiento de Detecciones

## 📋 Descripción

Sistema automático que almacena y consolida todas las detecciones de la IA en tiempo real, organizadas por turnos de trabajo. Genera resúmenes estadísticos y proporciona insights sobre el flujo de clientes.

## 🎯 Características Principales

### 1. **Almacenamiento en Tiempo Real**
- Cada detección de la cámara se guarda automáticamente en la base de datos
- Buffer temporal de detecciones (`deteccion_buffer`)
- Vinculado al turno actual de trabajo

### 2. **Gestión de Turnos**
- **Turnos automáticos**:
  - 🌅 **Matutino**: 6:00 AM - 2:00 PM
  - 🌞 **Vespertino**: 2:00 PM - 10:00 PM
  - 🌙 **Nocturno**: 10:00 PM - 6:00 AM

- **Cambios automáticos** a las horas programadas
- **Creación manual** de turnos mediante API

### 3. **Resúmenes Automáticos**
- ⏰ Generación cada hora del turno activo
- 📊 Consolidación al cerrar el turno
- 📈 Estadísticas completas por turno

### 4. **Analytics y Reportes**
- Distribución demográfica (rangos de edad)
- Preferencias de estilo de ropa
- Colores más detectados
- Prendas y accesorios más vistos
- Perfil de cliente predominante
- Recomendaciones de inventario

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias
```bash
cd apt-totem-backend
pip install -r requirements.txt
```

### 2. Crear Tablas en la Base de Datos
```bash
python3 migrate_shifts.py
```

Este script:
- Crea las tablas: `turno`, `deteccion_buffer`, `resumen_turno`
- Crea el turno inicial basado en la hora actual

### 3. Iniciar el Backend
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

El sistema de cron jobs se inicia automáticamente con la aplicación.

## 📡 Endpoints Disponibles

### Gestión de Turnos

#### `GET /shifts/current`
Obtiene el turno activo actual
```json
{
  "id_turno": 1,
  "nombre": "matutino",
  "fecha": "2024-10-18",
  "hora_inicio": "2024-10-18T06:00:00",
  "estado": "activo",
  "total_detecciones": 45,
  "total_clientes": 32
}
```

#### `POST /shifts/create`
Crea un nuevo turno manualmente
```bash
POST /shifts/create?nombre_turno=matutino
```

#### `POST /shifts/{id_turno}/close`
Cierra un turno y genera su resumen final
```bash
POST /shifts/1/close
```

#### `GET /shifts/{id_turno}/stats`
Obtiene estadísticas completas de un turno
```json
{
  "turno": {
    "id": 1,
    "nombre": "matutino",
    "total_detecciones": 45,
    "total_clientes": 32
  },
  "resumen": {
    "personas_detectadas": 32,
    "prendas_detectadas": 40,
    "accesorios_detectados": 15,
    "confianza_promedio": 0.87,
    "distribucion_edad": {
      "18-25": 12,
      "26-35": 15,
      "36-45": 5
    },
    "colores_predominantes": {
      "azul": 18,
      "negro": 12,
      "blanco": 8
    }
  }
}
```

#### `GET /shifts/{id_turno}/summary`
Obtiene el resumen consolidado de un turno
```json
{
  "estadisticas": {
    "total_detecciones": 45,
    "total_personas": 32,
    "confianza_promedio": 0.87
  },
  "demografía": {
    "distribucion_edad": {"18-25": 12, "26-35": 15}
  },
  "preferencias": {
    "estilos": {"casual": 20, "formal": 12},
    "colores": {"azul": 18, "negro": 12},
    "prendas": {"camiseta": 15, "chaqueta": 10}
  },
  "insights": {
    "perfil_predominante": {
      "edad_predominante": "26-35",
      "estilo_predominante": "casual",
      "color_predominante": "azul"
    },
    "recomendaciones_inventario": {
      "prendas_prioritarias": [
        {"prenda": "camiseta", "demanda": 15}
      ],
      "acciones_sugeridas": [
        "Aumentar stock de camiseta para público 26-35"
      ]
    }
  }
}
```

#### `GET /shifts/list`
Lista todos los turnos con paginación
```bash
GET /shifts/list?limit=10&offset=0&estado=cerrado
```

#### `GET /shifts/{id_turno}/detections`
Obtiene detecciones individuales de un turno
```json
{
  "total": 45,
  "detecciones": [
    {
      "id": 123,
      "fecha_hora": "2024-10-18T08:30:15",
      "persona_detectada": true,
      "rango_edad": "26-35",
      "estilo": "casual",
      "color_principal": "azul",
      "prenda": "camiseta",
      "confianza": 0.89,
      "motor": "real_detection_mediapipe",
      "fuente": "real"
    }
  ]
}
```

### Analytics

#### `GET /shifts/analytics/today`
Obtiene analytics consolidados del día actual
```json
{
  "fecha": "2024-10-18",
  "total_turnos": 2,
  "total_detecciones": 87,
  "total_clientes": 65,
  "colores_del_dia": {
    "azul": 35,
    "negro": 25,
    "blanco": 15
  },
  "prendas_del_dia": {
    "camiseta": 28,
    "chaqueta": 20
  },
  "demografia_del_dia": {
    "18-25": 20,
    "26-35": 30,
    "36-45": 15
  }
}
```

#### `POST /shifts/{id_turno}/regenerate-summary`
Regenera el resumen de un turno manualmente

## 🤖 Tareas Automáticas (Cron Jobs)

El sistema ejecuta automáticamente las siguientes tareas:

| Tarea | Frecuencia | Descripción |
|-------|------------|-------------|
| Resumen cada hora | Cada 60 min | Genera resumen del turno activo |
| Cambio turno matutino | 6:00 AM | Cierra nocturno, abre matutino |
| Cambio turno vespertino | 2:00 PM | Cierra matutino, abre vespertino |
| Cambio turno nocturno | 10:00 PM | Cierra vespertino, abre nocturno |
| Limpieza | 3:00 AM | Elimina detecciones procesadas >30 días |

## 📊 Modelo de Datos

### Turno
```python
- id_turno: int (PK)
- fecha: datetime
- hora_inicio: datetime
- hora_fin: datetime
- nombre_turno: str  # matutino, vespertino, nocturno
- estado: str  # activo, cerrado
- total_clientes_detectados: int
- total_detecciones: int
```

### DeteccionBuffer
```python
- id_buffer: int (PK)
- id_turno: int (FK)
- fecha_hora: datetime
- persona_detectada: bool
- rango_edad: str
- estilo_ropa: str
- color_principal: str
- color_secundario: str
- prenda_detectada: str
- accesorio_cabeza: str
- confianza_deteccion: float
- motor_deteccion: str
- fuente_camara: str
- procesado: bool
```

### ResumenTurno
```python
- id_resumen: int (PK)
- id_turno: int (FK)
- fecha_generacion: datetime
- total_detecciones: int
- total_personas_detectadas: int
- confianza_promedio: float
- distribucion_edad: JSON
- estilos_detectados: JSON
- colores_predominantes: JSON
- prendas_mas_vistas: JSON
- accesorios_mas_vistos: JSON
- perfil_cliente_predominante: JSON
- recomendaciones_inventario: JSON
```

## 🔄 Flujo de Trabajo

### 1. Detección en Tiempo Real
```
Usuario frente a cámara
    ↓
IA analiza imagen (MediaPipe)
    ↓
Análisis enviado por WebSocket
    ↓
Backend almacena en DeteccionBuffer
    ↓
Vincula al turno activo
```

### 2. Generación de Resúmenes
```
Cada hora (cron job)
    ↓
Procesa detecciones no procesadas
    ↓
Calcula estadísticas y analytics
    ↓
Guarda en ResumenTurno
    ↓
Marca detecciones como procesadas
```

### 3. Cambio de Turno
```
Hora programada (6am, 2pm, 10pm)
    ↓
Cron job ejecuta cambio
    ↓
Cierra turno anterior (genera resumen final)
    ↓
Crea nuevo turno
    ↓
Sistema continúa almacenando en nuevo turno
```

## 📈 Casos de Uso

### Para Gerentes de Tienda
- Consultar estadísticas del turno actual
- Ver qué productos/colores buscan más los clientes
- Obtener recomendaciones de inventario
- Analizar flujo de clientes por hora

### Para Marketing
- Entender perfil demográfico de clientes
- Identificar preferencias de estilo por turno
- Detectar tendencias de color y prendas
- Planificar campañas basadas en datos reales

### Para Operaciones
- Monitorear afluencia de clientes
- Optimizar horarios de personal
- Identificar horas pico
- Analizar efectividad de displays

## 🛠️ Comandos Útiles

### Ver turno actual
```bash
curl http://localhost:8001/shifts/current
```

### Crear turno manualmente
```bash
curl -X POST "http://localhost:8001/shifts/create?nombre_turno=vespertino"
```

### Obtener estadísticas del día
```bash
curl http://localhost:8001/shifts/analytics/today
```

### Cerrar turno manualmente
```bash
curl -X POST http://localhost:8001/shifts/1/close
```

### Regenerar resumen
```bash
curl -X POST http://localhost:8001/shifts/1/regenerate-summary
```

## 🔍 Monitoreo

### Logs del Sistema
Los cron jobs generan logs en tiempo real:
```
🕐 Iniciando sistema de tareas programadas...
✅ Sistema de tareas programadas activo
📊 Generando resumen horario...
✅ Resumen generado para turno 1
  - Total detecciones: 45
  - Personas detectadas: 32
```

### Verificar Estado
Consultar el turno actual para verificar que el sistema está funcionando:
```python
GET /shifts/current
```

## 🐛 Troubleshooting

### No hay turno activo
**Problema**: GET /shifts/current devuelve 404

**Solución**:
```bash
python3 migrate_shifts.py
```
o crear turno manualmente:
```bash
curl -X POST "http://localhost:8001/shifts/create?nombre_turno=matutino"
```

### Cron jobs no se ejecutan
**Problema**: Los turnos no cambian automáticamente

**Verificar**:
1. El backend está corriendo
2. Los logs muestran "✅ Sistema de cron jobs iniciado"
3. No hay errores en los logs

### Detecciones no se almacenan
**Problema**: Las detecciones no aparecen en la BD

**Verificar**:
1. Hay un turno activo
2. El WebSocket está conectado
3. La cámara está enviando datos
4. Revisar logs de errores

## 📝 Notas Importantes

1. **Persistencia**: Las detecciones se guardan permanentemente en la BD
2. **Rendimiento**: El buffer permite procesar miles de detecciones sin afectar performance
3. **Limpieza**: Las detecciones procesadas se eliminan automáticamente después de 30 días
4. **Resúmenes**: Se mantienen indefinidamente para análisis histórico
5. **Turnos**: Se crean automáticamente si no existe uno activo

## 🚀 Próximas Mejoras

- [ ] Dashboard visual para analytics
- [ ] Exportación de reportes en PDF
- [ ] Alertas cuando cambia el perfil de clientes
- [ ] Integración con sistema de inventario
- [ ] Predicción de demanda basada en históricos
- [ ] Comparación entre turnos y días

## 📞 Soporte

Para más información sobre el sistema de turnos y detecciones, consultar la documentación del API en:
```
http://localhost:8001/docs
```


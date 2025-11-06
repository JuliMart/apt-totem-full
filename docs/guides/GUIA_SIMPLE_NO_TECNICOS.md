# 🛍️ NeoTotem AI - Guía Simple

> **Para gerentes, vendedores y personas no técnicas**

---

## 🤔 ¿Qué es NeoTotem AI?

Es un **totem inteligente** (como un iPad grande de pie) que:

1. **Te ve** 👀 con su cámara
2. **Entiende** 🧠 qué ropa llevas puesta
3. **Te recomienda** 💡 productos de la tienda
4. **Te escucha** 🎤 si le hablas
5. **Aprende** 📊 qué prefieren los clientes

---

## 🎬 ¿Cómo lo usa un cliente?

### Paso 1: Cliente se acerca al totem
```
Cliente entra a la tienda →  Ve el totem →  Se acerca
```

### Paso 2: El totem lo detecta automáticamente
```
👤 Detectado: Persona
👕 Lleva puesto: Camiseta negra
🧢 Tiene: Gorra y gafas
```

### Paso 3: Totem muestra recomendaciones
```
💬 "¡Hola! Veo que te gusta el estilo casual.
    Tenemos estas opciones que podrían interesarte..."

📦 Producto 1: Camiseta similar
📦 Producto 2: Pantalón que combina
📦 Producto 3: Accesorios
```

### Paso 4 (Opcional): Cliente puede hablar
```
Cliente: "Busco algo más formal"
Totem: "Perfecto, te muestro opciones formales..."
```

---

## 🏪 Beneficios para la Tienda

### 📈 Conoce a tus clientes
- **¿Qué colores prefieren?** → Negro 45%, Blanco 30%, Azul 15%
- **¿Qué prendas buscan?** → Camisetas 60%, Chaquetas 25%, Sudaderas 15%
- **¿Qué edades vienen?** → 18-25: 40%, 26-35: 35%, 36+: 25%

### ⏰ Reportes por turno
Cada 8 horas (mañana, tarde, noche) genera un reporte:

```
📊 REPORTE - TURNO MAÑANA (06:00 - 14:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 Clientes detectados: 47
👕 Prenda más vista: Camiseta (28 clientes)
🎨 Color más popular: Negro (21 clientes)
👓 Accesorios comunes: Gafas de sol (15 clientes)
📅 Fecha: 20 Oct 2025
```

### 💰 Aumenta ventas
- Cliente ve **recomendaciones personalizadas**
- **Más rápido** que buscar por toda la tienda
- **Experiencia moderna** que atrae clientes

---

## 🖥️ Componentes del Sistema

Imagina el sistema como un restaurante:

### 🍽️ **Frontend (La Mesa del Cliente)**
- Es lo que **ve y usa el cliente**
- Pantalla táctil grande
- Cámara arriba
- Micrófono integrado
- Altavoces para respuestas de voz

**Ejemplo:**
```
┌─────────────────────────────┐
│   🤖 NeoTotem AI            │
│                             │
│   👤 [CARA DEL CLIENTE]     │
│                             │
│   Detectamos:               │
│   👕 Camiseta casual        │
│   🎨 Color: Negro           │
│   🧢 Gorra deportiva        │
│                             │
│   ¿Te mostramos opciones    │
│   similares?                │
│                             │
│   [SÍ]    [NO]             │
│                             │
│   🎤 O dime qué buscas      │
└─────────────────────────────┘
```

### 🧑‍🍳 **Backend (La Cocina)**
- Es el **cerebro invisible**
- Analiza las imágenes
- Decide qué productos recomendar
- Guarda estadísticas
- Nadie lo ve, pero hace todo el trabajo

**Hace:**
- 🔍 Detecta qué ropa llevas
- 🎨 Identifica colores
- 👓 Ve accesorios (gorras, gafas, carteras)
- 📊 Guarda datos para reportes
- 💡 Busca productos similares en inventario

### 📺 **Visualización (La Ventana de la Cocina)**
- Pantalla especial para el **gerente/técnico**
- Muestra en tiempo real qué está detectando
- Útil para verificar que funciona bien

**Ejemplo:**
```
┌─────────────────────────────┐
│ 🔍 MONITOREO EN TIEMPO REAL │
│                             │
│ [Imagen con recuadros]      │
│  🟢 Verde = Cara            │
│  🟠 Naranja = Ropa          │
│  🟣 Morado = Accesorios     │
│                             │
│ Última detección:           │
│ • Camiseta negra ✅         │
│ • Gorra ✅                  │
│ • Gafas ✅                  │
│ • Confianza: 92%            │
└─────────────────────────────┘
```

---

## 🚦 Estados del Sistema

### 🟢 **Verde - Todo OK**
```
✅ Cámara funcionando
✅ Detectando clientes
✅ Guardando datos
```

### 🟡 **Amarillo - Advertencia**
```
⚠️ Conexión lenta
⚠️ Poca luz (cámara no ve bien)
⚠️ Cliente muy lejos
```

### 🔴 **Rojo - Error**
```
❌ Sin conexión a internet
❌ Cámara desconectada
❌ Sistema caído
```

---

## 📊 Estadísticas que Genera

### Cada Turno (8 horas)
- Total de clientes detectados
- Prendas más vistas
- Colores más populares
- Rango de edades
- Hora pico de tráfico

### Cada Semana
- Comparación entre días
- Tendencias de moda
- Productos más buscados

### Cada Mes
- Evolución de preferencias
- Efectividad del totem
- ROI (retorno de inversión)

**Ejemplo de reporte semanal:**
```
📊 REPORTE SEMANAL: 14-20 Octubre 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 TRÁFICO TOTAL
   • Lunes:     67 clientes  ⬆️ +12%
   • Martes:    54 clientes  ⬇️ -8%
   • Miércoles: 71 clientes  ⬆️ +20% 🔥
   • Jueves:    48 clientes  ⬇️ -15%
   • Viernes:   89 clientes  ⬆️ +35% 🔥🔥
   • Sábado:   134 clientes  ⬆️ +78% 🔥🔥🔥
   • Domingo:   98 clientes  ⬆️ +45%

👕 PRENDAS MÁS VISTAS
   1. Camisetas (42%)
   2. Chaquetas (28%)
   3. Sudaderas (18%)
   4. Camisas (12%)

🎨 COLORES POPULARES
   1. ⚫ Negro (38%)
   2. ⚪ Blanco (22%)
   3. 🔵 Azul (18%)
   4. ⚫ Gris (15%)
   5. 🔴 Rojo (7%)

⏰ HORARIOS PICO
   • 12:00-14:00 (hora de almuerzo) 🔥
   • 18:00-20:00 (salida del trabajo) 🔥
   • 10:00-11:00 (fin de semana) 🔥

💡 RECOMENDACIÓN
   → Aumentar stock de camisetas negras
   → Promocionar chaquetas en horario 12-14h
```

---

## 🎯 Preguntas Frecuentes

### ❓ ¿Graba videos de los clientes?
**NO.** Solo captura fotos cada 0.3 segundos para analizar, pero **NO las guarda**. Solo guarda los resultados (ej: "camiseta negra detectada").

### ❓ ¿Necesita internet?
**SÍ**, necesita conexión WiFi para:
- Procesar las imágenes
- Guardar estadísticas
- Sincronizar con sistema de inventario

### ❓ ¿Funciona de noche / con poca luz?
Funciona mejor con **buena iluminación**. Si hay poca luz, puede detectar menos detalles.

### ❓ ¿Puede detectar varias personas a la vez?
Actualmente detecta **1 persona a la vez** (la más cercana al totem).

### ❓ ¿Qué tan rápido funciona?
**Casi instantáneo** - detecta en menos de 1 segundo desde que el cliente se acerca.

### ❓ ¿Se puede personalizar?
**SÍ**, se puede ajustar:
- Productos que recomienda
- Velocidad de análisis
- Sensibilidad de detección
- Idioma de respuestas

### ❓ ¿Necesita mantenimiento?
**Mínimo:**
- Limpiar cámara 1 vez por semana
- Verificar conexión WiFi
- Revisar reportes en la app de administración

---

## 🛠️ Cómo Usar - Guía Rápida para Vendedores

### Encender el Sistema

#### Paso 1: Encender el Backend (Cerebro)
```
1. Abrir computadora/servidor
2. Abrir Terminal/CMD
3. Escribir: cd apt-totem-backend
4. Escribir: uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
5. Esperar mensaje: "Application startup complete"
```

#### Paso 2: Encender el Frontend (Pantalla Cliente)
```
1. Abrir otra Terminal/CMD
2. Escribir: cd frontend
3. Escribir: flutter run -d chrome --web-port=8080
4. Esperar que abra navegador automáticamente
```

#### Paso 3: Verificar que funciona
```
1. Pararse frente a la cámara
2. Presionar botón "Activar Cámara"
3. Ver que detecta tu ropa en pantalla
4. ✅ Todo listo!
```

### Ver Estadísticas (Solo Gerente)

```
1. Abrir navegador
2. Ir a: http://localhost:8001/visualization
3. Ver detecciones en tiempo real
4. Para reportes: http://localhost:8001/shifts/analytics
```

---

## 📱 Pantallas Principales

### Pantalla 1: Bienvenida
```
┌─────────────────────────────┐
│                             │
│       🤖 NeoTotem AI        │
│                             │
│   Bienvenido a [TIENDA]    │
│                             │
│   Acércate para recibir     │
│   recomendaciones           │
│   personalizadas            │
│                             │
│         👋 ¡Hola!          │
│                             │
└─────────────────────────────┘
```

### Pantalla 2: Detectando
```
┌─────────────────────────────┐
│   🎥 Analizando...          │
│                             │
│   [CARA DEL CLIENTE]        │
│                             │
│   ✨ Detectado:             │
│   👕 Camiseta deportiva     │
│   🎨 Color: Azul            │
│   🧢 Gorra                  │
│                             │
│   ⏳ Buscando opciones...   │
└─────────────────────────────┘
```

### Pantalla 3: Recomendaciones
```
┌─────────────────────────────┐
│   💡 Tenemos esto para ti:  │
│                             │
│   📦 Camiseta Deportiva     │
│   [Imagen] $29.99           │
│   ⭐⭐⭐⭐⭐               │
│                             │
│   📦 Shorts Running         │
│   [Imagen] $24.99           │
│   ⭐⭐⭐⭐                 │
│                             │
│   [VER MÁS] [BUSCAR OTRA]  │
│   🎤 O dime qué necesitas   │
└─────────────────────────────┘
```

---

## 🎓 Glosario de Términos

| Término | Qué significa | Ejemplo |
|---------|---------------|---------|
| **Frontend** | La pantalla que ve el cliente | Como la TV en tu casa |
| **Backend** | El cerebro que procesa todo | Como el CPU dentro de la computadora |
| **WebSocket** | Conexión en tiempo real | Como una llamada telefónica (siempre conectado) |
| **IA / AI** | Inteligencia Artificial | Programa que "piensa" y decide |
| **MediaPipe** | Tecnología de Google para ver personas | Detecta dónde están tus ojos, brazos, etc. |
| **Bounding Box** | Recuadro de colores en la imagen | Como marcar con resaltador |
| **FPS** | Frames por segundo (velocidad) | Cuántas fotos toma por segundo |
| **Turno** | Período de trabajo (8 horas) | Mañana, Tarde, Noche |
| **Analytics** | Estadísticas y reportes | Gráficas de ventas, tendencias |

---

## ✅ Checklist Diario

### Al Abrir la Tienda
- [ ] Encender computadora/servidor
- [ ] Iniciar backend (cerebro)
- [ ] Iniciar frontend (pantalla)
- [ ] Verificar que cámara funciona
- [ ] Probar con tu propia ropa
- [ ] Limpiar pantalla táctil

### Durante el Día
- [ ] Verificar que sigue funcionando cada 2 horas
- [ ] Si cliente reporta problema, reiniciar sistema
- [ ] Limpiar cámara si está sucia

### Al Cerrar la Tienda
- [ ] Revisar estadísticas del día
- [ ] Cerrar navegador (frontend)
- [ ] Detener backend (Ctrl+C en Terminal)
- [ ] Apagar computadora

---

## 🆘 Problemas Comunes y Soluciones

### "No detecta mi ropa"
✅ **Solución:**
1. Acércate más a la cámara
2. Verifica que hay buena luz
3. Ponte de frente (no de lado)

### "Detecta mal (dice chaqueta pero llevo camiseta)"
✅ **Solución:**
1. Esperar 2-3 segundos (se autocorrige)
2. Moverte un poco
3. Si persiste, avisar a técnico

### "Pantalla congelada"
✅ **Solución:**
1. Recargar página (F5)
2. Si no funciona, reiniciar navegador
3. Si persiste, reiniciar sistema completo

### "No hay sonido"
✅ **Solución:**
1. Verificar volumen del dispositivo
2. Verificar altavoces conectados
3. Probar con auriculares

---

## 📞 Contacto Soporte Técnico

**Para emergencias o dudas técnicas:**
- 📧 Email: soporte@neototem.com
- 📱 WhatsApp: +XX XXX XXX XXXX
- 🌐 Web: www.neototem.com/soporte

**Horario:** Lunes a Viernes, 8:00 - 20:00

---

**¡Listo! Con esta guía cualquier persona puede entender y usar NeoTotem AI** 🚀

*Versión: 1.0 - Octubre 2025*


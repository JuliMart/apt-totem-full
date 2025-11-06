# 📊 Scripts SQL - NeoTotem AI

> Guía rápida de qué archivo SQL usar según tu caso

---

## 🎯 ¿Cuál archivo usar?

### Para Configuración Inicial (Primera vez)

```
1️⃣ schema_mysql_completo.sql    ← PRIMERO: Crea las tablas
2️⃣ populate_mysql_complete.sql  ← DESPUÉS: Llena con datos
```

---

## 📁 Descripción de Archivos

### 1. `schema_mysql_completo.sql` (214 líneas)

**¿Qué hace?**
- ✅ Crea TODAS las tablas de la base de datos
- ✅ Define estructura: columnas, tipos, relaciones
- ✅ Configura claves primarias y foráneas

**¿Cuándo usarlo?**
- Primera vez que configuras el proyecto
- Cuando quieres recrear la BD desde cero
- Cuando cambias de servidor

**Tablas que crea:**
```
- tienda
- dispositivo
- producto
- producto_variante
- inventario
- sesion
- deteccion
- consulta_voz
- recomendacion_sesion
- recomendacion_item
- interaccion_usuario
- metricas_sesion
- evento
```

**Cómo usarlo:**
```bash
mysql -u root -p < data/sql/schema_mysql_completo.sql
```

---

### 2. `populate_mysql_complete.sql` (266 líneas)

**¿Qué hace?**
- ✅ Llena las tablas con datos de ejemplo COMPLETOS
- ✅ Incluye productos reales (Nike, Adidas, Puma, etc.)
- ✅ Incluye variantes (tallas, colores)
- ✅ Incluye inventario
- ✅ Incluye sesiones de ejemplo
- ✅ Incluye detecciones simuladas

**¿Cuándo usarlo?**
- Después de crear las tablas con `schema_mysql_completo.sql`
- Para tener datos de prueba completos
- Para desarrollo y testing
- **⭐ ESTE ES EL PRINCIPAL PARA POBLAR**

**Qué incluye:**
```
- 30+ productos reales de marcas conocidas
- Múltiples variantes por producto (tallas, colores)
- Stock de inventario
- Sesiones de ejemplo
- Detecciones simuladas
- Recomendaciones de prueba
```

**Cómo usarlo:**
```bash
mysql -u root -p < data/sql/populate_mysql_complete.sql
```

---

### 3. `populate_mysql_simple.sql` (231 líneas)

**¿Qué hace?**
- ✅ Llena las tablas con datos BÁSICOS
- ✅ Menos productos que el completo
- ✅ Datos mínimos para testing rápido

**¿Cuándo usarlo?**
- Para testing rápido
- Cuando no necesitas muchos datos
- Alternativa más ligera al complete

**Diferencia con `populate_mysql_complete.sql`:**
- ❌ Menos productos
- ❌ Menos variantes
- ❌ Menos datos de ejemplo
- ✅ Más rápido de ejecutar

**Cómo usarlo:**
```bash
mysql -u root -p < data/sql/populate_mysql_simple.sql
```

---

### 4. `update_placeholder_images.sql` (27 líneas)

**¿Qué hace?**
- ✅ Actualiza URLs de imágenes placeholder
- ✅ Corrige URLs rotas
- ✅ Pone imágenes genéricas temporales

**¿Cuándo usarlo?**
- Cuando las imágenes de productos no cargan
- Para poner placeholders mientras consigues imágenes reales
- Para fixing rápido de URLs

**Cómo usarlo:**
```bash
mysql -u root -p neototem < data/sql/update_placeholder_images.sql
```

---

### 5. `update_product_images.sql` (31 líneas)

**¿Qué hace?**
- ✅ Actualiza URLs de imágenes de productos específicos
- ✅ Cambia imágenes placeholder por reales
- ✅ Corrige URLs de productos existentes

**¿Cuándo usarlo?**
- Cuando tienes imágenes reales y quieres actualizarlas
- Para reemplazar placeholders
- Para corregir URLs rotas de productos específicos

**Cómo usarlo:**
```bash
mysql -u root -p neototem < data/sql/update_product_images.sql
```

---

## 🚀 Orden de Ejecución Recomendado

### Setup Inicial (Primera Vez)

```bash
# Paso 1: Crear base de datos (si no existe)
mysql -u root -p -e "CREATE DATABASE neototem;"

# Paso 2: Crear tablas
mysql -u root -p < data/sql/schema_mysql_completo.sql

# Paso 3: Llenar con datos
mysql -u root -p < data/sql/populate_mysql_complete.sql

# Paso 4 (Opcional): Actualizar imágenes si es necesario
mysql -u root -p neototem < data/sql/update_placeholder_images.sql
```

---

### Resetear Base de Datos

```bash
# Opción 1: Borrar y recrear
mysql -u root -p -e "DROP DATABASE neototem; CREATE DATABASE neototem;"
mysql -u root -p < data/sql/schema_mysql_completo.sql
mysql -u root -p < data/sql/populate_mysql_complete.sql

# Opción 2: Solo vaciar datos
mysql -u root -p neototem -e "SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE producto; TRUNCATE TABLE sesion; SET FOREIGN_KEY_CHECKS=1;"
mysql -u root -p < data/sql/populate_mysql_complete.sql
```

---

### Actualizar Solo Imágenes

```bash
# Opción 1: Placeholders genéricos
mysql -u root -p neototem < data/sql/update_placeholder_images.sql

# Opción 2: Imágenes reales específicas
mysql -u root -p neototem < data/sql/update_product_images.sql
```

---

## 📊 Comparación Rápida

| Archivo | Líneas | Para qué | Cuándo usar |
|---------|--------|----------|-------------|
| **schema_mysql_completo.sql** | 214 | Crear tablas | 🥇 **Primera vez** / Recrear BD |
| **populate_mysql_complete.sql** | 266 | Datos completos | 🥇 **Primera vez** / Desarrollo |
| **populate_mysql_simple.sql** | 231 | Datos básicos | Testing rápido |
| **update_placeholder_images.sql** | 27 | Fix imágenes | Imágenes rotas |
| **update_product_images.sql** | 31 | Actualizar URLs | Cambiar imágenes |

---

## 🎯 Casos de Uso Comunes

### "Es mi primera vez, ¿qué hago?"

```bash
# Estos dos:
1. schema_mysql_completo.sql       ← Crea estructura
2. populate_mysql_complete.sql     ← Llena datos
```

### "Ya tengo las tablas, solo quiero datos frescos"

```bash
# Solo este:
populate_mysql_complete.sql        ← Borra y llena de nuevo
```

### "Las imágenes no cargan"

```bash
# Este:
update_placeholder_images.sql      ← Pone placeholders
```

### "Quiero testing rápido con pocos datos"

```bash
# Estos dos:
1. schema_mysql_completo.sql       ← Crea estructura
2. populate_mysql_simple.sql       ← Datos mínimos
```

---

## 🔍 Verificar Qué Tienes

```bash
# Ver si existen las tablas
mysql -u root -p neototem -e "SHOW TABLES;"

# Ver cuántos productos hay
mysql -u root -p neototem -e "SELECT COUNT(*) FROM producto;"

# Ver productos con imágenes
mysql -u root -p neototem -e "SELECT nombre, url_imagen FROM producto LIMIT 5;"

# Ver estructura de una tabla
mysql -u root -p neototem -e "DESCRIBE producto;"
```

---

## ⚠️ Advertencias

### ❌ NO ejecutes esto sin leer

```bash
# CUIDADO: Borra TODO
DROP DATABASE neototem;
```

### ✅ Haz backup antes

```bash
# Backup antes de cambios grandes
mysqldump -u root -p neototem > backup_$(date +%Y%m%d).sql
```

---

## 📝 Resumen Ejecutivo

| Si quieres... | Usa este archivo |
|---------------|------------------|
| **Empezar desde cero** | `schema_mysql_completo.sql` + `populate_mysql_complete.sql` |
| **Solo crear tablas** | `schema_mysql_completo.sql` |
| **Solo llenar datos** | `populate_mysql_complete.sql` |
| **Datos mínimos** | `populate_mysql_simple.sql` |
| **Fix imágenes** | `update_placeholder_images.sql` |
| **Cambiar imágenes** | `update_product_images.sql` |

---

## 🎓 Para Saber Más

- Ver estructura de tablas: `apt-totem-backend/database/models.py`
- Documentación de BD: `docs/guides/ARQUITECTURA_TECNICA.md`
- Sistema completo: `docs/guides/GUIA_COMPLETA_APLICACION.md`

---

**Última actualización:** 2025-10-20  
**Versión:** 1.0.0

---

**🎯 Recomendación: Usa `schema_mysql_completo.sql` + `populate_mysql_complete.sql` para empezar**


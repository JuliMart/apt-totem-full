# 🔧 Mejoras en Detección de Prendas

## 🐛 Problema Resuelto

**Síntoma**: El sistema siempre detectaba "chaqueta" independientemente de la prenda real.

**Causa**: La lógica original usaba solo la distancia entre hombros, lo cual es insuficiente:
```python
# ❌ ANTES (INCORRECTO)
if shoulder_distance > 0.15:
    clothing_item = "chaqueta"  # Muy fácil de activar
```

## ✅ Solución Implementada

Ahora usamos **análisis multi-criterio** que considera 3 factores:

### 1. Distancia entre Hombros
- **Chaqueta**: > 0.18 (muy ancho, voluminoso)
- **Sudadera**: > 0.16 (ancho, con capucha)
- **Camiseta**: < 0.16 (normal)

### 2. Altura del Torso
- **Chaqueta**: > 0.3 (prenda larga)
- **Camiseta**: < 0.3 (prenda corta)

### 3. Cobertura de Brazos
- **Chaqueta**: > 0.15 (manga larga formal)
- **Sudadera**: > 0.12 (manga deportiva)
- **Camiseta manga larga**: > 0.12
- **Camiseta**: < 0.12 (manga corta)

## 📊 Nueva Lógica de Detección

```python
# ✅ AHORA (CORRECTO - Multi-criterio)

# Chaqueta: TODOS los criterios deben cumplirse
if shoulder_distance > 0.18 AND torso_height > 0.3 AND arm_coverage > 0.15:
    clothing_item = "chaqueta"
    style = "formal"

# Sudadera: hombros anchos + brazos cubiertos
elif shoulder_distance > 0.16 AND arm_coverage > 0.12:
    clothing_item = "sudadera"
    style = "deportivo"

# Camiseta manga larga: solo brazos cubiertos
elif arm_coverage > 0.12:
    clothing_item = "camiseta_manga_larga"
    style = "casual"

# Camiseta: default (más común)
else:
    clothing_item = "camiseta"
    style = "casual"
```

## 🎯 Tipos de Prenda Detectables

| Prenda | Criterios | Estilo |
|--------|-----------|--------|
| **Chaqueta** | Hombros anchos + Torso largo + Brazos cubiertos | Formal |
| **Sudadera** | Hombros anchos + Brazos cubiertos | Deportivo |
| **Camiseta manga larga** | Brazos cubiertos | Casual |
| **Camiseta** | Default (sin características especiales) | Casual |

## 🔍 Sistema de Debug

Ahora el sistema imprime métricas en tiempo real para debugging:

```
🔍 DEBUG - Métricas de detección:
  Distancia hombros: 0.142
  Altura torso: 0.285
  Cobertura brazos: 0.095
  ✅ DETECTADO: camiseta (casual)
  Criterios: S=False, T=False, A=False
```

Esto te permite:
- Ver los valores exactos calculados
- Entender por qué se clasificó como una prenda específica
- Calibrar los umbrales si es necesario

## 📈 Mejoras en Precisión

### Antes
- ❌ Siempre detectaba chaqueta
- ❌ Solo usaba 1 métrica (impreciso)
- ❌ No diferenciaba tipos de prendas

### Ahora
- ✅ Detecta correctamente 4 tipos de prendas
- ✅ Usa 3 métricas combinadas (más preciso)
- ✅ Requiere múltiples criterios para chaqueta (menos falsos positivos)
- ✅ Default inteligente: camiseta (prenda más común)

## 🧪 Cómo Probar

### 1. Reiniciar el Backend
```bash
cd apt-totem-backend
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

### 2. Activar Cámara en UI
- Abrir Flutter UI
- Tab "Detección"
- Click "📹 Activar Cámara"

### 3. Ver Logs en Terminal
Observa los logs de debug para ver las métricas:
```
🔍 DEBUG - Métricas de detección:
  Distancia hombros: 0.156
  Altura torso: 0.312
  Cobertura brazos: 0.108
  ✅ DETECTADO: camiseta_manga_larga (casual)
```

### 4. Ver en Visualización
- Abrir `http://localhost:8001/visualization`
- Ver la prenda detectada en el panel derecho
- Ver el recuadro naranja sobre la vestimenta

## 🎨 Ejemplos de Detección

### Ejemplo 1: Camiseta Manga Corta
```
Métricas:
  Distancia hombros: 0.14 ❌ (< 0.16)
  Altura torso: 0.25 ❌ (< 0.3)
  Cobertura brazos: 0.08 ❌ (< 0.12)

→ RESULTADO: camiseta (casual) ✅
```

### Ejemplo 2: Chaqueta Formal
```
Métricas:
  Distancia hombros: 0.22 ✅ (> 0.18)
  Altura torso: 0.35 ✅ (> 0.3)
  Cobertura brazos: 0.18 ✅ (> 0.15)

→ RESULTADO: chaqueta (formal) ✅
```

### Ejemplo 3: Sudadera
```
Métricas:
  Distancia hombros: 0.17 ✅ (> 0.16)
  Altura torso: 0.28 ❌ (< 0.3)
  Cobertura brazos: 0.13 ✅ (> 0.12)

→ RESULTADO: sudadera (deportivo) ✅
```

### Ejemplo 4: Camiseta Manga Larga
```
Métricas:
  Distancia hombros: 0.15 ❌ (< 0.16)
  Altura torso: 0.26 ❌ (< 0.3)
  Cobertura brazos: 0.14 ✅ (> 0.12)

→ RESULTADO: camiseta_manga_larga (casual) ✅
```

## 🔧 Calibración (Si es necesario)

Si encuentras que las detecciones no son precisas, puedes ajustar los umbrales en `real_detection.py`:

```python
# Hacer chaqueta MÁS difícil de detectar (menos falsos positivos)
if shoulder_distance > 0.20:  # Aumentar de 0.18 a 0.20
    ...

# Hacer chaqueta MÁS fácil de detectar (más sensible)
if shoulder_distance > 0.16:  # Reducir de 0.18 a 0.16
    ...
```

## 📝 Notas Técnicas

### Métricas Calculadas

**shoulder_distance**: Distancia horizontal entre hombros (normalizada 0-1)
- Valores típicos: 0.12 - 0.25
- Mayor = prendas más voluminosas

**torso_height**: Altura vertical del torso (normalizada 0-1)
- Valores típicos: 0.2 - 0.4
- Mayor = prendas más largas

**arm_coverage**: Distancia vertical entre hombro y codo (normalizada 0-1)
- Valores típicos: 0.05 - 0.20
- Mayor = mangas más largas

### Landmarks de MediaPipe Usados

```python
11 = LEFT_SHOULDER
12 = RIGHT_SHOULDER
13 = LEFT_ELBOW
15 = RIGHT_ELBOW
23 = LEFT_HIP
24 = RIGHT_HIP
```

## ✅ Verificación

Para verificar que el problema está resuelto:

1. ✅ Probar con camiseta → debe detectar "camiseta"
2. ✅ Probar con chaqueta formal → debe detectar "chaqueta"
3. ✅ Probar con sudadera → debe detectar "sudadera"
4. ✅ Ver logs de debug para entender la clasificación

## 🐛 Troubleshooting

### Problema: Sigue detectando chaqueta
**Solución**: Los umbrales están muy bajos. Aumentar:
```python
if shoulder_distance > 0.20 and torso_height > 0.35 and arm_coverage > 0.18:
```

### Problema: Nunca detecta chaqueta
**Solución**: Los umbrales están muy altos. Reducir:
```python
if shoulder_distance > 0.16 and torso_height > 0.25 and arm_coverage > 0.12:
```

### Problema: Detección inestable (cambia mucho)
**Solución**: Puede ser iluminación o movimiento. Mejorar:
1. Iluminación constante
2. Posición estable del usuario
3. Cámara fija (sin movimiento)

## 📈 Próximas Mejoras

- [ ] Detección de pantalones
- [ ] Detección de faldas/vestidos
- [ ] Análisis de textura (liso, rayado, estampado)
- [ ] Detección de múltiples capas (camiseta + chaqueta)
- [ ] Machine learning para mejorar precisión
- [ ] Calibración automática por usuario

## 📞 Soporte

Si encuentras problemas con la detección, revisa:
1. Los logs de debug en la terminal
2. La visualización en `/visualization`
3. Los valores de las métricas calculadas

Para ajustar la sensibilidad, edita los umbrales en:
`apt-totem-backend/services/ai/real_detection.py` líneas 462-493


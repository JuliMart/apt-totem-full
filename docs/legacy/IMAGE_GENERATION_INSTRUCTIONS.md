# 🎨 Generación de Imágenes de Productos con IA

## 📊 Resumen
- **9 productos únicos** para generar
- **Una imagen base** por producto
- **Aplicada a todas las tallas** automáticamente

## 🚀 Proceso Completo

### 1. Generar Imágenes
Elige una de estas opciones:

#### Opción A: DALL-E (Recomendado)
```bash
# Instalar dependencias
pip install openai python-dotenv requests

# Configurar API key
echo "OPENAI_API_KEY=tu_api_key_aqui" > .env

# Generar imágenes
python3 generate_with_dalle.py
```

#### Opción B: Midjourney
1. Abre `midjourney_prompts.txt`
2. Copia cada prompt
3. Pégalo en Midjourney
4. Descarga las imágenes
5. Renómbralas según la guía

#### Opción C: Stable Diffusion
1. Abre `stable_diffusion_prompts.txt`
2. Usa con AUTOMATIC1111 o ComfyUI
3. Genera las imágenes
4. Renómbralas según la guía

### 2. Mapear a Variantes
```bash
# Después de generar las imágenes
python3 map_generated_images.py
```

### 3. Verificar Resultado
Las imágenes aparecerán automáticamente en el frontend.

## 📁 Estructura de Archivos

```
generated_images/          # Imágenes generadas (una por producto)
├── nike-air-max-270.jpg
├── adidas-ultraboost-22.jpg
└── ...

product_images/            # Imágenes mapeadas (una por variante)
├── nike/
│   ├── nike-air-max-270-negro-36.jpg
│   ├── nike-air-max-270-negro-38.jpg
│   └── ...
└── adidas/
    ├── adidas-ultraboost-22-azul-36.jpg
    └── ...
```

## 🎯 Ventajas del Sistema

1. **Eficiencia**: Una imagen por producto, no por variante
2. **Consistencia**: Misma imagen para todas las tallas
3. **Calidad**: Imágenes profesionales generadas por IA
4. **Automatización**: Mapeo automático a todas las variantes

## 📋 Lista de Productos

1. **Adidas Adidas Ultraboost 22**
   - Colores: Negro, Blanco, Azul
   - Tallas: 36, 37, 38, 39
   - Archivo: `adidas-adidas-ultraboost-22.jpg`

2. **Adidas Hoodie Adidas Originals**
   - Colores: Negro, Blanco, Azul
   - Tallas: XS, S, M, L
   - Archivo: `adidas-hoodie-adidas-originals.jpg`

3. **Adidas Pantalón Adidas Tiro**
   - Colores: Negro, Blanco, Azul
   - Tallas: XS, S, M, L
   - Archivo: `adidas-pantalón-adidas-tiro.jpg`

4. **Converse Converse Chuck Taylor**
   - Colores: Negro, Blanco, Azul
   - Tallas: 36, 37, 38, 39
   - Archivo: `converse-converse-chuck-taylor.jpg`

5. **Nike Camiseta Nike Dri-FIT**
   - Colores: Negro, Blanco, Azul
   - Tallas: XS, S, M, L
   - Archivo: `nike-camiseta-nike-dri-fit.jpg`

6. **Nike Nike Air Max 270**
   - Colores: Negro, Blanco, Azul
   - Tallas: 36, 37, 38, 39
   - Archivo: `nike-nike-air-max-270.jpg`

7. **Nike Pantalón Nike Tech Fleece**
   - Colores: Negro, Blanco, Azul
   - Tallas: XS, S, M, L
   - Archivo: `nike-pantalón-nike-tech-fleece.jpg`

8. **Puma Puma RS-X**
   - Colores: Negro, Blanco, Azul
   - Tallas: 36, 37, 38, 39
   - Archivo: `puma-puma-rs-x.jpg`

9. **Vans Vans Old Skool**
   - Colores: Negro, Blanco, Azul
   - Tallas: 36, 37, 38, 39
   - Archivo: `vans-vans-old-skool.jpg`


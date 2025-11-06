-- ============================================================================
-- ACTUALIZAR CON PLACEHOLDER IMAGES (MÁS SIMPLE)
-- ============================================================================

USE neototem;

-- Usar placeholder images de diferentes servicios
UPDATE producto_variante SET image_url = CONCAT('https://picsum.photos/400/400?random=', id_variante) WHERE image_url LIKE 'https://example.com%';

-- O usar placeholder específicos por categoría
UPDATE producto_variante pv 
JOIN producto p ON pv.id_producto = p.id_producto
JOIN categoria c ON p.id_categoria = c.id_categoria
SET pv.image_url = CASE 
    WHEN c.nombre = 'Zapatillas Deportivas' THEN CONCAT('https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&crop=center&auto=format&q=80&', pv.id_variante)
    WHEN c.nombre = 'Zapatillas Casual' THEN CONCAT('https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&crop=center&auto=format&q=80&', pv.id_variante)
    WHEN c.nombre = 'Poleras' THEN CONCAT('https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center&auto=format&q=80&', pv.id_variante)
    WHEN c.nombre = 'Chaquetas' THEN CONCAT('https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop&crop=center&auto=format&q=80&', pv.id_variante)
    ELSE CONCAT('https://picsum.photos/400/400?random=', pv.id_variante)
END
WHERE pv.image_url LIKE 'https://example.com%';

-- Verificar actualizaciones
SELECT p.nombre, pv.sku, pv.color, pv.image_url 
FROM producto p 
JOIN producto_variante pv ON p.id_producto = pv.id_producto 
LIMIT 5;

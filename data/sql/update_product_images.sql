-- ============================================================================
-- ACTUALIZAR IMÁGENES DE PRODUCTOS CON URLs REALES
-- ============================================================================

USE neototem;

-- Actualizar imágenes de Nike Air Max 270
UPDATE producto_variante SET image_url = 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b47e1602-8c02-4a1b-9c8e-5b5b5b5b5b5b/air-max-270-mens-shoes-KkLcGR.png' WHERE sku LIKE 'NIKE-AM270%' AND color = 'Negro';
UPDATE producto_variante SET image_url = 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b47e1602-8c02-4a1b-9c8e-5b5b5b5b5b5b/air-max-270-mens-shoes-KkLcGR-white.png' WHERE sku LIKE 'NIKE-AM270%' AND color = 'Blanco';
UPDATE producto_variante SET image_url = 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b47e1602-8c02-4a1b-9c8e-5b5b5b5b5b5b/air-max-270-mens-shoes-KkLcGR-red.png' WHERE sku LIKE 'NIKE-AM270%' AND color = 'Rojo';

-- Actualizar imágenes de Adidas Ultraboost 22
UPDATE producto_variante SET image_url = 'https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/fbaf991a78bc4896a3e9ac8f00d1e2a6_9366/Ultraboost_22_Shoes_Black_GZ0127_01_standard.jpg' WHERE sku LIKE 'ADIDAS-UB22%' AND color = 'Negro';
UPDATE producto_variante SET image_url = 'https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/fbaf991a78bc4896a3e9ac8f00d1e2a6_9366/Ultraboost_22_Shoes_White_GZ0127_01_standard.jpg' WHERE sku LIKE 'ADIDAS-UB22%' AND color = 'Blanco';
UPDATE producto_variante SET image_url = 'https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/fbaf991a78bc4896a3e9ac8f00d1e2a6_9366/Ultraboost_22_Shoes_Blue_GZ0127_01_standard.jpg' WHERE sku LIKE 'ADIDAS-UB22%' AND color = 'Azul';

-- Actualizar imágenes de Converse Chuck Taylor
UPDATE producto_variante SET image_url = 'https://www.converse.com/dw/image/v2/BCZC_PRD/on/demandware.static/-/Sites-cnv-master-catalog/default/dw8b8b8b8b/Chuck_Taylor_All_Star_Black.jpg' WHERE sku LIKE 'CONV-CT%' AND color = 'Negro';
UPDATE producto_variante SET image_url = 'https://www.converse.com/dw/image/v2/BCZC_PRD/on/demandware.static/-/Sites-cnv-master-catalog/default/dw8b8b8b8b/Chuck_Taylor_All_Star_White.jpg' WHERE sku LIKE 'CONV-CT%' AND color = 'Blanco';

-- Actualizar imágenes de Nike Dri-FIT
UPDATE producto_variante SET image_url = 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b47e1602-8c02-4a1b-9c8e-5b5b5b5b5b5b/dri-fit-academy-mens-t-shirt-KkLcGR-black.png' WHERE sku LIKE 'NIKE-DF%' AND color = 'Negro';
UPDATE producto_variante SET image_url = 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b47e1602-8c02-4a1b-9c8e-5b5b5b5b5b5b/dri-fit-academy-mens-t-shirt-KkLcGR-white.png' WHERE sku LIKE 'NIKE-DF%' AND color = 'Blanco';
UPDATE producto_variante SET image_url = 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b47e1602-8c02-4a1b-9c8e-5b5b5b5b5b5b/dri-fit-academy-mens-t-shirt-KkLcGR-red.png' WHERE sku LIKE 'NIKE-DF%' AND color = 'Rojo';

-- Verificar actualizaciones
SELECT p.nombre, pv.sku, pv.color, pv.image_url 
FROM producto p 
JOIN producto_variante pv ON p.id_producto = pv.id_producto 
WHERE p.marca = 'Nike' 
LIMIT 5;

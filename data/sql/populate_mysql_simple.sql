-- ============================================================================
-- POBLAR BD NeoTotem - Script Simple y Compatible
-- ============================================================================

USE neototem;

-- Deshabilitar safe update mode temporalmente
SET SQL_SAFE_UPDATES = 0;

-- Limpiar datos existentes
DELETE FROM evento;
DELETE FROM metricas_sesion;
DELETE FROM interaccion_usuario;
DELETE FROM recomendacion_item;
DELETE FROM recomendacion_sesion;
DELETE FROM consulta_voz;
DELETE FROM deteccion;
DELETE FROM inventario;
DELETE FROM sesion;
DELETE FROM producto_variante;
DELETE FROM producto;
DELETE FROM categoria;
DELETE FROM dispositivo;
DELETE FROM tienda;

-- Rehabilitar safe update mode
SET SQL_SAFE_UPDATES = 1;

-- ============================================================================
-- TIENDAS Y DISPOSITIVOS
-- ============================================================================
INSERT INTO tienda (id_tienda, nombre, ubicacion, region) VALUES 
(1, 'NeoTotem Central', 'Av. Providencia 1234', 'RM'),
(2, 'NeoTotem Norte', 'Mall Plaza Norte', 'RM'),
(3, 'NeoTotem Sur', 'Mall Plaza Sur', 'RM');

INSERT INTO dispositivo (id_dispositivo, id_tienda, etiqueta, estado) VALUES 
(1, 1, 'Totem-Entrada-Principal', 'active'),
(2, 1, 'Totem-Vestuario', 'active'),
(3, 2, 'Totem-Entrada-Norte', 'active'),
(4, 3, 'Totem-Entrada-Sur', 'active');

-- ============================================================================
-- CATEGORÍAS
-- ============================================================================
INSERT INTO categoria (id_categoria, nombre) VALUES 
(1, 'Zapatillas Deportivas'),
(2, 'Zapatillas Casual'),
(3, 'Poleras'),
(4, 'Polerones'),
(5, 'Chaquetas'),
(6, 'Pantalones'),
(7, 'Shorts'),
(8, 'Accesorios');

-- ============================================================================
-- PRODUCTOS Y VARIANTES
-- ============================================================================

-- ZAPATILLAS DEPORTIVAS
INSERT INTO producto (id_producto, nombre, id_categoria, marca) VALUES 
(1, 'Nike Air Max 270', 1, 'Nike'),
(2, 'Adidas Ultraboost 22', 1, 'Adidas'),
(3, 'Puma RS-X', 1, 'Puma'),
(4, 'New Balance 990v5', 1, 'New Balance'),
(5, 'Nike React Infinity Run', 1, 'Nike');

-- Variantes Nike Air Max 270
INSERT INTO producto_variante (id_variante, id_producto, sku, talla, color, precio, image_url) VALUES 
(1, 1, 'NIKE-AM270-40-BLK', '40', 'Negro', 89990, 'https://example.com/nike-airmax-270-negro.jpg'),
(2, 1, 'NIKE-AM270-41-BLK', '41', 'Negro', 89990, 'https://example.com/nike-airmax-270-negro.jpg'),
(3, 1, 'NIKE-AM270-42-BLK', '42', 'Negro', 89990, 'https://example.com/nike-airmax-270-negro.jpg'),
(4, 1, 'NIKE-AM270-40-WHT', '40', 'Blanco', 89990, 'https://example.com/nike-airmax-270-blanco.jpg'),
(5, 1, 'NIKE-AM270-41-WHT', '41', 'Blanco', 89990, 'https://example.com/nike-airmax-270-blanco.jpg'),
(6, 1, 'NIKE-AM270-42-WHT', '42', 'Blanco', 89990, 'https://example.com/nike-airmax-270-blanco.jpg'),
(7, 1, 'NIKE-AM270-40-RED', '40', 'Rojo', 89990, 'https://example.com/nike-airmax-270-rojo.jpg'),
(8, 1, 'NIKE-AM270-41-RED', '41', 'Rojo', 89990, 'https://example.com/nike-airmax-270-rojo.jpg'),
(9, 1, 'NIKE-AM270-42-RED', '42', 'Rojo', 89990, 'https://example.com/nike-airmax-270-rojo.jpg');

-- Variantes Adidas Ultraboost 22
INSERT INTO producto_variante (id_variante, id_producto, sku, talla, color, precio, image_url) VALUES 
(10, 2, 'ADIDAS-UB22-40-BLK', '40', 'Negro', 129990, 'https://example.com/adidas-ultraboost-22-negro.jpg'),
(11, 2, 'ADIDAS-UB22-41-BLK', '41', 'Negro', 129990, 'https://example.com/adidas-ultraboost-22-negro.jpg'),
(12, 2, 'ADIDAS-UB22-42-BLK', '42', 'Negro', 129990, 'https://example.com/adidas-ultraboost-22-negro.jpg'),
(13, 2, 'ADIDAS-UB22-40-WHT', '40', 'Blanco', 129990, 'https://example.com/adidas-ultraboost-22-blanco.jpg'),
(14, 2, 'ADIDAS-UB22-41-WHT', '41', 'Blanco', 129990, 'https://example.com/adidas-ultraboost-22-blanco.jpg'),
(15, 2, 'ADIDAS-UB22-42-WHT', '42', 'Blanco', 129990, 'https://example.com/adidas-ultraboost-22-blanco.jpg'),
(16, 2, 'ADIDAS-UB22-40-BLU', '40', 'Azul', 129990, 'https://example.com/adidas-ultraboost-22-azul.jpg'),
(17, 2, 'ADIDAS-UB22-41-BLU', '41', 'Azul', 129990, 'https://example.com/adidas-ultraboost-22-azul.jpg'),
(18, 2, 'ADIDAS-UB22-42-BLU', '42', 'Azul', 129990, 'https://example.com/adidas-ultraboost-22-azul.jpg');

-- ZAPATILLAS CASUAL
INSERT INTO producto (id_producto, nombre, id_categoria, marca) VALUES 
(6, 'Converse Chuck Taylor', 2, 'Converse'),
(7, 'Vans Old Skool', 2, 'Vans'),
(8, 'Adidas Stan Smith', 2, 'Adidas'),
(9, 'Nike Air Force 1', 2, 'Nike');

-- Variantes Converse Chuck Taylor
INSERT INTO producto_variante (id_variante, id_producto, sku, talla, color, precio, image_url) VALUES 
(19, 6, 'CONV-CT-40-BLK', '40', 'Negro', 49990, 'https://example.com/converse-chuck-negro.jpg'),
(20, 6, 'CONV-CT-41-BLK', '41', 'Negro', 49990, 'https://example.com/converse-chuck-negro.jpg'),
(21, 6, 'CONV-CT-42-BLK', '42', 'Negro', 49990, 'https://example.com/converse-chuck-negro.jpg'),
(22, 6, 'CONV-CT-40-WHT', '40', 'Blanco', 49990, 'https://example.com/converse-chuck-blanco.jpg'),
(23, 6, 'CONV-CT-41-WHT', '41', 'Blanco', 49990, 'https://example.com/converse-chuck-blanco.jpg'),
(24, 6, 'CONV-CT-42-WHT', '42', 'Blanco', 49990, 'https://example.com/converse-chuck-blanco.jpg');

-- POLERAS
INSERT INTO producto (id_producto, nombre, id_categoria, marca) VALUES 
(10, 'Nike Dri-FIT Academy', 3, 'Nike'),
(11, 'Adidas Tiro 21', 3, 'Adidas'),
(12, 'Puma Team Logo', 3, 'Puma'),
(13, 'Under Armour Tech 2.0', 3, 'Under Armour');

-- Variantes Nike Dri-FIT
INSERT INTO producto_variante (id_variante, id_producto, sku, talla, color, precio, image_url) VALUES 
(25, 10, 'NIKE-DF-40-BLK', '40', 'Negro', 24990, 'https://example.com/nike-drifit-negro.jpg'),
(26, 10, 'NIKE-DF-41-BLK', '41', 'Negro', 24990, 'https://example.com/nike-drifit-negro.jpg'),
(27, 10, 'NIKE-DF-42-BLK', '42', 'Negro', 24990, 'https://example.com/nike-drifit-negro.jpg'),
(28, 10, 'NIKE-DF-40-WHT', '40', 'Blanco', 24990, 'https://example.com/nike-drifit-blanco.jpg'),
(29, 10, 'NIKE-DF-41-WHT', '41', 'Blanco', 24990, 'https://example.com/nike-drifit-blanco.jpg'),
(30, 10, 'NIKE-DF-42-WHT', '42', 'Blanco', 24990, 'https://example.com/nike-drifit-blanco.jpg'),
(31, 10, 'NIKE-DF-40-RED', '40', 'Rojo', 24990, 'https://example.com/nike-drifit-rojo.jpg'),
(32, 10, 'NIKE-DF-41-RED', '41', 'Rojo', 24990, 'https://example.com/nike-drifit-rojo.jpg'),
(33, 10, 'NIKE-DF-42-RED', '42', 'Rojo', 24990, 'https://example.com/nike-drifit-rojo.jpg');

-- CHAQUETAS
INSERT INTO producto (id_producto, nombre, id_categoria, marca) VALUES 
(14, 'Nike Sportswear Windrunner', 5, 'Nike'),
(15, 'Adidas Tiro 21 Jacket', 5, 'Adidas'),
(16, 'Puma Archive Track Jacket', 5, 'Puma'),
(17, 'Under Armour Storm', 5, 'Under Armour');

-- Variantes Nike Windrunner
INSERT INTO producto_variante (id_variante, id_producto, sku, talla, color, precio, image_url) VALUES 
(34, 14, 'NIKE-WR-40-BLK', '40', 'Negro', 89990, 'https://example.com/nike-windrunner-negro.jpg'),
(35, 14, 'NIKE-WR-41-BLK', '41', 'Negro', 89990, 'https://example.com/nike-windrunner-negro.jpg'),
(36, 14, 'NIKE-WR-42-BLK', '42', 'Negro', 89990, 'https://example.com/nike-windrunner-negro.jpg'),
(37, 14, 'NIKE-WR-40-BLU', '40', 'Azul', 89990, 'https://example.com/nike-windrunner-azul.jpg'),
(38, 14, 'NIKE-WR-41-BLU', '41', 'Azul', 89990, 'https://example.com/nike-windrunner-azul.jpg'),
(39, 14, 'NIKE-WR-42-BLU', '42', 'Azul', 89990, 'https://example.com/nike-windrunner-azul.jpg');

-- ============================================================================
-- INVENTARIO
-- ============================================================================
-- Inventario para tienda 1 (Central)
INSERT INTO inventario (id_inventario, id_variante, id_tienda, cantidad) VALUES 
(1, 1, 1, 25), (2, 2, 1, 30), (3, 3, 1, 20), (4, 4, 1, 15), (5, 5, 1, 35),
(6, 6, 1, 28), (7, 7, 1, 22), (8, 8, 1, 18), (9, 9, 1, 32), (10, 10, 1, 40),
(11, 11, 1, 25), (12, 12, 1, 30), (13, 13, 1, 20), (14, 14, 1, 15), (15, 15, 1, 35),
(16, 16, 1, 28), (17, 17, 1, 22), (18, 18, 1, 18), (19, 19, 1, 32), (20, 20, 1, 40);

-- Inventario para tienda 2 (Norte)
INSERT INTO inventario (id_inventario, id_variante, id_tienda, cantidad) VALUES 
(21, 1, 2, 15), (22, 2, 2, 20), (23, 3, 2, 12), (24, 4, 2, 8), (25, 5, 2, 25),
(26, 6, 2, 18), (27, 7, 2, 15), (28, 8, 2, 10), (29, 9, 2, 22), (30, 10, 2, 30),
(31, 11, 2, 15), (32, 12, 2, 20), (33, 13, 2, 12), (34, 14, 2, 8), (35, 15, 2, 25),
(36, 16, 2, 18), (37, 17, 2, 15), (38, 18, 2, 10), (39, 19, 2, 22), (40, 20, 2, 30);

-- Inventario para tienda 3 (Sur)
INSERT INTO inventario (id_inventario, id_variante, id_tienda, cantidad) VALUES 
(41, 1, 3, 20), (42, 2, 3, 25), (43, 3, 3, 15), (44, 4, 3, 10), (45, 5, 3, 30),
(46, 6, 3, 22), (47, 7, 3, 18), (48, 8, 3, 12), (49, 9, 3, 28), (50, 10, 3, 35),
(51, 11, 3, 20), (52, 12, 3, 25), (53, 13, 3, 15), (54, 14, 3, 10), (55, 15, 3, 30),
(56, 16, 3, 22), (57, 17, 3, 18), (58, 18, 3, 12), (59, 19, 3, 28), (60, 20, 3, 35);

-- ============================================================================
-- SESIONES DE EJEMPLO
-- ============================================================================

-- Sesión 1: Usuario buscando zapatillas deportivas
INSERT INTO sesion (id_sesion, id_dispositivo, canal, consent) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 1, 'voz', 1);

-- Consulta de voz
INSERT INTO consulta_voz (id_consulta, id_sesion, transcripcion, intencion, entidades, confianza, exito) VALUES 
(1, '550e8400-e29b-41d4-a716-446655440001', 'quiero zapatillas deportivas negras', 'buscar', '{"producto": "zapatillas", "categoria": "deportivas", "color": "negro"}', 'alta', 1);

-- Recomendación generada
INSERT INTO recomendacion_sesion (id_recomendacion, id_sesion, tipo_recomendacion, algoritmo_usado, total_productos_recomendados, tiempo_generacion_ms) VALUES 
(1, '550e8400-e29b-41d4-a716-446655440001', 'categoria', 'filtro_color', 6, 150);

-- Items recomendados
INSERT INTO recomendacion_item (id_item, id_recomendacion, id_variante, posicion, score_recomendacion, fue_mostrado, fue_clicado) VALUES 
(1, 1, 1, 1, 0.95, 1, 1),  -- Nike Air Max 270 Negro 40
(2, 1, 2, 2, 0.90, 1, 0),  -- Nike Air Max 270 Negro 41
(3, 1, 3, 3, 0.85, 1, 0),  -- Nike Air Max 270 Negro 42
(4, 1, 10, 4, 0.80, 1, 0), -- Adidas Ultraboost 22 Negro 40
(5, 1, 11, 5, 0.75, 1, 0), -- Adidas Ultraboost 22 Negro 41
(6, 1, 12, 6, 0.70, 1, 0); -- Adidas Ultraboost 22 Negro 42

-- Interacciones del usuario
INSERT INTO interaccion_usuario (id_interaccion, id_sesion, tipo_interaccion, id_variante, metadata_interaccion, duracion_segundos) VALUES 
(1, '550e8400-e29b-41d4-a716-446655440001', 'view', 1, '{"pantalla": "recomendaciones", "seccion": "zapatillas"}', 3.5),
(2, '550e8400-e29b-41d4-a716-446655440001', 'click', 1, '{"pantalla": "recomendaciones", "accion": "ver_detalle"}', 0.2),
(3, '550e8400-e29b-41d4-a716-446655440001', 'search', NULL, '{"query": "zapatillas deportivas negras", "resultados": 6}', 2.1);

-- Métricas de la sesión
INSERT INTO metricas_sesion (id_metrica, id_sesion, total_recomendaciones_generadas, total_productos_mostrados, total_clics, tasa_clic, tiempo_promedio_visualizacion) VALUES 
(1, '550e8400-e29b-41d4-a716-446655440001', 1, 6, 1, 0.167, 2.5);

COMMIT;

-- ============================================================================
-- VERIFICAR DATOS
-- ============================================================================
SELECT 'PRODUCTOS POR CATEGORIA' as info;
SELECT c.nombre as categoria, COUNT(p.id_producto) as total_productos
FROM categoria c 
LEFT JOIN producto p ON c.id_categoria = p.id_categoria 
GROUP BY c.id_categoria, c.nombre;

SELECT 'VARIANTES POR PRODUCTO' as info;
SELECT p.nombre, p.marca, COUNT(pv.id_variante) as total_variantes
FROM producto p 
LEFT JOIN producto_variante pv ON p.id_producto = pv.id_producto 
GROUP BY p.id_producto, p.nombre, p.marca
ORDER BY total_variantes DESC;

SELECT 'SESIONES CON INTERACCIONES' as info;
SELECT s.id_sesion, s.canal, 
       COUNT(cv.id_consulta) as consultas_voz,
       COUNT(d.id_deteccion) as detecciones,
       COUNT(rs.id_recomendacion) as recomendaciones,
       COUNT(iu.id_interaccion) as interacciones
FROM sesion s
LEFT JOIN consulta_voz cv ON s.id_sesion = cv.id_sesion
LEFT JOIN deteccion d ON s.id_sesion = d.id_sesion  
LEFT JOIN recomendacion_sesion rs ON s.id_sesion = rs.id_sesion
LEFT JOIN interaccion_usuario iu ON s.id_sesion = iu.id_sesion
GROUP BY s.id_sesion, s.canal;

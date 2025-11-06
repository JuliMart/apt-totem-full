-- ============================================================================
-- POBLAR BD NeoTotem con datos reales para recomendaciones
-- ============================================================================

USE neototem;

-- Limpiar datos existentes (con WHERE para evitar safe update mode)
DELETE FROM evento WHERE id_evento > 0;
DELETE FROM metricas_sesion WHERE id_metrica > 0;
DELETE FROM interaccion_usuario WHERE id_interaccion > 0;
DELETE FROM recomendacion_item WHERE id_item > 0;
DELETE FROM recomendacion_sesion WHERE id_recomendacion > 0;
DELETE FROM consulta_voz WHERE id_consulta > 0;
DELETE FROM deteccion WHERE id_deteccion > 0;
DELETE FROM inventario WHERE id_inventario > 0;
DELETE FROM sesion WHERE id_sesion != '';
DELETE FROM producto_variante WHERE id_variante > 0;
DELETE FROM producto WHERE id_producto > 0;
DELETE FROM categoria WHERE id_categoria > 0;
DELETE FROM dispositivo WHERE id_dispositivo > 0;
DELETE FROM tienda WHERE id_tienda > 0;

-- ============================================================================
-- TIENDAS Y DISPOSITIVOS
-- ============================================================================
INSERT INTO tienda (nombre, ubicacion, region) VALUES 
('NeoTotem Central', 'Av. Providencia 1234', 'RM'),
('NeoTotem Norte', 'Mall Plaza Norte', 'RM'),
('NeoTotem Sur', 'Mall Plaza Sur', 'RM');

INSERT INTO dispositivo (id_tienda, etiqueta, estado) VALUES 
(1, 'Totem-Entrada-Principal', 'active'),
(1, 'Totem-Vestuario', 'active'),
(2, 'Totem-Entrada-Norte', 'active'),
(3, 'Totem-Entrada-Sur', 'active');

-- ============================================================================
-- CATEGORÍAS
-- ============================================================================
INSERT INTO categoria (nombre) VALUES 
('Zapatillas Deportivas'),
('Zapatillas Casual'),
('Poleras'),
('Polerones'),
('Chaquetas'),
('Pantalones'),
('Shorts'),
('Accesorios');

-- ============================================================================
-- PRODUCTOS Y VARIANTES
-- ============================================================================

-- ZAPATILLAS DEPORTIVAS
INSERT INTO producto (nombre, id_categoria, marca) VALUES 
('Nike Air Max 270', 1, 'Nike'),
('Adidas Ultraboost 22', 1, 'Adidas'),
('Puma RS-X', 1, 'Puma'),
('New Balance 990v5', 1, 'New Balance'),
('Nike React Infinity Run', 1, 'Nike');

-- Variantes Nike Air Max 270
INSERT INTO producto_variante (id_producto, sku, talla, color, precio, image_url) VALUES 
(1, 'NIKE-AM270-40-BLK', '40', 'Negro', 89990, 'https://example.com/nike-airmax-270-negro.jpg'),
(1, 'NIKE-AM270-41-BLK', '41', 'Negro', 89990, 'https://example.com/nike-airmax-270-negro.jpg'),
(1, 'NIKE-AM270-42-BLK', '42', 'Negro', 89990, 'https://example.com/nike-airmax-270-negro.jpg'),
(1, 'NIKE-AM270-40-WHT', '40', 'Blanco', 89990, 'https://example.com/nike-airmax-270-blanco.jpg'),
(1, 'NIKE-AM270-41-WHT', '41', 'Blanco', 89990, 'https://example.com/nike-airmax-270-blanco.jpg'),
(1, 'NIKE-AM270-42-WHT', '42', 'Blanco', 89990, 'https://example.com/nike-airmax-270-blanco.jpg'),
(1, 'NIKE-AM270-40-RED', '40', 'Rojo', 89990, 'https://example.com/nike-airmax-270-rojo.jpg'),
(1, 'NIKE-AM270-41-RED', '41', 'Rojo', 89990, 'https://example.com/nike-airmax-270-rojo.jpg'),
(1, 'NIKE-AM270-42-RED', '42', 'Rojo', 89990, 'https://example.com/nike-airmax-270-rojo.jpg');

-- Variantes Adidas Ultraboost 22
INSERT INTO producto_variante (id_producto, sku, talla, color, precio, image_url) VALUES 
(2, 'ADIDAS-UB22-40-BLK', '40', 'Negro', 129990, 'https://example.com/adidas-ultraboost-22-negro.jpg'),
(2, 'ADIDAS-UB22-41-BLK', '41', 'Negro', 129990, 'https://example.com/adidas-ultraboost-22-negro.jpg'),
(2, 'ADIDAS-UB22-42-BLK', '42', 'Negro', 129990, 'https://example.com/adidas-ultraboost-22-negro.jpg'),
(2, 'ADIDAS-UB22-40-WHT', '40', 'Blanco', 129990, 'https://example.com/adidas-ultraboost-22-blanco.jpg'),
(2, 'ADIDAS-UB22-41-WHT', '41', 'Blanco', 129990, 'https://example.com/adidas-ultraboost-22-blanco.jpg'),
(2, 'ADIDAS-UB22-42-WHT', '42', 'Blanco', 129990, 'https://example.com/adidas-ultraboost-22-blanco.jpg'),
(2, 'ADIDAS-UB22-40-BLU', '40', 'Azul', 129990, 'https://example.com/adidas-ultraboost-22-azul.jpg'),
(2, 'ADIDAS-UB22-41-BLU', '41', 'Azul', 129990, 'https://example.com/adidas-ultraboost-22-azul.jpg'),
(2, 'ADIDAS-UB22-42-BLU', '42', 'Azul', 129990, 'https://example.com/adidas-ultraboost-22-azul.jpg');

-- ZAPATILLAS CASUAL
INSERT INTO producto (nombre, id_categoria, marca) VALUES 
('Converse Chuck Taylor', 2, 'Converse'),
('Vans Old Skool', 2, 'Vans'),
('Adidas Stan Smith', 2, 'Adidas'),
('Nike Air Force 1', 2, 'Nike');

-- Variantes Converse Chuck Taylor
INSERT INTO producto_variante (id_producto, sku, talla, color, precio, image_url) VALUES 
(6, 'CONV-CT-40-BLK', '40', 'Negro', 49990, 'https://example.com/converse-chuck-negro.jpg'),
(6, 'CONV-CT-41-BLK', '41', 'Negro', 49990, 'https://example.com/converse-chuck-negro.jpg'),
(6, 'CONV-CT-42-BLK', '42', 'Negro', 49990, 'https://example.com/converse-chuck-negro.jpg'),
(6, 'CONV-CT-40-WHT', '40', 'Blanco', 49990, 'https://example.com/converse-chuck-blanco.jpg'),
(6, 'CONV-CT-41-WHT', '41', 'Blanco', 49990, 'https://example.com/converse-chuck-blanco.jpg'),
(6, 'CONV-CT-42-WHT', '42', 'Blanco', 49990, 'https://example.com/converse-chuck-blanco.jpg');

-- POLERAS
INSERT INTO producto (nombre, id_categoria, marca) VALUES 
('Nike Dri-FIT Academy', 3, 'Nike'),
('Adidas Tiro 21', 3, 'Adidas'),
('Puma Team Logo', 3, 'Puma'),
('Under Armour Tech 2.0', 3, 'Under Armour');

-- Variantes Nike Dri-FIT
INSERT INTO producto_variante (id_producto, sku, talla, color, precio, image_url) VALUES 
(10, 'NIKE-DF-40-BLK', '40', 'Negro', 24990, 'https://example.com/nike-drifit-negro.jpg'),
(10, 'NIKE-DF-41-BLK', '41', 'Negro', 24990, 'https://example.com/nike-drifit-negro.jpg'),
(10, 'NIKE-DF-42-BLK', '42', 'Negro', 24990, 'https://example.com/nike-drifit-negro.jpg'),
(10, 'NIKE-DF-40-WHT', '40', 'Blanco', 24990, 'https://example.com/nike-drifit-blanco.jpg'),
(10, 'NIKE-DF-41-WHT', '41', 'Blanco', 24990, 'https://example.com/nike-drifit-blanco.jpg'),
(10, 'NIKE-DF-42-WHT', '42', 'Blanco', 24990, 'https://example.com/nike-drifit-blanco.jpg'),
(10, 'NIKE-DF-40-RED', '40', 'Rojo', 24990, 'https://example.com/nike-drifit-rojo.jpg'),
(10, 'NIKE-DF-41-RED', '41', 'Rojo', 24990, 'https://example.com/nike-drifit-rojo.jpg'),
(10, 'NIKE-DF-42-RED', '42', 'Rojo', 24990, 'https://example.com/nike-drifit-rojo.jpg');

-- CHAQUETAS
INSERT INTO producto (nombre, id_categoria, marca) VALUES 
('Nike Sportswear Windrunner', 5, 'Nike'),
('Adidas Tiro 21 Jacket', 5, 'Adidas'),
('Puma Archive Track Jacket', 5, 'Puma'),
('Under Armour Storm', 5, 'Under Armour');

-- Variantes Nike Windrunner
INSERT INTO producto_variante (id_producto, sku, talla, color, precio, image_url) VALUES 
(14, 'NIKE-WR-40-BLK', '40', 'Negro', 89990, 'https://example.com/nike-windrunner-negro.jpg'),
(14, 'NIKE-WR-41-BLK', '41', 'Negro', 89990, 'https://example.com/nike-windrunner-negro.jpg'),
(14, 'NIKE-WR-42-BLK', '42', 'Negro', 89990, 'https://example.com/nike-windrunner-negro.jpg'),
(14, 'NIKE-WR-40-BLU', '40', 'Azul', 89990, 'https://example.com/nike-windrunner-azul.jpg'),
(14, 'NIKE-WR-41-BLU', '41', 'Azul', 89990, 'https://example.com/nike-windrunner-azul.jpg'),
(14, 'NIKE-WR-42-BLU', '42', 'Azul', 89990, 'https://example.com/nike-windrunner-azul.jpg');

-- ============================================================================
-- INVENTARIO
-- ============================================================================
-- Inventario para tienda 1 (Central)
INSERT INTO inventario (id_variante, id_tienda, cantidad) 
SELECT id_variante, 1, FLOOR(RAND() * 50) + 10 FROM producto_variante;

-- Inventario para tienda 2 (Norte)
INSERT INTO inventario (id_variante, id_tienda, cantidad) 
SELECT id_variante, 2, FLOOR(RAND() * 30) + 5 FROM producto_variante;

-- Inventario para tienda 3 (Sur)
INSERT INTO inventario (id_variante, id_tienda, cantidad) 
SELECT id_variante, 3, FLOOR(RAND() * 40) + 8 FROM producto_variante;

-- ============================================================================
-- SESIONES DE EJEMPLO CON INTERACCIONES
-- ============================================================================

-- Sesión 1: Usuario buscando zapatillas deportivas
INSERT INTO sesion (id_sesion, id_dispositivo, canal, consent) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 1, 'voz', 1);

-- Consulta de voz
INSERT INTO consulta_voz (id_sesion, transcripcion, intencion, entidades, confianza, exito) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 'quiero zapatillas deportivas negras', 'buscar', '{"producto": "zapatillas", "categoria": "deportivas", "color": "negro"}', 'alta', 1);

-- Recomendación generada
INSERT INTO recomendacion_sesion (id_sesion, tipo_recomendacion, algoritmo_usado, total_productos_recomendados, tiempo_generacion_ms) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 'categoria', 'filtro_color', 6, 150);

-- Items recomendados
INSERT INTO recomendacion_item (id_recomendacion, id_variante, posicion, score_recomendacion, fue_mostrado, fue_clicado) VALUES 
(1, 1, 1, 0.95, 1, 1),  -- Nike Air Max 270 Negro 40
(1, 2, 2, 0.90, 1, 0),  -- Nike Air Max 270 Negro 41
(1, 3, 3, 0.85, 1, 0),  -- Nike Air Max 270 Negro 42
(1, 10, 4, 0.80, 1, 0), -- Adidas Ultraboost 22 Negro 40
(1, 11, 5, 0.75, 1, 0), -- Adidas Ultraboost 22 Negro 41
(1, 12, 6, 0.70, 1, 0); -- Adidas Ultraboost 22 Negro 42

-- Interacciones del usuario
INSERT INTO interaccion_usuario (id_sesion, tipo_interaccion, id_variante, metadata_interaccion, duracion_segundos) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 'view', 1, '{"pantalla": "recomendaciones", "seccion": "zapatillas"}', 3.5),
('550e8400-e29b-41d4-a716-446655440001', 'click', 1, '{"pantalla": "recomendaciones", "accion": "ver_detalle"}', 0.2),
('550e8400-e29b-41d4-a716-446655440001', 'search', NULL, '{"query": "zapatillas deportivas negras", "resultados": 6}', 2.1);

-- Métricas de la sesión
INSERT INTO metricas_sesion (id_sesion, total_recomendaciones_generadas, total_productos_mostrados, total_clics, tasa_clic, tiempo_promedio_visualizacion) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 1, 6, 1, 0.167, 2.5);

-- Sesión 2: Usuario buscando poleras
INSERT INTO sesion (id_sesion, id_dispositivo, canal, consent) VALUES 
('550e8400-e29b-41d4-a716-446655440002', 1, 'tactil', 1);

INSERT INTO consulta_voz (id_sesion, transcripcion, intencion, entidades, confianza, exito) VALUES 
('550e8400-e29b-41d4-a716-446655440002', 'busco poleras blancas', 'buscar', '{"producto": "poleras", "color": "blanco"}', 'alta', 1);

INSERT INTO recomendacion_sesion (id_sesion, tipo_recomendacion, algoritmo_usado, total_productos_recomendados, tiempo_generacion_ms) VALUES 
('550e8400-e29b-41d4-a716-446655440002', 'categoria', 'filtro_color', 3, 120);

INSERT INTO recomendacion_item (id_recomendacion, id_variante, posicion, score_recomendacion, fue_mostrado, fue_clicado) VALUES 
(2, 19, 1, 0.95, 1, 1),  -- Nike Dri-FIT Blanco 40
(2, 20, 2, 0.90, 1, 0),  -- Nike Dri-FIT Blanco 41
(2, 21, 3, 0.85, 1, 0);  -- Nike Dri-FIT Blanco 42

INSERT INTO interaccion_usuario (id_sesion, tipo_interaccion, id_variante, metadata_interaccion, duracion_segundos) VALUES 
('550e8400-e29b-41d4-a716-446655440002', 'view', 19, '{"pantalla": "recomendaciones", "seccion": "poleras"}', 2.8),
('550e8400-e29b-41d4-a716-446655440002', 'click', 19, '{"pantalla": "recomendaciones", "accion": "ver_detalle"}', 0.3),
('550e8400-e29b-41d4-a716-446655440002', 'search', NULL, '{"query": "poleras blancas", "resultados": 3}', 1.5);

INSERT INTO metricas_sesion (id_sesion, total_recomendaciones_generadas, total_productos_mostrados, total_clics, tasa_clic, tiempo_promedio_visualizacion) VALUES 
('550e8400-e29b-41d4-a716-446655440002', 1, 3, 1, 0.333, 2.1);

-- Sesión 3: Usuario con detección de cámara
INSERT INTO sesion (id_sesion, id_dispositivo, canal, consent) VALUES 
('550e8400-e29b-41d4-a716-446655440003', 1, 'mixto', 1);

INSERT INTO deteccion (id_sesion, prenda, color, rango_etario, genero, color_dominante, confianza, modelo_version) VALUES 
('550e8400-e29b-41d4-a716-446655440003', 'zapatillas', 'negro', 'adult', 'masculine', 'negro', 0.85, 'yolo_v8');

INSERT INTO consulta_voz (id_sesion, transcripcion, intencion, entidades, confianza, exito) VALUES 
('550e8400-e29b-41d4-a716-446655440003', 'recomiéndame algo similar', 'recomendar', '{"contexto": "deteccion_camara", "prenda_detectada": "zapatillas", "color_detectado": "negro"}', 'media', 1);

INSERT INTO recomendacion_sesion (id_sesion, tipo_recomendacion, algoritmo_usado, total_productos_recomendados, tiempo_generacion_ms) VALUES 
('550e8400-e29b-41d4-a716-446655440003', 'similar', 'vision_based', 4, 200);

INSERT INTO recomendacion_item (id_recomendacion, id_variante, posicion, score_recomendacion, fue_mostrado, fue_clicado) VALUES 
(3, 1, 1, 0.90, 1, 0),  -- Nike Air Max 270 Negro 40
(3, 2, 2, 0.85, 1, 1),  -- Nike Air Max 270 Negro 41
(3, 10, 3, 0.80, 1, 0), -- Adidas Ultraboost 22 Negro 40
(3, 11, 4, 0.75, 1, 0); -- Adidas Ultraboost 22 Negro 41

INSERT INTO interaccion_usuario (id_sesion, tipo_interaccion, id_variante, metadata_interaccion, duracion_segundos) VALUES 
('550e8400-e29b-41d4-a716-446655440003', 'camera_detection', NULL, '{"prenda": "zapatillas", "color": "negro", "confianza": 0.85}', 0.0),
('550e8400-e29b-41d4-a716-446655440003', 'view', 1, '{"pantalla": "recomendaciones", "seccion": "similar"}', 4.2),
('550e8400-e29b-41d4-a716-446655440003', 'click', 2, '{"pantalla": "recomendaciones", "accion": "ver_detalle"}', 0.4);

INSERT INTO metricas_sesion (id_sesion, total_recomendaciones_generadas, total_productos_mostrados, total_clics, tasa_clic, tiempo_promedio_visualizacion) VALUES 
('550e8400-e29b-41d4-a716-446655440003', 1, 4, 1, 0.25, 3.1);

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

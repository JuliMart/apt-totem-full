-- Sembrar métricas históricas realistas (últimos 30 días)
-- Ejecutar en MySQL 8+ conectado a la BD neototem
-- No elimina datos; solo agrega cuando falta histórico

USE neototem;

-- Generador de series de días
WITH RECURSIVE days AS (
  SELECT (CURDATE() - INTERVAL 30 DAY) AS d
  UNION ALL
  SELECT d + INTERVAL 1 DAY FROM days WHERE d < CURDATE() - INTERVAL 1 DAY
),
nums AS (
  SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
),
sessions_to_create AS (
  -- Para cada día, generamos entre 3 y 10 sesiones pseudo-aleatorias
  SELECT 
    UUID() AS id_sesion,
    d AS day_ref,
    -- hora de inicio entre 09:00 y 20:00
    TIMESTAMP(d, MAKETIME(9,0,0)) + INTERVAL FLOOR(RAND()* (11*60)) MINUTE AS inicio,
    'tracking' AS canal
  FROM days
  JOIN nums n1 ON n1.n <= 10
  WHERE n1.n <= 3 + FLOOR(RAND()*8)
),
missing_sessions AS (
  SELECT s.*
  FROM sessions_to_create s
  LEFT JOIN sesion e ON DATE(e.inicio) = DATE(s.inicio)
  GROUP BY s.id_sesion, s.day_ref, s.inicio, s.canal
)
INSERT INTO sesion (id_sesion, id_dispositivo, inicio, termino, canal)
SELECT 
  id_sesion,
  1,
  inicio,
  inicio + INTERVAL (1 + FLOOR(RAND()*9)) MINUTE,
  canal
FROM missing_sessions;

-- Recomendaciones por sesión (1-4)
INSERT INTO recomendacion_sesion (
  id_sesion, fecha_hora, tipo_recomendacion, filtros_aplicados,
  algoritmo_usado, total_productos_recomendados, tiempo_generacion_ms
)
SELECT 
  s.id_sesion,
  s.inicio + INTERVAL FLOOR(RAND()*4) MINUTE,
  ELT(1+FLOOR(RAND()*4),'categoria','marca','color','personalizada'),
  '{}',
  ELT(1+FLOOR(RAND()*4),'trending','search_engine','similar','personalized'),
  3 + FLOOR(RAND()*8),
  120 + FLOOR(RAND()*900)
FROM sesion s
JOIN nums n ON n.n <= 4
WHERE s.inicio >= CURDATE() - INTERVAL 30 DAY
  AND n.n <= 1 + FLOOR(RAND()*4);

-- Vistas de recomendación (recommendation_viewed) y clics (click)
-- Creamos vistas 1-3 por recomendación y clic con prob 15-35%
INSERT INTO interaccion_usuario (
  id_sesion, fecha_hora, tipo_interaccion, id_variante, metadata_interaccion, duracion_segundos
)
SELECT 
  r.id_sesion,
  r.fecha_hora + INTERVAL (5 + FLOOR(RAND()*120)) SECOND,
  'recommendation_viewed',
  NULL,
  NULL,
  ROUND(RAND()*3,2)
FROM recomendacion_sesion r
JOIN nums n ON n.n <= 3
WHERE r.fecha_hora >= CURDATE() - INTERVAL 30 DAY
  AND n.n <= 1 + FLOOR(RAND()*3);

INSERT INTO interaccion_usuario (
  id_sesion, fecha_hora, tipo_interaccion, id_variante, metadata_interaccion, duracion_segundos
)
SELECT 
  r.id_sesion,
  r.fecha_hora + INTERVAL (10 + FLOOR(RAND()*240)) SECOND,
  'click',
  NULL,
  NULL,
  0
FROM recomendacion_sesion r
WHERE r.fecha_hora >= CURDATE() - INTERVAL 30 DAY
  AND RAND() < 0.30; -- prob. de aceptación

-- Detecciones por sesión (0-2)
INSERT INTO deteccion (
  id_sesion, fecha_hora, prenda, color, rango_etario, confianza
)
SELECT 
  s.id_sesion,
  s.inicio + INTERVAL FLOOR(RAND()*10) MINUTE,
  ELT(1+FLOOR(RAND()*5),'camiseta','chaqueta','pantalon','gorra','zapatillas'),
  ELT(1+FLOOR(RAND()*5),'negro','azul','blanco','rojo','verde'),
  ELT(1+FLOOR(RAND()*4),'18-25','26-35','36-45','46-60'),
  0.65 + RAND()*0.3
FROM sesion s
JOIN nums n ON n.n <= 2
WHERE s.inicio >= CURDATE() - INTERVAL 30 DAY
  AND n.n <= FLOOR(RAND()*3);

-- Fin



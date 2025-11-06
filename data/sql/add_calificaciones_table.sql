-- Script para agregar tabla de calificaciones de recomendaciones
-- Ejecutar en MySQL

USE neototem;

-- Crear tabla de calificaciones
CREATE TABLE IF NOT EXISTS calificacion_recomendacion (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_sesion VARCHAR(36) NOT NULL,
    id_recomendacion INT NOT NULL,
    calificacion INT NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_sesion (id_sesion),
    INDEX idx_recomendacion (id_recomendacion),
    INDEX idx_fecha (fecha_hora),
    
    -- Claves foráneas
    FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE,
    FOREIGN KEY (id_recomendacion) REFERENCES recomendacion_sesion(id_recomendacion) ON DELETE CASCADE
);

-- Insertar datos de ejemplo para testing
INSERT INTO calificacion_recomendacion (id_sesion, id_recomendacion, calificacion, comentario, fecha_hora) VALUES
('550e8400-e29b-41d4-a716-446655440000', 1, 5, 'Excelente recomendación, muy acertada', '2025-10-27 10:30:00'),
('550e8400-e29b-41d4-a716-446655440000', 2, 4, 'Buena recomendación, me gustó', '2025-10-27 10:35:00'),
('550e8400-e29b-41d4-a716-446655440001', 3, 5, 'Perfecto, exactamente lo que buscaba', '2025-10-27 11:15:00'),
('550e8400-e29b-41d4-a716-446655440001', 4, 3, 'Regular, no era exactamente mi estilo', '2025-10-27 11:20:00'),
('550e8400-e29b-41d4-a716-446655440002', 5, 4, 'Muy buena sugerencia', '2025-10-27 12:00:00'),
('550e8400-e29b-41d4-a716-446655440002', 6, 5, 'Increíble, superó mis expectativas', '2025-10-27 12:05:00'),
('550e8400-e29b-41d4-a716-446655440003', 7, 2, 'No me convenció mucho', '2025-10-27 13:30:00'),
('550e8400-e29b-41d4-a716-446655440003', 8, 4, 'Buena opción', '2025-10-27 13:35:00'),
('550e8400-e29b-41d4-a716-446655440004', 9, 5, 'Excelente, muy recomendado', '2025-10-27 14:00:00'),
('550e8400-e29b-41d4-a716-446655440004', 10, 3, 'Está bien, pero podría ser mejor', '2025-10-27 14:05:00');

-- Verificar que se creó correctamente
SELECT 
    COUNT(*) as total_calificaciones,
    AVG(calificacion) as promedio_calificacion,
    MIN(calificacion) as calificacion_minima,
    MAX(calificacion) as calificacion_maxima
FROM calificacion_recomendacion;

-- Mostrar algunas calificaciones de ejemplo
SELECT 
    cr.id_calificacion,
    cr.calificacion,
    cr.comentario,
    rs.producto,
    cr.fecha_hora
FROM calificacion_recomendacion cr
JOIN recomendacion_sesion rs ON cr.id_recomendacion = rs.id_recomendacion
ORDER BY cr.fecha_hora DESC
LIMIT 5;


-- Script para agregar tabla de calificaciones de grupos de recomendaciones
-- Ejecutar en MySQL

USE neototem;

-- Crear tabla de calificaciones de grupos
CREATE TABLE IF NOT EXISTS calificacion_grupo_recomendacion (
    id_calificacion_grupo INT AUTO_INCREMENT PRIMARY KEY,
    id_sesion VARCHAR(36) NOT NULL,
    tipo_grupo VARCHAR(50) NOT NULL,
    nombre_grupo VARCHAR(100) NOT NULL,
    productos_incluidos TEXT,
    calificacion_general INT NOT NULL CHECK (calificacion_general >= 1 AND calificacion_general <= 5),
    comentario_grupo TEXT,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_sesion (id_sesion),
    INDEX idx_tipo_grupo (tipo_grupo),
    INDEX idx_nombre_grupo (nombre_grupo),
    INDEX idx_fecha (fecha_hora),
    
    -- Claves foráneas
    FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE
);

-- Insertar datos de ejemplo para testing
INSERT INTO calificacion_grupo_recomendacion (id_sesion, tipo_grupo, nombre_grupo, productos_incluidos, calificacion_general, comentario_grupo, fecha_hora) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'categoria', 'Zapatillas', '[1,2,3,4,5]', 5, 'Excelente selección de zapatillas, muy variada', '2025-10-27 10:30:00'),
('550e8400-e29b-41d4-a716-446655440000', 'marca', 'Nike', '[6,7,8,9]', 4, 'Buena calidad de Nike, pero falta más variedad', '2025-10-27 10:35:00'),
('550e8400-e29b-41d4-a716-446655440001', 'color', 'Azul', '[10,11,12]', 5, 'Perfecto, me encanta el color azul', '2025-10-27 11:15:00'),
('550e8400-e29b-41d4-a716-446655440001', 'estilo', 'Deportivo', '[13,14,15,16]', 4, 'Muy buena selección deportiva', '2025-10-27 11:20:00'),
('550e8400-e29b-41d4-a716-446655440002', 'categoria', 'Poleras', '[17,18,19]', 3, 'Regular, no era exactamente mi estilo', '2025-10-27 12:00:00'),
('550e8400-e29b-41d4-a716-446655440002', 'marca', 'Adidas', '[20,21,22,23]', 5, 'Increíble selección de Adidas', '2025-10-27 12:05:00'),
('550e8400-e29b-41d4-a716-446655440003', 'color', 'Negro', '[24,25,26]', 2, 'No me convenció mucho la selección', '2025-10-27 13:30:00'),
('550e8400-e29b-41d4-a716-446655440003', 'estilo', 'Formal', '[27,28,29]', 4, 'Buena opción para eventos formales', '2025-10-27 13:35:00'),
('550e8400-e29b-41d4-a716-446655440004', 'categoria', 'Accesorios', '[30,31,32,33]', 5, 'Excelente variedad de accesorios', '2025-10-27 14:00:00'),
('550e8400-e29b-41d4-a716-446655440004', 'marca', 'Puma', '[34,35,36]', 3, 'Está bien, pero podría ser mejor', '2025-10-27 14:05:00');


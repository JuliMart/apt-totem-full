-- -----------------------------------------------------
-- PROYECTO: Totem Retail - Modelo de Datos (MySQL 8.x)
-- COMPAT: usa AUTO_INCREMENT, JSON y DATETIME
-- NOTA: id_sesion se maneja como CHAR(36) (UUID desde la app)
-- -----------------------------------------------------

DROP TABLE IF EXISTS recommendation_item;
DROP TABLE IF EXISTS recommendation_set;
DROP TABLE IF EXISTS evento;
DROP TABLE IF EXISTS consulta_voz;
DROP TABLE IF EXISTS deteccion;
DROP TABLE IF EXISTS inventario;
DROP TABLE IF EXISTS producto_variante;
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS sesion;
DROP TABLE IF EXISTS dispositivo;
DROP TABLE IF EXISTS tienda;

-- -----------------------------------------------------
-- MAESTROS
-- -----------------------------------------------------
CREATE TABLE tienda (
  id_tienda INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  ubicacion VARCHAR(100),
  region VARCHAR(50),
  timezone VARCHAR(50) DEFAULT 'America/Santiago'
);

CREATE TABLE dispositivo (
  id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
  id_tienda INT NOT NULL,
  etiqueta VARCHAR(50),
  estado ENUM('active','inactive') DEFAULT 'active',
  api_key CHAR(36) DEFAULT (UUID()),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_tienda) REFERENCES tienda(id_tienda)
);

CREATE TABLE categoria (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE producto (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  id_categoria INT NOT NULL,
  marca VARCHAR(60),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE producto_variante (
  id_variante INT AUTO_INCREMENT PRIMARY KEY,
  id_producto INT NOT NULL,
  sku VARCHAR(40) NOT NULL UNIQUE,
  talla VARCHAR(20),
  color VARCHAR(30),
  precio DECIMAL(10,2) NOT NULL,
  image_url VARCHAR(400),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_producto) REFERENCES producto(id_producto) ON DELETE CASCADE,
  UNIQUE KEY uq_pv (id_producto, talla, color),
  INDEX ix_pv_producto (id_producto)
);

-- -----------------------------------------------------
-- OPERACIONAL
-- -----------------------------------------------------
CREATE TABLE sesion (
  id_sesion CHAR(36) PRIMARY KEY, -- UUID desde la app
  id_dispositivo INT NOT NULL,
  inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
  termino DATETIME,
  canal VARCHAR(20), -- voz / tactil
  consent BOOLEAN DEFAULT 0,
  FOREIGN KEY (id_dispositivo) REFERENCES dispositivo(id_dispositivo)
);

CREATE TABLE inventario (
  id_inventario INT AUTO_INCREMENT PRIMARY KEY,
  id_variante INT NOT NULL,
  id_tienda INT NOT NULL,
  cantidad INT DEFAULT 0 NOT NULL,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_variante) REFERENCES producto_variante(id_variante),
  FOREIGN KEY (id_tienda) REFERENCES tienda(id_tienda),
  UNIQUE KEY uq_inventario (id_tienda, id_variante)
);

CREATE TABLE deteccion (
  id_deteccion INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion CHAR(36) NOT NULL,
  fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
  prenda VARCHAR(50),
  color VARCHAR(50),
  rango_etario ENUM('child','youth','adult','senior'),
  genero ENUM('masculine','feminine','unknown'),
  color_dominante VARCHAR(30),
  confianza JSON,
  modelo_version VARCHAR(50),
  FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  INDEX ix_deteccion_sesion_fecha (id_sesion, fecha_hora)
);

CREATE TABLE consulta_voz (
  id_consulta INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion CHAR(36) NOT NULL,
  fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
  transcripcion TEXT,
  intencion VARCHAR(80),
  entidades JSON,
  confianza JSON,
  latencia_ms INT,
  exito BOOLEAN,
  FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  INDEX ix_cv_sesion_fecha (id_sesion, fecha_hora)
);

CREATE TABLE recommendation_set (
  id_set INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion CHAR(36) NOT NULL,
  fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
  estrategia VARCHAR(50),
  FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE
);

CREATE TABLE recommendation_item (
  id_item INT AUTO_INCREMENT PRIMARY KEY,
  id_set INT NOT NULL,
  id_variante INT NOT NULL,
  score DECIMAL(5,4),
  mostrado BOOLEAN,
  clicado BOOLEAN,
  FOREIGN KEY (id_set) REFERENCES recommendation_set(id_set) ON DELETE CASCADE,
  FOREIGN KEY (id_variante) REFERENCES producto_variante(id_variante),
  INDEX ix_reco_item_set (id_set)
);

CREATE TABLE evento (
  id_evento INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion CHAR(36) NOT NULL,
  fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
  tipo VARCHAR(40) NOT NULL, -- view, click, dwell, oos, voice_ok, voice_fail...
  metadata JSON,
  FOREIGN KEY (id_sesion) REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  INDEX ix_evento_sesion_fecha (id_sesion, fecha_hora)
);

-- -----------------------------------------------------
-- DATOS DE EJEMPLO
-- -----------------------------------------------------
INSERT INTO tienda (nombre, ubicacion, region)
VALUES ('Tienda Central', 'Av. Principal 123', 'RM');

INSERT INTO dispositivo (id_tienda, etiqueta)
SELECT id_tienda, 'Totem-Entrada'
FROM tienda WHERE nombre = 'Tienda Central';

INSERT INTO categoria (nombre) VALUES ('Zapatillas'), ('Poleras'), ('Chaquetas');

INSERT INTO producto (nombre, id_categoria, marca)
SELECT 'Zapatilla Runner X', id_categoria, 'MarcaZ'
FROM categoria WHERE nombre = 'Zapatillas';

INSERT INTO producto_variante (id_producto, sku, talla, color, precio)
SELECT id_producto, 'SKU-RUNX-42-RED', '42', 'Rojo', 49990
FROM producto WHERE nombre = 'Zapatilla Runner X';

COMMIT;

-- ============================================================================
-- PROYECTO: NeoTotem Retail - Esquema MySQL Completo
-- INCLUYE: Todas las tablas para métricas, analytics y tracking
-- ============================================================================

USE neototem;

-- ============================================================================
-- MAESTROS
-- ============================================================================
CREATE TABLE tienda (
  id_tienda   INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(50) NOT NULL,
  ubicacion   VARCHAR(100),
  region      VARCHAR(50),
  timezone    VARCHAR(50) DEFAULT 'America/Santiago'
);

CREATE TABLE dispositivo (
  id_dispositivo INT AUTO_INCREMENT PRIMARY KEY,
  id_tienda      INT NOT NULL,
  etiqueta       VARCHAR(50),
  estado         VARCHAR(10) DEFAULT 'active' CHECK (estado IN ('active','inactive')),
  api_key        VARCHAR(36) DEFAULT (UUID()),
  created_at     DATETIME DEFAULT NOW(),
  CONSTRAINT dispositivo_tienda_fk
    FOREIGN KEY (id_tienda) REFERENCES tienda(id_tienda)
);

CREATE TABLE categoria (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(50) NOT NULL
);

CREATE TABLE producto (
  id_producto  INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(100) NOT NULL,
  id_categoria INT NOT NULL,
  marca        VARCHAR(60),
  created_at   DATETIME DEFAULT NOW(),
  updated_at   DATETIME DEFAULT NOW(),
  CONSTRAINT producto_categoria_fk
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE producto_variante (
  id_variante  INT AUTO_INCREMENT PRIMARY KEY,
  id_producto   INT NOT NULL,
  sku          VARCHAR(40) NOT NULL UNIQUE,
  talla        VARCHAR(20),
  color        VARCHAR(30),
  precio       DECIMAL(10,2) NOT NULL,
  image_url    VARCHAR(400),
  created_at   DATETIME DEFAULT NOW(),
  updated_at   DATETIME DEFAULT NOW(),
  CONSTRAINT pv_producto_fk FOREIGN KEY (id_producto)
    REFERENCES producto(id_producto) ON DELETE CASCADE,
  CONSTRAINT pv_unique UNIQUE (id_producto, talla, color)
);
CREATE INDEX ix_pv_producto ON producto_variante(id_producto);

-- ============================================================================
-- OPERACIONAL
-- ============================================================================
CREATE TABLE sesion (
  id_sesion      VARCHAR(36) PRIMARY KEY,
  id_dispositivo INT NOT NULL,
  inicio         DATETIME DEFAULT NOW(),
  termino        DATETIME,
  canal          VARCHAR(20), -- voz / tactil
  consent        TINYINT(1) DEFAULT 0 CHECK (consent IN (0,1)),
  CONSTRAINT sesion_dispositivo_fk
    FOREIGN KEY (id_dispositivo) REFERENCES dispositivo(id_dispositivo)
);

CREATE TABLE inventario (
  id_inventario INT AUTO_INCREMENT PRIMARY KEY,
  id_variante   INT NOT NULL,
  id_tienda     INT NOT NULL,
  cantidad      INT DEFAULT 0 NOT NULL,
  updated_at    DATETIME DEFAULT NOW(),
  CONSTRAINT inventario_variante_fk FOREIGN KEY (id_variante)
    REFERENCES producto_variante(id_variante),
  CONSTRAINT inventario_tienda_fk FOREIGN KEY (id_tienda)
    REFERENCES tienda(id_tienda),
  CONSTRAINT inventario_unique UNIQUE (id_tienda, id_variante)
);

CREATE TABLE deteccion (
  id_deteccion    INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion       VARCHAR(36) NOT NULL,
  fecha_hora      DATETIME DEFAULT NOW(),
  prenda          VARCHAR(50),
  color           VARCHAR(50),
  rango_etario    VARCHAR(20),  -- child / youth / adult / senior
  genero          VARCHAR(20),  -- masculine / feminine / unknown
  color_dominante VARCHAR(30),
  confianza       TEXT,         -- JSON libre
  modelo_version  VARCHAR(50),
  CONSTRAINT deteccion_sesion_fk FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion) ON DELETE CASCADE
);
CREATE INDEX ix_deteccion_sesion_fecha ON deteccion(id_sesion, fecha_hora);

CREATE TABLE consulta_voz (
  id_consulta    INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion      VARCHAR(36) NOT NULL,
  fecha_hora     DATETIME DEFAULT NOW(),
  transcripcion  TEXT,
  intencion      VARCHAR(80),
  entidades      TEXT,         -- JSON libre
  confianza      TEXT,         -- JSON libre
  latencia_ms    INT,
  exito          TINYINT(1) CHECK (exito IN (0,1)),
  CONSTRAINT consulta_voz_sesion_fk FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion) ON DELETE CASCADE
);
CREATE INDEX ix_cv_sesion_fecha ON consulta_voz(id_sesion, fecha_hora);

-- ============================================================================
-- RECOMENDACIONES Y ANALYTICS (TABLAS FALTANTES)
-- ============================================================================
CREATE TABLE recomendacion_sesion (
  id_recomendacion INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion VARCHAR(36) NOT NULL,
  fecha_hora DATETIME DEFAULT NOW(),
  tipo_recomendacion VARCHAR(50) NOT NULL,
  filtros_aplicados TEXT,
  algoritmo_usado VARCHAR(50),
  total_productos_recomendados INT DEFAULT 0,
  tiempo_generacion_ms INT,
  CONSTRAINT reco_sesion_fk FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion) ON DELETE CASCADE
);

CREATE TABLE recomendacion_item (
  id_item INT AUTO_INCREMENT PRIMARY KEY,
  id_recomendacion INT NOT NULL,
  id_variante INT NOT NULL,
  posicion INT NOT NULL,
  score_recomendacion FLOAT,
  fue_mostrado BOOLEAN DEFAULT FALSE,
  fue_clicado BOOLEAN DEFAULT FALSE,
  tiempo_visualizacion_segundos FLOAT,
  fecha_clic DATETIME,
  CONSTRAINT reco_item_recomendacion_fk FOREIGN KEY (id_recomendacion)
    REFERENCES recomendacion_sesion(id_recomendacion) ON DELETE CASCADE,
  CONSTRAINT reco_item_variante_fk FOREIGN KEY (id_variante)
    REFERENCES producto_variante(id_variante)
);

CREATE TABLE interaccion_usuario (
  id_interaccion INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion VARCHAR(36) NOT NULL,
  fecha_hora DATETIME DEFAULT NOW(),
  tipo_interaccion VARCHAR(50) NOT NULL,
  id_variante INT,
  metadata_interaccion TEXT,
  duracion_segundos FLOAT,
  CONSTRAINT interaccion_sesion_fk FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  CONSTRAINT interaccion_variante_fk FOREIGN KEY (id_variante)
    REFERENCES producto_variante(id_variante)
);

CREATE TABLE metricas_sesion (
  id_metrica INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion VARCHAR(36) NOT NULL,
  fecha_calculo DATETIME DEFAULT NOW(),
  total_recomendaciones_generadas INT DEFAULT 0,
  total_productos_mostrados INT DEFAULT 0,
  total_clics INT DEFAULT 0,
  tasa_clic FLOAT,
  tiempo_promedio_visualizacion FLOAT,
  productos_mas_clicados TEXT,
  categorias_mas_populares TEXT,
  conversion_rate FLOAT,
  CONSTRAINT metricas_sesion_fk FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion) ON DELETE CASCADE
);

-- Eventos genéricos
CREATE TABLE evento (
  id_evento   INT AUTO_INCREMENT PRIMARY KEY,
  id_sesion   VARCHAR(36) NOT NULL,
  fecha_hora  DATETIME DEFAULT NOW(),
  tipo        VARCHAR(40) NOT NULL, -- view, click, dwell, oos, voice_ok, voice_fail...
  metadata    TEXT,
  CONSTRAINT evento_sesion_fk FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion) ON DELETE CASCADE
);
CREATE INDEX ix_evento_sesion_fecha ON evento(id_sesion, fecha_hora);

-- ============================================================================
-- DATOS DE EJEMPLO
-- ============================================================================
INSERT INTO tienda (nombre, ubicacion, region) VALUES ('Tienda Central', 'Av. Principal 123', 'RM');

INSERT INTO dispositivo (id_tienda, etiqueta)
SELECT id_tienda, 'Totem-Entrada' FROM tienda WHERE nombre = 'Tienda Central';

INSERT INTO categoria (nombre) VALUES ('Zapatillas');
INSERT INTO categoria (nombre) VALUES ('Poleras');
INSERT INTO categoria (nombre) VALUES ('Chaquetas');

INSERT INTO producto (nombre, id_categoria, marca)
SELECT 'Zapatilla Runner X', id_categoria, 'MarcaZ'
FROM categoria WHERE nombre = 'Zapatillas';

INSERT INTO producto_variante (id_producto, sku, talla, color, precio)
SELECT id_producto, 'SKU-RUNX-42-RED', '42', 'Rojo', 49990
FROM producto WHERE nombre = 'Zapatilla Runner X';

COMMIT;

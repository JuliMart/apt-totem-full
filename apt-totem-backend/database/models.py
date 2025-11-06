from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

# --- Catálogo ---
class Categoria(Base):
    __tablename__ = "categoria"
    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "producto"
    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categoria.id_categoria"), nullable=False)
    marca = Column(String(60))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="productos")
    variantes = relationship("ProductoVariante", back_populates="producto")

class ProductoVariante(Base):
    __tablename__ = "producto_variante"
    id_variante = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    sku = Column(String(40), unique=True, nullable=False)
    talla = Column(String(20))
    color = Column(String(30))
    precio = Column(Float, nullable=False)
    image_url = Column(String(400))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="variantes")

# --- Interacciones ---
class Sesion(Base):
    __tablename__ = "sesion"
    id_sesion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_dispositivo = Column(Integer, default=1)
    inicio = Column(DateTime, default=datetime.utcnow)
    termino = Column(DateTime, nullable=True)
    canal = Column(String(20))  # voz / vision / mixto

    detecciones = relationship("Deteccion", back_populates="sesion")
    consultas_voz = relationship("ConsultaVoz", back_populates="sesion")

class ConsultaVoz(Base):
    __tablename__ = "consulta_voz"
    id_consulta = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"))
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    transcripcion = Column(Text)
    intencion = Column(String(80))
    entidades = Column(Text)   # JSON serializado
    confianza = Column(String(20))
    exito = Column(Boolean, default=False)

    sesion = relationship("Sesion", back_populates="consultas_voz")

class Deteccion(Base):
    __tablename__ = "deteccion"
    id_deteccion = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"))
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    prenda = Column(String(50))
    color = Column(String(30))
    rango_etario = Column(String(20))
    confianza = Column(Float)

    sesion = relationship("Sesion", back_populates="detecciones")

# --- Recomendaciones y Analytics ---
class RecomendacionSesion(Base):
    __tablename__ = "recomendacion_sesion"
    id_recomendacion = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    tipo_recomendacion = Column(String(50), nullable=False)  # categoria, marca, color, personalizada, etc.
    filtros_aplicados = Column(Text)  # JSON con filtros usados
    algoritmo_usado = Column(String(50))  # trending, similar, cross_sell, etc.
    total_productos_recomendados = Column(Integer, default=0)
    tiempo_generacion_ms = Column(Integer)  # Tiempo que tardó en generar las recomendaciones
    
    sesion = relationship("Sesion", back_populates="recomendaciones")
    items_recomendados = relationship("RecomendacionItem", back_populates="recomendacion")

class RecomendacionItem(Base):
    __tablename__ = "recomendacion_item"
    id_item = Column(Integer, primary_key=True, index=True)
    id_recomendacion = Column(Integer, ForeignKey("recomendacion_sesion.id_recomendacion"), nullable=False)
    id_variante = Column(Integer, ForeignKey("producto_variante.id_variante"), nullable=False)
    posicion = Column(Integer, nullable=False)  # Posición en la lista de recomendaciones
    score_recomendacion = Column(Float)  # Score del algoritmo de recomendación
    fue_mostrado = Column(Boolean, default=False)
    fue_clicado = Column(Boolean, default=False)
    tiempo_visualizacion_segundos = Column(Float)  # Tiempo que estuvo visible
    fecha_clic = Column(DateTime)
    
    recomendacion = relationship("RecomendacionSesion", back_populates="items_recomendados")
    variante = relationship("ProductoVariante")

class InteraccionUsuario(Base):
    __tablename__ = "interaccion_usuario"
    id_interaccion = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    tipo_interaccion = Column(String(50), nullable=False)  # view, click, hover, scroll, search, etc.
    id_variante = Column(Integer, ForeignKey("producto_variante.id_variante"), nullable=True)
    metadata_interaccion = Column(Text)  # JSON con datos adicionales
    duracion_segundos = Column(Float)  # Duración de la interacción
    
    sesion = relationship("Sesion", back_populates="interacciones")
    variante = relationship("ProductoVariante")

class MetricasSesion(Base):
    __tablename__ = "metricas_sesion"
    id_metrica = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"), nullable=False)
    fecha_calculo = Column(DateTime, default=datetime.utcnow)
    total_recomendaciones_generadas = Column(Integer, default=0)
    total_productos_mostrados = Column(Integer, default=0)
    total_clics = Column(Integer, default=0)
    tasa_clic = Column(Float)  # CTR = clics / productos mostrados
    tiempo_promedio_visualizacion = Column(Float)
    productos_mas_clicados = Column(Text)  # JSON con top productos
    categorias_mas_populares = Column(Text)  # JSON con top categorías
    conversion_rate = Column(Float)  # Si hay sistema de compras
    
    sesion = relationship("Sesion", back_populates="metricas")

# Actualizar relaciones en Sesion
Sesion.recomendaciones = relationship("RecomendacionSesion", back_populates="sesion")
Sesion.interacciones = relationship("InteraccionUsuario", back_populates="sesion")
Sesion.metricas = relationship("MetricasSesion", back_populates="sesion")

# --- Turnos y Detecciones en Tiempo Real ---
class Turno(Base):
    __tablename__ = "turno"
    id_turno = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=True)
    nombre_turno = Column(String(50))  # matutino, vespertino, nocturno
    estado = Column(String(20), default="activo")  # activo, cerrado
    total_clientes_detectados = Column(Integer, default=0)
    total_detecciones = Column(Integer, default=0)
    
    detecciones_buffer = relationship("DeteccionBuffer", back_populates="turno")
    resumen = relationship("ResumenTurno", back_populates="turno", uselist=False)

class DeteccionBuffer(Base):
    """Buffer temporal para almacenar detecciones en tiempo real antes de consolidar"""
    __tablename__ = "deteccion_buffer"
    id_buffer = Column(Integer, primary_key=True, index=True)
    id_turno = Column(Integer, ForeignKey("turno.id_turno"), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Datos de detección
    persona_detectada = Column(Boolean, default=False)
    rango_edad = Column(String(20))
    estilo_ropa = Column(String(50))
    color_principal = Column(String(30))
    color_secundario = Column(String(30), nullable=True)
    prenda_detectada = Column(String(50))
    accesorio_cabeza = Column(String(50), nullable=True)
    confianza_deteccion = Column(Float)
    
    # Metadata
    motor_deteccion = Column(String(50))  # real_detection_mediapipe, simulated, etc.
    fuente_camara = Column(String(20))  # real, simulated
    procesado = Column(Boolean, default=False)  # Si ya fue procesado en el resumen
    
    turno = relationship("Turno", back_populates="detecciones_buffer")

class ResumenTurno(Base):
    """Resumen consolidado de detecciones por turno"""
    __tablename__ = "resumen_turno"
    id_resumen = Column(Integer, primary_key=True, index=True)
    id_turno = Column(Integer, ForeignKey("turno.id_turno"), nullable=False, unique=True)
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    
    # Estadísticas generales
    total_detecciones = Column(Integer, default=0)
    total_personas_detectadas = Column(Integer, default=0)
    total_prendas_detectadas = Column(Integer, default=0)
    total_accesorios_detectados = Column(Integer, default=0)
    confianza_promedio = Column(Float)
    
    # Demografía
    distribucion_edad = Column(Text)  # JSON: {"18-25": 10, "26-35": 20, ...}
    
    # Preferencias de estilo
    estilos_detectados = Column(Text)  # JSON: {"casual": 50, "formal": 30, ...}
    colores_predominantes = Column(Text)  # JSON: {"azul": 40, "negro": 35, ...}
    prendas_mas_vistas = Column(Text)  # JSON: {"camiseta": 60, "chaqueta": 30, ...}
    accesorios_mas_vistos = Column(Text)  # JSON: {"gorra": 20, "gafas": 15, ...}
    
    # Insights
    perfil_cliente_predominante = Column(Text)  # JSON con el perfil más común
    recomendaciones_inventario = Column(Text)  # JSON con sugerencias de stock
    
    turno = relationship("Turno", back_populates="resumen")

# --- Sistema de Calificaciones ---
class CalificacionRecomendacion(Base):
    """Tabla para calificar las recomendaciones del tótem"""
    __tablename__ = "calificacion_recomendacion"
    
    id_calificacion = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"), nullable=False)
    id_recomendacion = Column(Integer, ForeignKey("recomendacion_sesion.id_recomendacion"), nullable=False)
    calificacion = Column(Integer, nullable=False)  # 1-5 estrellas
    comentario = Column(Text, nullable=True)  # Comentario opcional
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    sesion = relationship("Sesion")
    recomendacion = relationship("RecomendacionSesion")

class CalificacionGrupoRecomendacion(Base):
    """Tabla para calificar grupos de recomendaciones del tótem"""
    __tablename__ = "calificacion_grupo_recomendacion"
    
    id_calificacion_grupo = Column(Integer, primary_key=True, index=True)
    id_sesion = Column(String(36), ForeignKey("sesion.id_sesion"), nullable=False)
    tipo_grupo = Column(String(50), nullable=False)  # categoria, marca, color, estilo, etc.
    nombre_grupo = Column(String(100), nullable=False)  # nombre específico del grupo
    productos_incluidos = Column(Text)  # JSON con IDs de productos incluidos
    calificacion_general = Column(Integer, nullable=False)  # 1-5 estrellas para el grupo completo
    comentario_grupo = Column(Text, nullable=True)  # Comentario sobre el grupo
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    sesion = relationship("Sesion")

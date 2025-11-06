"""
Servicio para gestión de turnos y consolidación de detecciones
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Turno, DeteccionBuffer, ResumenTurno
import json
from typing import Dict, Any, Optional
from collections import Counter


class ShiftManager:
    """Gestor de turnos y detecciones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_current_shift(self) -> Optional[Turno]:
        """Obtiene el turno activo actual"""
        try:
            return self.db.query(Turno).filter(
                Turno.estado == "activo"
            ).first()
        except Exception as e:
            # Tabla no existe o error de BD - modo sin turnos
            return None
    
    def create_shift(self, nombre_turno: str, hora_inicio: datetime = None) -> Turno:
        """
        Crea un nuevo turno
        
        Args:
            nombre_turno: Nombre del turno (matutino, vespertino, nocturno)
            hora_inicio: Hora de inicio (default: ahora)
        """
        if hora_inicio is None:
            hora_inicio = datetime.utcnow()
        
        # Cerrar turnos anteriores activos
        turnos_activos = self.db.query(Turno).filter(Turno.estado == "activo").all()
        for turno in turnos_activos:
            turno.estado = "cerrado"
            turno.hora_fin = hora_inicio
            self.db.commit()
        
        # Crear nuevo turno
        nuevo_turno = Turno(
            fecha=hora_inicio.date(),
            hora_inicio=hora_inicio,
            nombre_turno=nombre_turno,
            estado="activo"
        )
        self.db.add(nuevo_turno)
        self.db.commit()
        self.db.refresh(nuevo_turno)
        
        return nuevo_turno
    
    def close_shift(self, id_turno: int = None) -> Optional[Turno]:
        """
        Cierra un turno y genera su resumen
        
        Args:
            id_turno: ID del turno a cerrar (default: turno activo actual)
        """
        if id_turno:
            turno = self.db.query(Turno).filter(Turno.id_turno == id_turno).first()
        else:
            turno = self.get_current_shift()
        
        if not turno:
            return None
        
        # Cerrar turno
        turno.estado = "cerrado"
        turno.hora_fin = datetime.utcnow()
        
        # Generar resumen
        self.generate_shift_summary(turno.id_turno)
        
        self.db.commit()
        self.db.refresh(turno)
        
        return turno
    
    def store_detection(self, analysis: Dict[str, Any], engine: str = "unknown", 
                       camera_source: str = "unknown") -> Optional[DeteccionBuffer]:
        """
        Almacena una detección en el buffer
        
        Args:
            analysis: Datos del análisis de la detección
            engine: Motor de detección usado
            camera_source: Fuente de la cámara
        
        Returns:
            DeteccionBuffer o None si las tablas no existen
        """
        try:
            # Obtener o crear turno activo
            turno = self.get_current_shift()
            if not turno:
                # Crear turno automáticamente
                hora_actual = datetime.utcnow().hour
                if 6 <= hora_actual < 14:
                    nombre_turno = "matutino"
                elif 14 <= hora_actual < 22:
                    nombre_turno = "vespertino"
                else:
                    nombre_turno = "nocturno"
                turno = self.create_shift(nombre_turno)
            
            # Si aún no hay turno (tabla no existe), salir silenciosamente
            if not turno:
                return None
            
            # Crear registro de detección
            deteccion = DeteccionBuffer(
                id_turno=turno.id_turno,
                persona_detectada=analysis.get('person_detected', False),
                rango_edad=analysis.get('age_range', 'desconocido'),
                estilo_ropa=analysis.get('clothing_style', 'desconocido'),
                color_principal=analysis.get('primary_color', 'desconocido'),
                color_secundario=analysis.get('secondary_color'),
                prenda_detectada=analysis.get('clothing_item', 'desconocido'),
                accesorio_cabeza=analysis.get('head_accessory'),
                confianza_deteccion=analysis.get('detection_confidence', 0.0),
                motor_deteccion=engine,
                fuente_camara=camera_source,
                procesado=False
            )
            
            self.db.add(deteccion)
            
            # Actualizar contadores del turno
            turno.total_detecciones += 1
            if analysis.get('person_detected', False):
                turno.total_clientes_detectados += 1
            
            self.db.commit()
            self.db.refresh(deteccion)
            
            return deteccion
        
        except Exception as e:
            # Tablas no existen o error de BD - modo sin turnos
            print(f"⚠️ Sistema de turnos deshabilitado (tablas no encontradas): {e}")
            return None
    
    def generate_shift_summary(self, id_turno: int) -> Optional[ResumenTurno]:
        """
        Genera un resumen consolidado de todas las detecciones de un turno
        
        Args:
            id_turno: ID del turno
        """
        turno = self.db.query(Turno).filter(Turno.id_turno == id_turno).first()
        if not turno:
            return None
        
        # Obtener todas las detecciones del turno
        detecciones = self.db.query(DeteccionBuffer).filter(
            DeteccionBuffer.id_turno == id_turno,
            DeteccionBuffer.procesado == False
        ).all()
        
        if not detecciones:
            return None
        
        # Estadísticas generales
        total_detecciones = len(detecciones)
        total_personas = sum(1 for d in detecciones if d.persona_detectada)
        total_prendas = sum(1 for d in detecciones if d.prenda_detectada and d.prenda_detectada != 'desconocido')
        total_accesorios = sum(1 for d in detecciones if d.accesorio_cabeza and d.accesorio_cabeza != 'desconocido')
        
        confianzas = [d.confianza_deteccion for d in detecciones if d.confianza_deteccion]
        confianza_promedio = sum(confianzas) / len(confianzas) if confianzas else 0.0
        
        # Distribución de edad
        edades = [d.rango_edad for d in detecciones if d.rango_edad and d.rango_edad != 'desconocido']
        distribucion_edad = dict(Counter(edades))
        
        # Estilos detectados
        estilos = [d.estilo_ropa for d in detecciones if d.estilo_ropa and d.estilo_ropa != 'desconocido']
        estilos_detectados = dict(Counter(estilos))
        
        # Colores predominantes
        colores = [d.color_principal for d in detecciones if d.color_principal and d.color_principal != 'desconocido']
        colores_secundarios = [d.color_secundario for d in detecciones if d.color_secundario and d.color_secundario != 'desconocido']
        todos_colores = colores + colores_secundarios
        colores_predominantes = dict(Counter(todos_colores))
        
        # Prendas más vistas
        prendas = [d.prenda_detectada for d in detecciones if d.prenda_detectada and d.prenda_detectada != 'desconocido']
        prendas_mas_vistas = dict(Counter(prendas))
        
        # Accesorios más vistos
        accesorios = [d.accesorio_cabeza for d in detecciones if d.accesorio_cabeza and d.accesorio_cabeza != 'desconocido']
        accesorios_mas_vistos = dict(Counter(accesorios))
        
        # Perfil cliente predominante
        perfil_predominante = self._calcular_perfil_predominante(
            distribucion_edad, estilos_detectados, colores_predominantes
        )
        
        # Recomendaciones de inventario
        recomendaciones = self._generar_recomendaciones_inventario(
            prendas_mas_vistas, colores_predominantes, distribucion_edad
        )
        
        # Crear o actualizar resumen
        resumen = self.db.query(ResumenTurno).filter(
            ResumenTurno.id_turno == id_turno
        ).first()
        
        if resumen:
            # Actualizar resumen existente
            resumen.fecha_generacion = datetime.utcnow()
            resumen.total_detecciones = total_detecciones
            resumen.total_personas_detectadas = total_personas
            resumen.total_prendas_detectadas = total_prendas
            resumen.total_accesorios_detectados = total_accesorios
            resumen.confianza_promedio = confianza_promedio
            resumen.distribucion_edad = json.dumps(distribucion_edad)
            resumen.estilos_detectados = json.dumps(estilos_detectados)
            resumen.colores_predominantes = json.dumps(colores_predominantes)
            resumen.prendas_mas_vistas = json.dumps(prendas_mas_vistas)
            resumen.accesorios_mas_vistos = json.dumps(accesorios_mas_vistos)
            resumen.perfil_cliente_predominante = json.dumps(perfil_predominante)
            resumen.recomendaciones_inventario = json.dumps(recomendaciones)
        else:
            # Crear nuevo resumen
            resumen = ResumenTurno(
                id_turno=id_turno,
                total_detecciones=total_detecciones,
                total_personas_detectadas=total_personas,
                total_prendas_detectadas=total_prendas,
                total_accesorios_detectados=total_accesorios,
                confianza_promedio=confianza_promedio,
                distribucion_edad=json.dumps(distribucion_edad),
                estilos_detectados=json.dumps(estilos_detectados),
                colores_predominantes=json.dumps(colores_predominantes),
                prendas_mas_vistas=json.dumps(prendas_mas_vistas),
                accesorios_mas_vistos=json.dumps(accesorios_mas_vistos),
                perfil_cliente_predominante=json.dumps(perfil_predominante),
                recomendaciones_inventario=json.dumps(recomendaciones)
            )
            self.db.add(resumen)
        
        # Marcar detecciones como procesadas
        for deteccion in detecciones:
            deteccion.procesado = True
        
        self.db.commit()
        self.db.refresh(resumen)
        
        return resumen
    
    def _calcular_perfil_predominante(self, distribucion_edad: Dict, 
                                     estilos: Dict, colores: Dict) -> Dict[str, Any]:
        """Calcula el perfil de cliente predominante"""
        perfil = {}
        
        # Rango de edad más común
        if distribucion_edad:
            perfil['edad_predominante'] = max(distribucion_edad, key=distribucion_edad.get)
            perfil['porcentaje_edad'] = round(
                distribucion_edad[perfil['edad_predominante']] / sum(distribucion_edad.values()) * 100, 1
            )
        
        # Estilo más común
        if estilos:
            perfil['estilo_predominante'] = max(estilos, key=estilos.get)
            perfil['porcentaje_estilo'] = round(
                estilos[perfil['estilo_predominante']] / sum(estilos.values()) * 100, 1
            )
        
        # Color más común
        if colores:
            perfil['color_predominante'] = max(colores, key=colores.get)
            perfil['porcentaje_color'] = round(
                colores[perfil['color_predominante']] / sum(colores.values()) * 100, 1
            )
        
        return perfil
    
    def _generar_recomendaciones_inventario(self, prendas: Dict, colores: Dict, 
                                           edades: Dict) -> Dict[str, Any]:
        """Genera recomendaciones de inventario basadas en las detecciones"""
        recomendaciones = {
            "prendas_prioritarias": [],
            "colores_prioritarios": [],
            "acciones_sugeridas": []
        }
        
        # Top 3 prendas
        if prendas:
            top_prendas = sorted(prendas.items(), key=lambda x: x[1], reverse=True)[:3]
            recomendaciones["prendas_prioritarias"] = [
                {"prenda": p[0], "demanda": p[1]} for p in top_prendas
            ]
        
        # Top 3 colores
        if colores:
            top_colores = sorted(colores.items(), key=lambda x: x[1], reverse=True)[:3]
            recomendaciones["colores_prioritarios"] = [
                {"color": c[0], "demanda": c[1]} for c in top_colores
            ]
        
        # Acciones sugeridas
        if edades and prendas:
            edad_principal = max(edades, key=edades.get)
            prenda_principal = max(prendas, key=prendas.get)
            
            recomendaciones["acciones_sugeridas"].append(
                f"Aumentar stock de {prenda_principal} para público {edad_principal}"
            )
            
            if colores:
                color_principal = max(colores, key=colores.get)
                recomendaciones["acciones_sugeridas"].append(
                    f"Priorizar compra de productos en color {color_principal}"
                )
        
        return recomendaciones
    
    def get_shift_stats(self, id_turno: int) -> Optional[Dict[str, Any]]:
        """Obtiene estadísticas en tiempo real de un turno"""
        turno = self.db.query(Turno).filter(Turno.id_turno == id_turno).first()
        if not turno:
            return None
        
        resumen = self.db.query(ResumenTurno).filter(
            ResumenTurno.id_turno == id_turno
        ).first()
        
        stats = {
            "turno": {
                "id": turno.id_turno,
                "nombre": turno.nombre_turno,
                "fecha": turno.fecha.isoformat() if turno.fecha else None,
                "hora_inicio": turno.hora_inicio.isoformat() if turno.hora_inicio else None,
                "hora_fin": turno.hora_fin.isoformat() if turno.hora_fin else None,
                "estado": turno.estado,
                "total_detecciones": turno.total_detecciones,
                "total_clientes": turno.total_clientes_detectados
            }
        }
        
        if resumen:
            stats["resumen"] = {
                "personas_detectadas": resumen.total_personas_detectadas,
                "prendas_detectadas": resumen.total_prendas_detectadas,
                "accesorios_detectados": resumen.total_accesorios_detectados,
                "confianza_promedio": round(resumen.confianza_promedio, 2),
                "distribucion_edad": json.loads(resumen.distribucion_edad),
                "estilos_detectados": json.loads(resumen.estilos_detectados),
                "colores_predominantes": json.loads(resumen.colores_predominantes),
                "prendas_mas_vistas": json.loads(resumen.prendas_mas_vistas),
                "accesorios_mas_vistos": json.loads(resumen.accesorios_mas_vistos),
                "perfil_predominante": json.loads(resumen.perfil_cliente_predominante),
                "recomendaciones_inventario": json.loads(resumen.recomendaciones_inventario)
            }
        
        return stats


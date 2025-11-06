#!/usr/bin/env python3
"""
Script para verificar los datos reales en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import get_db
from database.models import RecomendacionSesion, InteraccionUsuario, Deteccion
from sqlalchemy import func
from datetime import datetime, timedelta

def verificar_datos_reales():
    """Verificar qué datos reales hay en la BD"""
    print("🔍 VERIFICANDO DATOS REALES EN LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        # Obtener sesión de BD
        db = next(get_db())
        
        # Verificar tablas
        print("\n📊 CONTEO DE REGISTROS POR TABLA:")
        print("-" * 40)
        
        # Total de sesiones
        total_sesiones = db.query(func.count(RecomendacionSesion.id_sesion)).scalar()
        print(f"   📋 Total Sesiones: {total_sesiones}")
        
        # Total de recomendaciones
        total_recomendaciones = db.query(func.count(RecomendacionSesion.id_recomendacion)).scalar()
        print(f"   🎯 Total Recomendaciones: {total_recomendaciones}")
        
        # Total de interacciones
        total_interacciones = db.query(func.count(InteraccionUsuario.id_interaccion)).scalar()
        print(f"   👆 Total Interacciones: {total_interacciones}")
        
        # Total de detecciones
        total_detecciones = db.query(func.count(Deteccion.id_deteccion)).scalar()
        print(f"   👁️ Total Detecciones: {total_detecciones}")
        
        # Datos del día actual
        today = datetime.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        
        print(f"\n📅 DATOS DEL DÍA ACTUAL ({today}):")
        print("-" * 40)
        
        # Sesiones hoy
        sesiones_hoy = db.query(func.count(func.distinct(RecomendacionSesion.id_sesion))).filter(
            RecomendacionSesion.fecha_hora >= start_of_day
        ).scalar()
        print(f"   📋 Sesiones Hoy: {sesiones_hoy}")
        
        # Recomendaciones hoy
        recomendaciones_hoy = db.query(func.count(RecomendacionSesion.id_recomendacion)).filter(
            RecomendacionSesion.fecha_hora >= start_of_day
        ).scalar()
        print(f"   🎯 Recomendaciones Hoy: {recomendaciones_hoy}")
        
        # Detecciones hoy
        detecciones_hoy = db.query(func.count(Deteccion.id_deteccion)).filter(
            Deteccion.fecha_hora >= start_of_day
        ).scalar()
        print(f"   👁️ Detecciones Hoy: {detecciones_hoy}")
        
        # Clics hoy
        clics_hoy = db.query(func.count(InteraccionUsuario.id_interaccion)).filter(
            InteraccionUsuario.tipo_interaccion == 'click',
            InteraccionUsuario.fecha_hora >= start_of_day
        ).scalar()
        print(f"   👆 Clics Hoy: {clics_hoy}")
        
        # CTR hoy
        ctr_hoy = (clics_hoy / recomendaciones_hoy) if recomendaciones_hoy > 0 else 0.0
        print(f"   📊 CTR Hoy: {ctr_hoy:.2%}")
        
        # Últimas 5 sesiones
        print(f"\n🕒 ÚLTIMAS 5 SESIONES:")
        print("-" * 40)
        ultimas_sesiones = db.query(RecomendacionSesion).order_by(
            RecomendacionSesion.fecha_hora.desc()
        ).limit(5).all()
        
        for i, sesion in enumerate(ultimas_sesiones, 1):
            print(f"   {i}. ID: {sesion.id_sesion} | Producto: {sesion.producto} | Fecha: {sesion.fecha_hora}")
        
        # Top productos más clickeados
        print(f"\n🏆 TOP 5 PRODUCTOS MÁS CLICKEADOS:")
        print("-" * 40)
        top_productos = db.query(
            RecomendacionSesion.producto,
            func.count(InteraccionUsuario.id_interaccion).label('clics')
        ).join(
            InteraccionUsuario, 
            RecomendacionSesion.id_recomendacion == InteraccionUsuario.id_recomendacion
        ).filter(
            InteraccionUsuario.tipo_interaccion == 'click'
        ).group_by(RecomendacionSesion.producto).order_by(
            func.count(InteraccionUsuario.id_interaccion).desc()
        ).limit(5).all()
        
        if top_productos:
            for i, (producto, clics) in enumerate(top_productos, 1):
                print(f"   {i}. {producto}: {clics} clics")
        else:
            print("   ❌ No hay datos de clics disponibles")
        
        # Verificar si hay datos simulados
        print(f"\n🤔 ANÁLISIS DE DATOS:")
        print("-" * 40)
        
        if total_sesiones == 0:
            print("   ⚠️  No hay sesiones en la BD - Los datos del dashboard son simulados")
        elif total_sesiones < 10:
            print("   ⚠️  Pocas sesiones en la BD - Algunos datos pueden ser simulados")
        else:
            print("   ✅ Hay suficientes datos reales en la BD")
        
        if total_interacciones == 0:
            print("   ⚠️  No hay interacciones en la BD - Los clics son simulados")
        else:
            print("   ✅ Hay interacciones reales en la BD")
        
        print(f"\n🎯 CONCLUSIÓN:")
        print("-" * 40)
        if total_sesiones > 0 and total_interacciones > 0:
            print("   ✅ El dashboard muestra datos REALES de tu base de datos")
            print("   📊 Los valores se actualizan porque hay actividad real registrada")
        else:
            print("   ⚠️  El dashboard muestra datos SIMULADOS porque no hay actividad real")
            print("   🔄 Los valores se actualizan por el código JavaScript del dashboard")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
        print("💡 Asegúrate de que el backend esté ejecutándose y la BD esté conectada")

if __name__ == "__main__":
    verificar_datos_reales()

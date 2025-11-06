#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a MySQL
"""
import sqlite3
from database.database import SessionLocal
from database import models
from datetime import datetime
from sqlalchemy import text

def migrate_data():
    """Migrar datos de SQLite a MySQL"""
    
    # Conectar a SQLite
    sqlite_conn = sqlite3.connect('neototem.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Conectar a MySQL
    mysql_db = SessionLocal()
    
    try:
        print("🔄 Migrando datos de SQLite a MySQL...")
        
        # 0. Crear dispositivo por defecto si no existe
        print("🔧 Creando dispositivo por defecto...")
        existing_device = mysql_db.execute(text("SELECT id_dispositivo FROM dispositivo LIMIT 1")).fetchone()
        if not existing_device:
            mysql_db.execute(text("INSERT INTO dispositivo (id_tienda, etiqueta, estado) VALUES (1, 'Totem-Default', 'active')"))
            mysql_db.commit()
            device_id = mysql_db.execute(text("SELECT id_dispositivo FROM dispositivo WHERE etiqueta = 'Totem-Default'")).fetchone()[0]
        else:
            device_id = existing_device[0]
        print(f"✅ Dispositivo ID: {device_id}")
        
        # 1. Migrar sesiones
        print("📝 Migrando sesiones...")
        sqlite_cursor.execute("SELECT * FROM sesion")
        sesiones = sqlite_cursor.fetchall()
        
        for sesion_data in sesiones:
            # Insertar directamente con SQL para incluir id_dispositivo
            mysql_db.execute(text("""
                INSERT INTO sesion (id_sesion, id_dispositivo, inicio, termino, canal, consent) 
                VALUES (:id_sesion, :id_dispositivo, :inicio, :termino, :canal, 1)
                ON DUPLICATE KEY UPDATE 
                inicio=VALUES(inicio), termino=VALUES(termino), canal=VALUES(canal)
            """), {
                'id_sesion': sesion_data[0],
                'id_dispositivo': device_id,
                'inicio': datetime.fromisoformat(sesion_data[1]) if sesion_data[1] else None,
                'termino': datetime.fromisoformat(sesion_data[2]) if sesion_data[2] else None,
                'canal': sesion_data[3]
            })
        
        # 2. Migrar consultas de voz
        print("🎙️ Migrando consultas de voz...")
        sqlite_cursor.execute("SELECT * FROM consulta_voz")
        consultas = sqlite_cursor.fetchall()
        
        for consulta_data in consultas:
            consulta = models.ConsultaVoz(
                id_consulta=consulta_data[0],
                id_sesion=consulta_data[1],
                fecha_hora=datetime.fromisoformat(consulta_data[2]) if consulta_data[2] else None,
                transcripcion=consulta_data[3],
                intencion=consulta_data[4],
                entidades=consulta_data[5],
                confianza=consulta_data[6],
                exito=bool(consulta_data[7]) if len(consulta_data) > 7 and consulta_data[7] is not None else False
            )
            mysql_db.merge(consulta)
        
        # 3. Migrar detecciones (solo las que tienen sesión válida)
        print("👁️ Migrando detecciones...")
        sqlite_cursor.execute("SELECT * FROM deteccion")
        detecciones = sqlite_cursor.fetchall()
        
        # Obtener sesiones válidas
        valid_sessions = mysql_db.execute(text("SELECT id_sesion FROM sesion")).fetchall()
        valid_session_ids = {row[0] for row in valid_sessions}
        
        migrated_count = 0
        for deteccion_data in detecciones:
            if deteccion_data[1] in valid_session_ids:  # Solo migrar si la sesión existe
                deteccion = models.Deteccion(
                    id_deteccion=deteccion_data[0],
                    id_sesion=deteccion_data[1],
                    fecha_hora=datetime.fromisoformat(deteccion_data[2]) if deteccion_data[2] else None,
                    prenda=deteccion_data[3],
                    color=deteccion_data[4],
                    rango_etario=deteccion_data[5],
                    confianza=deteccion_data[6]
                )
                mysql_db.merge(deteccion)
                migrated_count += 1
        
        print(f"✅ Migradas {migrated_count} detecciones de {len(detecciones)} totales")
        
        # Commit todos los cambios
        mysql_db.commit()
        print("✅ Migración completada exitosamente")
        
        # Mostrar estadísticas
        sesiones_count = mysql_db.query(models.Sesion).count()
        consultas_count = mysql_db.query(models.ConsultaVoz).count()
        detecciones_count = mysql_db.query(models.Deteccion).count()
        
        print(f"📊 Datos migrados:")
        print(f"  - Sesiones: {sesiones_count}")
        print(f"  - Consultas de voz: {consultas_count}")
        print(f"  - Detecciones: {detecciones_count}")
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        mysql_db.rollback()
    finally:
        sqlite_conn.close()
        mysql_db.close()

if __name__ == "__main__":
    migrate_data()

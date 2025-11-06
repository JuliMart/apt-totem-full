#!/usr/bin/env python3
"""
Script para crear las tablas de turnos y detecciones en la base de datos
"""
from database.database import engine, SessionLocal
from database.models import Base, Turno, DeteccionBuffer, ResumenTurno
from services.shift_manager import ShiftManager
from datetime import datetime

def create_tables():
    """Crea todas las tablas en la base de datos"""
    print("🔧 Creando tablas de turnos y detecciones...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")

def create_initial_shift():
    """Crea el turno inicial basado en la hora actual"""
    db = SessionLocal()
    try:
        manager = ShiftManager(db)
        
        # Verificar si ya hay un turno activo
        turno_activo = manager.get_current_shift()
        if turno_activo:
            print(f"ℹ️ Ya existe un turno activo: {turno_activo.nombre_turno} (ID: {turno_activo.id_turno})")
            return
        
        # Determinar turno basado en hora actual
        hora_actual = datetime.utcnow().hour
        if 6 <= hora_actual < 14:
            nombre_turno = "matutino"
        elif 14 <= hora_actual < 22:
            nombre_turno = "vespertino"
        else:
            nombre_turno = "nocturno"
        
        # Crear turno
        turno = manager.create_shift(nombre_turno)
        print(f"✅ Turno inicial creado: {nombre_turno} (ID: {turno.id_turno})")
        print(f"   Hora inicio: {turno.hora_inicio}")
        
    except Exception as e:
        print(f"❌ Error creando turno inicial: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando sistema de turnos y detecciones...\n")
    create_tables()
    print()
    create_initial_shift()
    print("\n✅ Migración completada")
    print("\nℹ️ El sistema ahora:")
    print("  - Almacenará detecciones en tiempo real")
    print("  - Generará resúmenes cada hora")
    print("  - Cambiará turnos automáticamente:")
    print("    • Matutino: 6:00 AM")
    print("    • Vespertino: 2:00 PM")
    print("    • Nocturno: 10:00 PM")


"""
Sistema de tareas programadas (cron jobs) para procesar detecciones por turnos
"""
import schedule
import time
import threading
from datetime import datetime, time as dt_time
from sqlalchemy.orm import Session
from database.database import SessionLocal
from services.shift_manager import ShiftManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CronScheduler:
    """Programador de tareas automáticas"""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Inicia el sistema de tareas programadas"""
        if self.running:
            logger.warning("El scheduler ya está corriendo")
            return
        
        logger.info("🕐 Iniciando sistema de tareas programadas...")
        
        # Configurar tareas
        self._setup_jobs()
        
        # Ejecutar en un thread separado
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info("✅ Sistema de tareas programadas activo")
    
    def stop(self):
        """Detiene el sistema de tareas programadas"""
        logger.info("🛑 Deteniendo sistema de tareas programadas...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("✅ Sistema de tareas programadas detenido")
    
    def _setup_jobs(self):
        """Configura las tareas programadas"""
        
        # Generar resumen cada hora (para turnos en curso)
        schedule.every().hour.do(self._generate_hourly_summary)
        
        # Cambio de turno matutino (6:00 AM)
        schedule.every().day.at("06:00").do(
            lambda: self._change_shift("matutino")
        )
        
        # Cambio de turno vespertino (14:00 / 2:00 PM)
        schedule.every().day.at("14:00").do(
            lambda: self._change_shift("vespertino")
        )
        
        # Cambio de turno nocturno (22:00 / 10:00 PM)
        schedule.every().day.at("22:00").do(
            lambda: self._change_shift("nocturno")
        )
        
        # Limpieza de detecciones procesadas (cada día a las 3:00 AM)
        schedule.every().day.at("03:00").do(self._cleanup_old_detections)
        
        logger.info("📋 Tareas programadas configuradas:")
        logger.info("  - Resumen cada hora")
        logger.info("  - Turno matutino: 6:00 AM")
        logger.info("  - Turno vespertino: 2:00 PM")
        logger.info("  - Turno nocturno: 10:00 PM")
        logger.info("  - Limpieza: 3:00 AM")
    
    def _run_scheduler(self):
        """Loop principal del scheduler"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
    
    def _generate_hourly_summary(self):
        """Genera resumen cada hora para el turno actual"""
        logger.info("📊 Generando resumen horario...")
        
        db = SessionLocal()
        try:
            manager = ShiftManager(db)
            turno_actual = manager.get_current_shift()
            
            if turno_actual:
                resumen = manager.generate_shift_summary(turno_actual.id_turno)
                if resumen:
                    logger.info(f"✅ Resumen generado para turno {turno_actual.id_turno}")
                    logger.info(f"  - Total detecciones: {resumen.total_detecciones}")
                    logger.info(f"  - Personas detectadas: {resumen.total_personas_detectadas}")
                else:
                    logger.info(f"ℹ️ No hay detecciones nuevas para procesar")
            else:
                logger.warning("⚠️ No hay turno activo")
        
        except Exception as e:
            logger.error(f"❌ Error generando resumen horario: {e}")
        finally:
            db.close()
    
    def _change_shift(self, nombre_turno: str):
        """Cambia de turno automáticamente"""
        logger.info(f"🔄 Cambiando a turno {nombre_turno}...")
        
        db = SessionLocal()
        try:
            manager = ShiftManager(db)
            
            # Cerrar turno anterior
            turno_anterior = manager.get_current_shift()
            if turno_anterior:
                logger.info(f"📝 Cerrando turno anterior: {turno_anterior.nombre_turno}")
                manager.close_shift(turno_anterior.id_turno)
                logger.info(f"✅ Turno cerrado - Total detecciones: {turno_anterior.total_detecciones}")
            
            # Crear nuevo turno
            nuevo_turno = manager.create_shift(nombre_turno)
            logger.info(f"🆕 Nuevo turno creado: {nombre_turno} (ID: {nuevo_turno.id_turno})")
        
        except Exception as e:
            logger.error(f"❌ Error cambiando turno: {e}")
        finally:
            db.close()
    
    def _cleanup_old_detections(self):
        """Limpia detecciones antiguas ya procesadas (>30 días)"""
        logger.info("🧹 Limpiando detecciones antiguas...")
        
        db = SessionLocal()
        try:
            from database.models import DeteccionBuffer
            from datetime import timedelta
            
            fecha_limite = datetime.utcnow() - timedelta(days=30)
            
            # Eliminar detecciones procesadas antiguas
            detecciones_eliminadas = db.query(DeteccionBuffer).filter(
                DeteccionBuffer.procesado == True,
                DeteccionBuffer.fecha_hora < fecha_limite
            ).delete()
            
            db.commit()
            logger.info(f"✅ Limpieza completada - {detecciones_eliminadas} detecciones eliminadas")
        
        except Exception as e:
            logger.error(f"❌ Error en limpieza: {e}")
            db.rollback()
        finally:
            db.close()


# Instancia global del scheduler
_scheduler = None


def start_cron_jobs():
    """Inicia el sistema de tareas programadas (llamar al iniciar la app)"""
    global _scheduler
    if _scheduler is None:
        _scheduler = CronScheduler()
        _scheduler.start()
    return _scheduler


def stop_cron_jobs():
    """Detiene el sistema de tareas programadas (llamar al cerrar la app)"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
        _scheduler = None


def get_scheduler():
    """Obtiene la instancia del scheduler"""
    return _scheduler


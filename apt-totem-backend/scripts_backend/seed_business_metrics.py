"""
Script para sembrar datos históricos de negocio de forma realista

Uso:
  python -m scripts_backend.seed_business_metrics

Inserta sesiones, recomendaciones, interacciones y detecciones
para los últimos 30 días, si hay pocos datos. No sobrescribe nada,
solo agrega cuando faltan registros para que el dashboard siempre
muestre información representativa por Día/Semana/Mes.
"""

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import (
    Sesion,
    RecomendacionSesion,
    InteraccionUsuario,
    Deteccion,
)

MIN_SESSIONS_PER_DAY = 3
MAX_SESSIONS_PER_DAY = 12

def ensure_day_data(db: Session, day_dt: datetime) -> None:
    """Si el día tiene pocos datos, agrega sesiones, recomendaciones e interacciones."""
    day_start = datetime.combine(day_dt.date(), datetime.min.time())
    day_end = day_start + timedelta(days=1)

    # Contar sesiones existentes ese día
    existing_sessions = (
        db.query(Sesion)
        .filter(Sesion.inicio >= day_start, Sesion.inicio < day_end)
        .count()
    )

    target_sessions = random.randint(MIN_SESSIONS_PER_DAY, MAX_SESSIONS_PER_DAY)
    to_create = max(0, target_sessions - existing_sessions)

    for i in range(to_create):
        start_time = day_start + timedelta(minutes=random.randint(9 * 60, 20 * 60))
        end_time = start_time + timedelta(minutes=random.randint(1, 9))

        sesion = Sesion(
            id_sesion=f"seed_{day_start.strftime('%Y%m%d')}_{i}_{random.randint(1000,9999)}",
            canal=random.choice(["voice", "vision", "tracking"]),
            inicio=start_time,
            termino=end_time,
        )
        db.add(sesion)
        db.flush()

        # Recomendaciones generadas en la sesión (1-5)
        rec_count = random.randint(1, 5)
        for r in range(rec_count):
            rec_time = start_time + timedelta(minutes=random.randint(0, max(1, int((end_time - start_time).seconds / 60))))
            rec = RecomendacionSesion(
                id_sesion=sesion.id_sesion,
                fecha_hora=rec_time,
                tipo_recomendacion=random.choice(["categoria", "marca", "color", "personalizada"]),
                filtros_aplicados="{}",
                algoritmo_usado=random.choice(["trending", "search_engine", "similar", "personalized"]),
                total_productos_recomendados=random.randint(3, 10),
                tiempo_generacion_ms=random.randint(120, 800)
            )
            db.add(rec)

            # Interacciones alrededor de la recomendación
            # Impresiones/vistas de recomendación
            for _ in range(random.randint(1, 3)):
                iv = InteraccionUsuario(
                    id_sesion=sesion.id_sesion,
                    fecha_hora=rec_time + timedelta(seconds=random.randint(5, 90)),
                    tipo_interaccion="recommendation_viewed",
                    id_variante=None,
                    metadata_interaccion=None,
                    duracion_segundos=random.uniform(0.5, 3.0),
                )
                db.add(iv)

            # Clics (tasa de aceptación aproximada 10%–35%)
            if random.random() < random.uniform(0.10, 0.35):
                ic = InteraccionUsuario(
                    id_sesion=sesion.id_sesion,
                    fecha_hora=rec_time + timedelta(seconds=random.randint(15, 180)),
                    tipo_interaccion="click",
                    id_variante=None,
                    metadata_interaccion=None,
                    duracion_segundos=0,
                )
                db.add(ic)

        # Detecciones en la sesión (0–2)
        for _ in range(random.randint(0, 2)):
            det = Deteccion(
                id_sesion=sesion.id_sesion,
                fecha_hora=start_time + timedelta(minutes=random.randint(0, 10)),
                prenda=random.choice(["camiseta", "chaqueta", "pantalon", "gorra", "zapatillas"]),
                color=random.choice(["negro", "azul", "blanco", "rojo", "verde"]),
                rango_etario=random.choice(["18-25", "26-35", "36-45", "46-60"]),
                confianza=random.uniform(0.65, 0.95),
            )
            db.add(det)

    db.commit()


def main():
    db = SessionLocal()
    try:
        today = datetime.now()
        for days_back in range(1, 31):  # últimos 30 días
            day = today - timedelta(days=days_back)
            ensure_day_data(db, day)
        print("✅ Datos históricos sembrados/asegurados correctamente")
    finally:
        db.close()


if __name__ == "__main__":
    main()




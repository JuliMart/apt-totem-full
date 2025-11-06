import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usar MySQL para producción profesional
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/neototem")

# Para SQLite, agregar configuraciones específicas
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Cambiar a True para debug
        connect_args={"check_same_thread": False},  # Necesario para SQLite con FastAPI
        pool_size=20,  # Aumentar pool (default: 5)
        max_overflow=40,  # Aumentar overflow (default: 10)
        pool_timeout=60,  # Aumentar timeout (default: 30)
        pool_recycle=3600,  # Reciclar conexiones cada hora
        pool_pre_ping=True  # Verificar conexión antes de usar
    )
else:
    engine = create_engine(
        DATABASE_URL, 
        echo=False,
        pool_size=20,
        max_overflow=40,
        pool_timeout=60,
        pool_recycle=3600,
        pool_pre_ping=True
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para usar en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

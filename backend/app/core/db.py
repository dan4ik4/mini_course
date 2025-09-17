import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Берём доступы из переменных окружения (.env ты уже сделал)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "app")
DB_USER = os.getenv("DB_USER", "app")
DB_PASS = os.getenv("DB_PASS", "app")

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Движок и фабрика сессий
engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Зависимость для FastAPI: даёт сессию и корректно закрывает её
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URI, pool_pre_ping=True, pool_size=30, max_overflow=120
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Locate the project's data directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database location
DATABASE_PATH = DATA_DIR / "matts_vault.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# Create the database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# Create database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Base class for database models
class Base(DeclarativeBase):
    pass
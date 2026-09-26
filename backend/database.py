#SQLite database and SearchHistory table
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os


# -----------------------------
# DATABASE LOCATION
# -----------------------------

DATABASE_FOLDER = "data"

os.makedirs(
    DATABASE_FOLDER,
    exist_ok=True
)


DATABASE_URL = "sqlite:///data/history.db"

# -----------------------------
# DATABASE ENGINE
# -----------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -----------------------------
# BASE CLASS
# -----------------------------

Base = declarative_base()
# -----------------------------
# SEARCH HISTORY TABLE
# -----------------------------

class SearchHistory(Base):

    __tablename__ = "search_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    query = Column(
        String,
        nullable=False
    )
    timestamp = Column(
        DateTime,
        default=datetime.now
    )

# -----------------------------
# DATABASE SESSION
# -----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------
# CREATE TABLE
# -----------------------------
Base.metadata.create_all(
    bind=engine
)
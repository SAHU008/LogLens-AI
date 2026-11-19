
from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DATABASE_DIR = BASE_DIR / "data"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_DIR / 'loglens_history.db'}"

# Database connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Prediction history table
class PredictionRecord(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    network_traffic_mb = Column(Float, nullable=False)

    prediction = Column(String(20), nullable=False)
    is_anomaly = Column(Boolean, nullable=False)
    anomaly_score = Column(Float, nullable=False)


# Create database tables
def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("LogLens AI database initialized successfully!")

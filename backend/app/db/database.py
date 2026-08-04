"""
Database connection setup using SQLAlchemy.
...
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Explicitly locate backend/.env, regardless of the current working
# directory the process was launched from (this matters because uvicorn
# is often started from the project root, not from inside backend/).
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        f"DATABASE_URL not found. Checked for .env at: {ENV_PATH}"
    )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Yields a database session for use in a request, and guarantees it's
    closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
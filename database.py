import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Railway sets DATABASE_URL directly
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback for local development
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/job_tracker"
    print("WARNING: Using local database (DATABASE_URL not set)")
else:
    print(f"Using database: {SQLALCHEMY_DATABASE_URL[:30]}...")  # Print first 30 chars

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
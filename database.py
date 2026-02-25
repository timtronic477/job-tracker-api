import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Simple debug
print(f"DATABASE_URL from environ: {os.environ.get('DATABASE_URL', 'NOT FOUND')}")

# Get DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/job_tracker"
    print("WARNING: Using local database")
else:
    print(f"Using database: {SQLALCHEMY_DATABASE_URL[:40]}...")

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
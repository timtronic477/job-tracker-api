import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Debug: Print ALL environment variables
print("=== ALL ENVIRONMENT VARIABLES ===")
for key, value in os.environ.items():
    if 'DATABASE' in key or 'PG' in key or 'POSTGRES' in key:
        print(f"{key}: {value[:50] if len(value) > 50 else value}")
print("=================================")

# Try multiple ways to get DATABASE_URL
db_url_1 = os.environ.get("DATABASE_URL")
db_url_2 = os.getenv("DATABASE_URL")

print(f"os.environ.get: {db_url_1}")
print(f"os.getenv: {db_url_2}")

# Railway sets DATABASE_URL directly
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback for local development
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/job_tracker"
    print("WARNING: Using local database (DATABASE_URL not set)")
else:
    print(f"Using database: {SQLALCHEMY_DATABASE_URL[:30]}...")

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
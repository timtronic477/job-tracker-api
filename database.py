import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost/job_tracker"
)

if "localhost" in SQLALCHEMY_DATABASE_URL:
    print("WARNING: Using local database")
else:
    print("Using Railway database")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
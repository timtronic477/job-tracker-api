import os
from database import engine, Base
from models import Application

def init_db():
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

if __name__ == "__main__":
    init_db()
from database import engine, Base
from models import Application

Base.metadata.create_all(bind=engine)

print("Tables Created Successfully")
#Back-end/database/database.py

from sqlalchemy import create_engine
from database.base import Base
from sqlalchemy.orm import sessionmaker
from models.quadras import Quadra
from models.usuarios import User
from models.agendamentos import Agendamento
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Back-end/models/password_reset_tokens.py

from sqlalchemy import Column, Integer, String, DateTime
from database.base import Base
from datetime import datetime, timedelta

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    token = Column(String, unique=True, index=True)
    expiration = Column(DateTime, default=datetime.utcnow() + timedelta(hours=1)) 

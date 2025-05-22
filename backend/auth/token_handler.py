#Back-end/auth/token_handler.py

import secrets
from datetime import datetime, timedelta

def generate_token():
    return secrets.token_urlsafe(32)

def generate_expiration(hours=1):
    return datetime.utcnow() + timedelta(hours=hours)

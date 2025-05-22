#back-end/auth/auth.py

from fastapi.security import HTTPBearer
from fastapi import Depends
from datetime import datetime, timedelta
from schemas.usuarios import UserBase
from fastapi import HTTPException, status
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def token_verifier(token = Depends(HTTPBearer())):
    OAuth2.verify_token(access_token=token.credentials)

def get_current_user_id(token = Depends(HTTPBearer())) -> int:
    payload = OAuth2.verify_token(token.credentials)
    user_id = int(payload.get("sub"))
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: ID não encontrado.",
        )
    return int(user_id)

class OAuth2:
    @staticmethod
    def user_login(user: UserBase, expires_in: int = 30):

            exp = datetime.utcnow() + timedelta(minutes=expires_in)
            
            payload = {
                'sub': str(user.id),
                'exp': exp
            }

            access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            return {
                'access_token': access_token,
                'exp': exp,
                'detail': "Login realizado com sucesso!"
            }
        
    @staticmethod
    def verify_token(access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return data
        except JWTError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de Acesso Inválido!!"
        )
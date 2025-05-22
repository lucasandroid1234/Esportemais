#Back-end/schemas/usuarios.py

from pydantic import BaseModel
import enum

class StatusEnum(str, enum.Enum):
    A = "A" 
    C = "C"

class PermissaoEnum(str, enum.Enum):
    USER = "USER"
    ADM = "ADM"

class UserBase(BaseModel):
    nome: str
    email: str
    cpf: str

class UserCreate(UserBase):
    senha: str

class LoginRequest(BaseModel):
    cpf: str
    senha: str
    
class ResetPasswordRequest(BaseModel):
    cpf: str
    email: str

class ValidatrPasswordRequest(BaseModel):
    token: str
    nova_senha: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
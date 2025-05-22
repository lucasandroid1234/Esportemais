#Back-end/schemas/quadras.py

from pydantic import BaseModel
from enum import Enum
from typing import Optional

class DisponivelEnum(str, Enum):
    S = "S"
    N = "N"

class QuadraBase(BaseModel):
    nome_quadra: str
    endereco: str
    esporte: str
    descricao: Optional[str] = None

    class Config:
        orm_mode = True

class QuadraCreate(QuadraBase):
    pass  

class QuadraUpdate(QuadraBase):
    disponibilidade: DisponivelEnum

    class Config:
        orm_mode = True

class Quadra(QuadraBase):
    ID: int

    class Config:
        orm_mode = True
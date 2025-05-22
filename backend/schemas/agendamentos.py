#Back-end/schemas/agendamentos.py

from pydantic import BaseModel
from datetime import date, time
from enum import Enum


class AgendamentoStatus(str, Enum):
    confirmado = "Confirmado"
    cancelado = "Cancelado"
    concluido = "Concluido"


class AgendamentoBase(BaseModel):
    id_quadra: int
    id_usuario: int
    data: date
    horario_inicio: time
    horario_fim: time

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoDetalhadoResponse(BaseModel):
    nome_quadra: str
    nome_usuario: str
    data: date
    horario_inicio: time
    horario_fim: time


class AgendamentoResponse(AgendamentoBase):
    id_agendamento: int

    class Config:
        orm_mode = True
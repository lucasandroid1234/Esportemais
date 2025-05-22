#Back-end/routers/agendamentos.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from auth.auth import token_verifier, get_current_user_id
from database.database import get_db
from schemas.agendamentos import AgendamentoCreate
from services.agendamentos import AgendamentoService

router = APIRouter(
    prefix="/agendamentos", 
    tags=["Agendamentos"],
    dependencies=[Depends(token_verifier)]
)

@router.post("/agendar-quadra")
async def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return AgendamentoService.criar_agendamento(db=db, agendamento=agendamento, user_id=user_id)

@router.get("/")
def listar_agendamentos(db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return AgendamentoService.listar_agendamentos(db=db, user_id=user_id)

@router.get("/quadra/{id_quadra}")
def listar_agendamentos_por_id_quadra(id_quadra: int, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return AgendamentoService.listar_agendamentos_por_id_quadra(db=db, id_quadra=id_quadra, user_id=user_id)

@router.get("/usuario/{id_usuario}")
def listar_agendamentos_por_id_usuario(id_usuario: int, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return AgendamentoService.listar_agendamentos_por_id_usuario(db=db, id_usuario=id_usuario, user_id=user_id)

@router.put("/cancelar/{id_agendamento}")
def cancelar_agendamento(id_agendamento: int, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return AgendamentoService.cancelar_agendamento(db=db, id_agendamento=id_agendamento, user_id=user_id)

@router.post("/renovar/{id_agendamento}")
def renovar_agendamento(id_agendamento: int, nova_data: date, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return AgendamentoService.renovar_agendamento(db, id_agendamento, nova_data, user_id)
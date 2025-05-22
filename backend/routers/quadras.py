#Back-end/routers/quadras.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from services.quadras import QuadrantService
from schemas.quadras import QuadraCreate, QuadraUpdate
from auth.auth import token_verifier, get_current_user_id
from database.database import get_db

router = APIRouter(
    prefix="/quadras",
    tags=["quadras"],
    dependencies=[Depends(token_verifier)]
)

@router.post("/cadastrar")
async def register_quadrant(quadra: QuadraCreate, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return QuadrantService.create_quadrant_service(db=db, quadra=quadra, user_id=user_id)

@router.get("/listar-quadras")
async def list_quadras(db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return QuadrantService.get_quadrant(db=db,  user_id=user_id)

@router.get("/listar-quadras/{id_quadra}")
async def list_quadra_by_id(id_quadra: int, db: Session = Depends(get_db)):
    return QuadrantService.get_quadrant_by_id(db=db, id_quadra=id_quadra)

@router.get("/horarios-disponiveis")
async def list_available_times(id_quadra: int, data: date, db: Session = Depends(get_db)):
    return QuadrantService.get_available_times(db=db, data=data, id_quadra=id_quadra)

@router.put("/atualizar/{id_quadra}")
async def update_quadrant(id_quadra: int, quadra: QuadraUpdate, db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
    return QuadrantService.update_quadrant(db=db, id_quadra=id_quadra, quadra=quadra, user_id=user_id)
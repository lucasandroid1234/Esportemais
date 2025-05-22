from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from schemas.usuarios import UserCreate, LoginRequest, ResetPasswordRequest, ValidatrPasswordRequest
from services.usuarios import (
    create_user_service,
    login_user_service,
    enviar_email_redefinicao_senha,
    redefinir_senha_com_token
)

router = APIRouter(
    prefix="/usuario",
    tags=["users"],
)

@router.post("/cadastrar")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return await create_user_service(db=db, user=user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login_user(request_form_user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = LoginRequest(
            cpf=request_form_user.username,  # Corrigido para usar username conforme OAuth2
            senha=request_form_user.password
        )
        return await login_user_service(db=db, user=user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/redefinir-senha")
async def solicitar_redefinicao_senha(user: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        return await enviar_email_redefinicao_senha(db=db, user=user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/validar-nova-senha/{token}")
async def confirmar_nova_senha(user: ValidatrPasswordRequest, db: Session = Depends(get_db)):
    try:
        return await redefinir_senha_com_token(db=db, user=user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
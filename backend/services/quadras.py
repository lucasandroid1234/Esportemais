#Back-end/services/quadras.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from datetime import time, timedelta, datetime, date
from schemas.quadras import QuadraCreate
from repository.quadras import QuadrantRepository
from repository.usuarios import UserRepository
from repository.agendamentos import AgendamentoRepository
import re

class QuadrantService:

    @staticmethod
    def validate_quadrant_info(quadra):
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", quadra.nome_quadra):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome da quadra inválido. Deve conter apenas letras."
            )

        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", quadra.esporte):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esporte inválido. Deve conter apenas letras."
            )

    @staticmethod
    def create_quadrant_service(db: Session, quadra: QuadraCreate, user_id: int):

        user = UserRepository.get_role_user(db=db, id_usuario=user_id)
        
        if user.permissao == "USER":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não permissão para acessar este menu!"
            )
        
        if QuadrantRepository.get_quadrant_by_name(db, quadra.nome_quadra):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma quadra com esse nome."
            )

        if QuadrantRepository.get_quadrant_by_address(db, quadra.endereco):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma quadra cadastrada nesse endereço."
            )
        
        try:
        
            result = QuadrantRepository.create_quadrant_repository(db=db, quadra=quadra)

            if result:
                return {
                    "status_code": status.HTTP_201_CREATED,
                    "detail": "Quadra cadastrada com sucesso!"
                }

        except HTTPException:
                raise
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e) 
            )

    @staticmethod
    def update_quadrant(db: Session, id_quadra, quadra, user_id: int):
        
        user = UserRepository.get_role_user(db=db, id_usuario=user_id)
        
        if user.permissao == "USER":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não permissão para acessar este menu!"
            )
        
        quadra_db = QuadrantRepository.get_quadrant_by_id(db=db, id_quadra=id_quadra)
        
        if not quadra_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadra não encontrada."
            )

        if QuadrantRepository.update_quadrant(db=db, quadra=quadra, id_quadra=id_quadra):   
            return {
                "status_code": status.HTTP_200_OK,
                "detail": "Quadra atualizada com sucesso!"
            }
        

    @staticmethod
    def get_quadrant(db: Session, user_id: int):

        user = UserRepository.get_role_user(db=db, id_usuario=user_id)

        if user.permissao == "ADM":
            
            quadras = QuadrantRepository.get_quadrants(db=db)
            
        else:

            quadras = QuadrantRepository.get_quadrants_available(db=db)
        
        if not quadras:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma quadra encontrada."
            )
        
        return {
            "status_code": status.HTTP_200_OK,
            "quadras": quadras
        }

    @staticmethod
    def get_quadrant_by_id(db: Session, id_quadra: int):
        
        quadra = QuadrantRepository.get_quadrant_by_id(db=db, id_quadra=id_quadra)
        
        if not quadra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadra não encontrada."
            )
        
        return {
            "status_code": status.HTTP_200_OK,
            "quadra": quadra
        }   
    
    @staticmethod
    def get_available_times(db: Session, data, id_quadra):
        
        hora_atual = datetime.combine(data, time(8, 0))
        fim_dia = datetime.combine(data, time(22, 0))
        blocos = []

        while hora_atual < fim_dia:
            bloco_inicio = hora_atual.time()
            bloco_fim = (hora_atual + timedelta(hours=1)).time()
            blocos.append((bloco_inicio, bloco_fim))
            hora_atual += timedelta(hours=1)

        agendamentos = AgendamentoRepository.get_agendamentos_by_quandrant_date(db=db, data=data, id_quadra=id_quadra)
        
        blocos_disponiveis = []
        for inicio, fim in blocos:
            conflito = any(
                ag.horario_inicio < fim and ag.horario_fim > inicio
                for ag in agendamentos
            )

            if not conflito:
                blocos_disponiveis.append({
                    "inicio": inicio.strftime("%H:%M"),
                    "fim": fim.strftime("%H:%M")
                }
            )
                
        return blocos_disponiveis
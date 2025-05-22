#Back-end/services/agendamentos.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from schemas.agendamentos import AgendamentoCreate, AgendamentoStatus
from repository.quadras import QuadrantRepository
from repository.usuarios import UserRepository
from repository.agendamentos import AgendamentoRepository
from mails.sendMail import send_email_agendamento, send_email_cancelamento_agendamento
from datetime import datetime, date
now = datetime.now()


class AgendamentoService:

    def validate_agendamento_info(db, agendamento):

        if not QuadrantRepository.get_quadrant_by_id(db, agendamento.id_quadra):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadra não encontrada."
            )
        
        if not UserRepository.get_usuario_by_id(db, agendamento.id_usuario):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        
        if AgendamentoRepository.get_agendamento_by_data_hora(db, agendamento):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um agendamento para essa quadra nesse horário."
            )  
    
        if AgendamentoRepository.get_agendamento_by_id_and_status(db, agendamento.id_usuario, status="confirmado"):
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já possui um agendamento em aberto!"
            )
        
        if agendamento.horario_inicio.hour < 8 or agendamento.horario_fim.hour > 22:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Horário inválido. O agendamento deve ser entre 08:00 e 22:00."
            ) 

        if (agendamento.horario_fim.hour - agendamento.horario_inicio.hour) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Horário inválido. O agendamento deve ser no minímo 1 hora!."
            ) 
        
        horario_inicio = datetime.combine(now.date(), agendamento.horario_inicio)
        if agendamento.data == now.date() and horario_inicio <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível agendar para um horário que já passou no mesmo dia."
            )

    @staticmethod
    def criar_agendamento(db: Session, agendamento, user_id: int): 
         
        user = UserRepository.get_role_user(db=db, id_usuario=user_id)
        
        if agendamento.id_usuario != user_id and user.permissao != "ADM":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não é possível agendar para outro usuário!"
        )

        AgendamentoService.validate_agendamento_info(db, agendamento)

        try:
            result = AgendamentoRepository.create_agendamento_repository(db=db, agendamento=agendamento)
            if result:
                send_email_agendamento(user.email, user.nome, agendamento= AgendamentoRepository.get_agendamento_detalhado_by_id(db=db, id_agendamento=result.id_agendamento))
                return {
                    "status_code": status.HTTP_201_CREATED,
                    "detail": "Agendamento criado com sucesso!",
                    "Agendamento": result
                }
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e) 
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar agendamento: " + str(e)
            )
    
    @staticmethod
    def renovar_agendamento(db: Session, id_agendamento: int, nova_data: date, user_id: int):

        user = UserRepository.get_role_user(db=db, id_usuario=user_id)
        agendamento_antigo = AgendamentoRepository.get_agendamento_by_id(db, id_agendamento)

        if not agendamento_antigo:
            raise HTTPException(status_code=404, detail="Não foi encontrado agendamento para renovar.")

        if agendamento_antigo.status != AgendamentoStatus.concluido:
            raise HTTPException(status_code=400, detail="Apenas agendamentos concluidos podem ser renovados.")

        if agendamento_antigo.id_usuario != user_id and user.permissao == "USER":
            raise HTTPException(status_code=403, detail="Você não tem permissão!")

        novo_agendamento = AgendamentoCreate(
            id_quadra=agendamento_antigo.id_quadra,
            id_usuario=user_id,
            data=nova_data,
            horario_inicio=agendamento_antigo.horario_inicio,
            horario_fim=agendamento_antigo.horario_fim
        )

        AgendamentoService.validate_agendamento_info(db, agendamento=novo_agendamento)

        return AgendamentoRepository.create_agendamento_repository(db=db, agendamento=novo_agendamento)


    @staticmethod
    def listar_agendamentos(db: Session, user_id: int):
        try:
            user = UserRepository.get_role_user(db=db, id_usuario=user_id)
            
            if user.permissao == "ADM":
                agendamentos = AgendamentoRepository.get_agendamentos(db=db)
            
            else:
                agendamentos = AgendamentoRepository.get_agendamento_user(db=db, id_usuario=user.id)

            if not agendamentos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nenhum agendamento encontrado."
                )
            return agendamentos
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar agendamentos: " + str(e)
            )
        
    @staticmethod
    def listar_agendamentos_por_id_quadra(db: Session, id_quadra: int, user_id: int):
        try:

            user = UserRepository.get_role_user(db=db, id_usuario=user_id)
            
            if user.permissao == "ADM":
                agendamentos = AgendamentoRepository.get_agendamento_by_id_quadra(db=db, id_quadra=id_quadra)
            
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Você não permissão para acessar este menu!"
                )

            if not agendamentos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nenhum agendamento encontrado para essa quadra."
                )
            return agendamentos
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar agendamentos: " + str(e)
            )
        
    @staticmethod
    def listar_agendamentos_por_id_usuario(db: Session, id_usuario: int, user_id: int):
        try:
            user = UserRepository.get_role_user(db=db, id_usuario=user_id)
            
            if user.permissao == "ADM":
                agendamentos = AgendamentoRepository.get_agendamento_by_id_usuario(db=db, id_usuario=id_usuario)
            
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Você não permissão para acessar este menu!"
                )

            if not agendamentos:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nenhum agendamento encontrado para esse usuário."
                )
            return agendamentos
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar agendamentos: " + str(e)
            )
        
    @staticmethod
    def cancelar_agendamento(db: Session, id_agendamento: int, user_id: int):
        try:
            user = UserRepository.get_role_user(db=db, id_usuario=user_id)
            agendamento = AgendamentoRepository.get_agendamento_by_id(db=db, id_agendamento=id_agendamento)
            
            if not agendamento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Agendamento não encontrado."
                )

            if agendamento.id_usuario != user_id and user.permissao != "ADM":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Você não tem permissão para cancelar este agendamento!"
                )
            
            if agendamento.status == AgendamentoStatus.cancelado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Agendamento já cancelado!"
                )
            
            if agendamento.status == AgendamentoStatus.concluido:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Não é possível cancelar um Agendamento já concluído!"
                )

            if AgendamentoRepository.cancelar_agendamento(db=db, id_agendamento=id_agendamento):

                send_email_cancelamento_agendamento(user.email, user.nome, agendamento= AgendamentoRepository.get_agendamento_detalhado_by_id(db=db, id_agendamento=id_agendamento))

                return {
                    "status_code": status.HTTP_200_OK,
                    "detail": "Agendamento cancelado com sucesso!"
                }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao cancelar agendamento: " + str(e)
            )
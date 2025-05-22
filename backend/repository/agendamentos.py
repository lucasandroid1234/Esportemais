#Back-end/repositoy/agendamentos.py

from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from models.agendamentos import Agendamento
from models.quadras import Quadra
from models.usuarios import User
from schemas.agendamentos import AgendamentoCreate, AgendamentoDetalhadoResponse, AgendamentoStatus


class AgendamentoRepository:

    @staticmethod
    def create_agendamento_repository(db: Session, agendamento: AgendamentoCreate):

        db_agendamento = Agendamento(
            id_quadra=agendamento.id_quadra,
            id_usuario=agendamento.id_usuario,
            data=agendamento.data,
            horario_inicio=agendamento.horario_inicio,
            horario_fim=agendamento.horario_fim
        )

        try:
            db.add(db_agendamento)
            db.commit()
            db.refresh(db_agendamento)
            return db_agendamento
        except IntegrityError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def cancelar_agendamento(db: Session, id_agendamento: int):
        agendamento = db.query(Agendamento).filter(Agendamento.id_agendamento == id_agendamento).first()
        if agendamento:
            agendamento.status = AgendamentoStatus.cancelado
            db.commit()
            db.refresh(agendamento)
        return agendamento

    @staticmethod
    def get_agendamento_by_data_hora(db: Session, agendamento):
        return db.query(Agendamento).filter(
            Agendamento.data == agendamento.data,
            Agendamento.horario_inicio < agendamento.horario_fim,
            Agendamento.horario_fim > agendamento.horario_inicio,
            Agendamento.id_quadra == agendamento.id_quadra,
            Agendamento.status == AgendamentoStatus.confirmado
        ).first()
    
    @staticmethod
    def get_agendamentos_by_quandrant_date(db: Session, data, id_quadra):
        return db.query(Agendamento).filter(
            Agendamento.id_quadra == id_quadra,
            Agendamento.data == data,
            Agendamento.status == AgendamentoStatus.confirmado
        ).all()
    
    @staticmethod
    def get_agendamentos(db: Session, id_quadra: Optional[int] = None, id_usuario: Optional[int] = None) -> List[AgendamentoDetalhadoResponse]:
        query = db.query(
            Quadra.nome_quadra.label("nome_quadra"),
            User.nome.label("nome_usuario"),
            Agendamento.data,
            Agendamento.horario_inicio,
            Agendamento.horario_fim
        ).join(
            Quadra, Agendamento.id_quadra == Quadra.id
        ).join(
            User, Agendamento.id_usuario == User.id
        )

        if id_quadra:
            query = query.filter(Agendamento.id_quadra == id_quadra)

        if id_usuario:
            query = query.filter(Agendamento.id_usuario == id_usuario)

        result = query.all()

        return [AgendamentoDetalhadoResponse(
            nome_quadra=row[0],
            nome_usuario=row[1],
            data=row[2],
            horario_inicio=row[3],
            horario_fim=row[4]
        ) for row in result]
    
    @staticmethod
    def get_agendamento_by_id(db: Session, id_agendamento: int):
        return db.query(Agendamento).filter(Agendamento.id_agendamento == id_agendamento).first()

    @staticmethod
    def get_agendamento_by_id_quadra(db: Session, id_quadra: int):
        return AgendamentoRepository.get_agendamentos(db, id_quadra=id_quadra)
    
    @staticmethod
    def get_agendamento_by_id_usuario(db: Session, id_usuario: int):
            return AgendamentoRepository.get_agendamentos(db, id_usuario=id_usuario)
    
    @staticmethod
    def get_agendamento_by_id_and_status(db: Session, id_usuario: int, status):
       return db.query(Agendamento).filter(Agendamento.id_usuario == id_usuario, Agendamento.status == status).all()
    
    @staticmethod
    def get_agendamento_user(db: Session, id_usuario: int):
        query = db.query(
            Quadra.nome_quadra.label("nome_quadra"),
            User.nome.label("nome_usuario"),
            Agendamento.data,
            Agendamento.horario_inicio,
            Agendamento.horario_fim
        ).join(
            Quadra, Agendamento.id_quadra == Quadra.id
        ).join(
            User, Agendamento.id_usuario == User.id
        ).filter(
        Agendamento.id_usuario == id_usuario
        ).all()
        
        return [AgendamentoDetalhadoResponse(
            nome_quadra=row[0],
            nome_usuario=row[1],
            data=row[2],
            horario_inicio=row[3],
            horario_fim=row[4]
        ) for row in query]
    
    def get_agendamento_detalhado_by_id(db: Session, id_agendamento: int) -> Optional[AgendamentoDetalhadoResponse]:
        result = db.query(
            Quadra.nome_quadra.label("nome_quadra"),
            User.nome.label("nome_usuario"),
            Agendamento.data,
            Agendamento.horario_inicio,
            Agendamento.horario_fim
        ).join(
            Quadra, Agendamento.id_quadra == Quadra.id
        ).join(
            User, Agendamento.id_usuario == User.id
        ).filter(
            Agendamento.id_agendamento == id_agendamento
        ).first()

        if result:
            return AgendamentoDetalhadoResponse(
                nome_quadra=result[0],
                nome_usuario=result[1],
                data=result[2],
                horario_inicio=result[3],
                horario_fim=result[4]
            )
        return None
        
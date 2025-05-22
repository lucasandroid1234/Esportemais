#Back-end/repository/quadras.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.quadras import Quadra
from schemas.quadras import QuadraCreate, QuadraUpdate, DisponivelEnum

class QuadrantRepository:

    @staticmethod
    def create_quadrant_repository(db: Session, quadra: QuadraCreate):
        db_quadrant= Quadra(nome_quadra=quadra.nome_quadra, endereco=quadra.endereco, esporte=quadra.esporte, descricao=quadra.descricao)

        try:
            db.add(db_quadrant)
            db.commit()
            db.refresh(db_quadrant)
            return db_quadrant
        except IntegrityError as e:
            db.rollback()
            raise e

    @staticmethod
    def update_quadrant(db: Session, quadra: QuadraUpdate, id_quadra: int):
        db_quadrant = QuadrantRepository.get_quadrant_by_id(db=db, id_quadra=id_quadra)
        
        try:

            db_quadrant.nome_quadra = quadra.nome_quadra
            db_quadrant.endereco = quadra.endereco
            db_quadrant.esporte = quadra.esporte
            db_quadrant.descricao = quadra.descricao
            db_quadrant.disponibilidade = quadra.disponibilidade
            db.commit()
            db.refresh(db_quadrant)
            return db_quadrant
        except IntegrityError as e:
            db.rollback()
            raise e
    @staticmethod   
    def get_quadrant_by_name(db: Session, nome_quadra: str):
        return db.query(Quadra).filter(Quadra.nome_quadra == nome_quadra).first()
    
    @staticmethod 
    def get_quadrant_by_address(db: Session, endereco: str):
        return db.query(Quadra).filter(Quadra.endereco == endereco).first()
    
    @staticmethod 
    def get_quadrant_by_id(db: Session, id_quadra: int):
        return db.query(Quadra).filter(Quadra.id == id_quadra).first()
    
    @staticmethod
    def get_quadrants(db: Session):
        return db.query(Quadra).all()
    
    @staticmethod
    def get_quadrants_available(db: Session):
        return db.query(Quadra).filter(Quadra.disponibilidade == DisponivelEnum.S).all()
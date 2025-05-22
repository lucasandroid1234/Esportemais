#Back-end/repository/usuarios.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.usuarios import User
from models.password_reset_tokens import PasswordResetToken
from schemas.usuarios import UserCreate

class UserRepository:
    @staticmethod
    def create_user_repository(db: Session, user: UserCreate):
        db_user = User(email=user.email, cpf=user.cpf, nome=user.nome, senha=user.senha)
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            raise e

    @staticmethod
    def get_usuario_by_id(db: Session, usuario_id: int):
        return db.query(User).filter(User.id == usuario_id).first()   

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_cpf(db: Session, cpf: str):
        return db.query(User).filter(User.cpf == cpf).first()
    
    def get_user_by_email_cpf(db, user: User):
        return db.query(User).filter(User.email == user.email, User.cpf == user.cpf).first()
    
    @staticmethod
    def update_user_password(db: Session, user_db):

        try:
            db.commit()
            db.refresh(user_db)
            return user_db
        except IntegrityError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_role_user(db: Session, id_usuario: int):
        return db.query(User).filter(User.id == id_usuario).first()

    @staticmethod
    def save_token(db, token, email, expiration):
        db_token = PasswordResetToken(token=token, email=email, expiration=expiration)
        db.add(db_token)
        db.commit()

    @staticmethod
    def get_token_record(db, token):
        return db.query(PasswordResetToken).filter_by(token=token).first()

    @staticmethod
    def invalidate_token(db, token_record):
        db.delete(token_record)
        db.commit()
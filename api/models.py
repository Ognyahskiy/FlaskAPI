import sqlalchemy as db
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token, create_refresh_token
from passlib.hash import bcrypt
from api.main import Base, session
from datetime import timedelta


class Resume(Base):  # создание анкеты
    __tablename__ = 'resume'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    full_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(128), nullable=True)


class User(Base):  # создаем таблицу с данными пользователей для входа
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    resumes = relationship('Resume', backref='user', lazy=True)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_access_token(self):
        access_token = create_access_token(identity=self.id, expires_delta=timedelta(hours=15))
        return access_token

    def get_refresh_token(self):
        refresh_token = create_refresh_token(identity=self.id,expires_delta=timedelta(days=2))
        return refresh_token

    @classmethod
    def autenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user

import sqlalchemy as db
from api.main import Base


class Teach(Base):  # создание таблицы
    __tablename__ = 'teach'
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)

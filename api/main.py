from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from api.config import Config


app = Flask(__name__)
app.config.from_object(Config)  # извлекаем данные из файла config.py

client = app.test_client()
# инициализируем связь с базой данных
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/flaskapi")

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
jwt = JWTManager(app)
from api.models import *  # импортируем таблицу
Base.metadata.create_all(bind=engine)


@app.route('/file', methods=['GET'], endpoint='get_list')  # метод получения данных
@jwt_required
def get_list():
    resume_id = get_jwt_identity()
    resume = Resume.query.filter(Resume.resume_id == resume_id).all()
    serialized = []
    for resume in resume:
        serialized.append({'id': resume.id,
                           'user_id': resume.resume_id,
                           'full_name': resume.full_name,
                           'age': resume.age,
                           'description': resume.description})
    return jsonify(serialized)


@app.route('/file', methods=["POST"], endpoint='update_list')  # метод ввода данных
@jwt_required
def update_list():
    resume_id = get_jwt_identity()
    new_one = Resume(resume_id=resume_id, **request.json)
    session.add(new_one)
    session.commit()
    serialized = {'id': new_one.id,
                  'user_id': new_one.resume_id,
                  'full_name': new_one.full_name,
                  'age': new_one.age,
                  'description': new_one.description}
    return jsonify(serialized)


@app.route("/file/<int:file_id>", methods=['PUT'], endpoint='update_file')  # метод внесения измнений в данные
@jwt_required
def update_file(file_id):
    resume_id = get_jwt_identity()
    item = Resume.query.filter(Resume.id == file_id,
                               Resume.resume_id == resume_id).first()
    params = request.json
    if not item:
        return {'message': 'No files with this id'}
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {'id': item.id,
                  'user_id': item.resume_id,
                  'full_name': item.full_name,
                  'age': item.age,
                  'description': item.description}
    return serialized


@app.route('/file/<int:file_id>', methods=['DELETE'], endpoint='delete_file')  # метод удаления данных
@jwt_required
def delete_file(file_id):
    resume_id = get_jwt_identity()
    item = Resume.query.filter(Resume.id == file_id,
                               Resume.resume_id == resume_id).first()
    if not item:
        return {'message': 'No files with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/register', methods=['POST'], endpoint='register')  # метод регистрации пользователя
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    access_token = user.get_access_token()
    refresh_token = user.get_refresh_token()
    return {'access_token': access_token, 'refresh token': refresh_token}


@app.route('/login', methods=['POST'], endpoint='login')  # метод авторизации пользователя
def login():
    params = request.json
    user = User.autenticate(**params)
    access_token = user.get_access_token()
    refresh_token = user.get_refresh_token()
    return {'access_token': access_token, 'refresh token': refresh_token}


@app.route('/refresh', methods=['POST'], endpoint='refresh')  # метод обновления jwt-токена
@jwt_required(refresh=True)
def refresh():
    resume_id = get_jwt_identity()
    access_token = create_access_token(identity=resume_id)
    return jsonify(access_token=access_token)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

import random
from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from api.config import Config
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)  # извлекаем данные из файла config.py

client = app.test_client()

db_username = os.getenv('POSTGRES_USERNAME')
db_password = os.getenv('POSTGRES_PASSWORD')
db_url = os.getenv('POSTGRES_URL')
# инициализируем связь с базой данных
engine = create_engine(f"postgresql+psycopg2://{db_username}:{db_password}@{db_url}/flaskapi")

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
jwt = JWTManager(app)
from api.models import *  # импортируем таблицу
Base.metadata.create_all(bind=engine)


@app.route('/profile', methods=['GET'], endpoint='get_profile_data')  # метод получения данных
@jwt_required()
def get_profile_data():
    data_id = get_jwt_identity()
    data = user_data.query.filter(user_data.data_id == data_id).all()
    serialized = []
    for data in data:
        serialized.append({'id': data.id,
                           'user_id': data.data_id,
                           'full_name': data.full_name,
                           'age': data.age,
                           'description': data.description})
    return jsonify(serialized)


@app.route('/chat/<int:profile_id>', methods=["POST"], endpoint='send_message')
@jwt_required()
def send_message(profile_id):
    data_id = get_jwt_identity()
    item = user_data.query.filter(user_data.id == profile_id,
                                  user_data.data_id == data_id).first()
    params = request.json
    # Как получить параметры в эту функцию с фронта?



@app.route('/profile', methods=["POST"], endpoint='add_profile')  # метод ввода данных
@jwt_required()
def add_profile():
    data_id = get_jwt_identity()
    new_one = user_data(data_id=data_id, **request.json)
    session.add(new_one)
    session.commit()
    serialized = {'id': new_one.id,
                  'user_id': new_one.data_id,
                  'full_name': new_one.full_name,
                  'age': new_one.age,
                  'description': new_one.description}
    return jsonify(serialized)


@app.route("/profile/<int:profile_id>", methods=['PUT'], endpoint='update_profile_data')  # метод внесения измнений в данные
@jwt_required()
def update_profile_data(profile_id):
    data_id = get_jwt_identity()
    item = user_data.query.filter(user_data.id == profile_id,
                                  user_data.data_id == data_id).first()
    params = request.json
    if not item:
        return {'message': 'No profiles with this id'}
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {'id': item.id,
                  'user_id': item.data_id,
                  'full_name': item.full_name,
                  'age': item.age,
                  'description': item.description}
    return serialized


@app.route('/profile/<int:profile_id>', methods=['DELETE'], endpoint='delete_profile')  # метод удаления данных
@jwt_required()
def delete_profile(profile_id):
    data_id = get_jwt_identity()
    item = user_data.query.filter(user_data.id == profile_id,
                                  user_data.data_id == data_id).first()
    if not item:
        return {'message': 'No files with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


# достаем 5 карточек из бд
@app.route('/cards', methods=['GET'], endpoint='get_cards')
@jwt_required()
def ger_cards():
    data = user_data.query.all()
    serialized = []
    for data in data:
        serialized.append({'full_name': data.full_name,
                           'age': data.age,
                           'description': data.description})
    rnd_crd = []
    for _ in range(1000):
        if len(rnd_crd) == 5:
            break
        rnd_card = random.choice(serialized)
        if rnd_card in rnd_crd:
            pass
        else:
            rnd_crd.append(rnd_card)
    return jsonify(rnd_crd)


@app.route('/register', methods=['POST'], endpoint='register')  # метод регистрации пользователя
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    access_token = user.get_access_token()
    refresh_token = user.get_refresh_token()
    return {'access_token': access_token, 'refresh token': refresh_token}


@app.route('/login', methods=['GET', 'POST'], endpoint='login')  # метод авторизации пользователя
def login():
    params = request.json
    try:
        item = User.query.filter(User.email == params['email']).first()
        crutch = {'id': item.id, 'username': item.username, 'email': item.email, 'password': item.password}
    except AttributeError:
        pass
    user = User.autenticate(**params)
    access_token = user.get_access_token()
    refresh_token = user.get_refresh_token()
    return {'access_token': access_token, 'refresh token': refresh_token, 'username': crutch['username']}


@app.route('/delete', methods=['DELETE'], endpoint='delete_user')  # удаление пользователя
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    item = User.query.filter(User.id == user_id).first()
    if not item:
        return {'message': 'User alredy deleted'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/like', methods=['POST'], endpoint='like_card')
@jwt_required()
def like_card():
        user_id = get_jwt_identity()
        likes_id = sympathy(user_id=user_id, **request.json)
        session.add(likes_id)
        session.commit()
        serialized = {'id': likes_id.id,
                      'user_id': likes_id.user_id,
                      'likes_id': likes_id.likes_id}
        return jsonify(serialized)



@app.route('/refresh', methods=['POST'], endpoint='refresh')  # метод обновления jwt-токена
@jwt_required(refresh=True)
def refresh():
    profile_id = get_jwt_identity()
    access_token = create_access_token(identity=profile_id)
    refresh_token= create_refresh_token(identity=profile_id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# 1)Реализовать лайк\бан систему(пока не придумал)
# 2)Написать чат человек-женщина


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine


app = Flask(__name__)

client = app.test_client()
# инициализируем связь с базой данных
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/flaskapi")

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
from api.models import *  # импортируем таблицу


@app.route('/file', methods=['GET'])  # метод получения данных
def get_list():
    teach = Teach.query.all()
    serialized = []
    for teach in teach:
        serialized.append({'id': teach.id, 'username': teach.Username, 'email': teach.email})
    return jsonify(serialized)


@app.route('/file', methods=["POST"])  # метод ввода данных
def updste_list():
    new_one = Teach(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {'id': new_one.id, 'username': new_one.Username, 'email': new_one.email}

    return jsonify(serialized)


@app.route("/file/<int:file_id>", methods=['PUT'])  # метод внесения измнений в данные
def update_file(file_id):
    item = Teach.query.filter(Teach.id == file_id).first()
    params = request.json
    if not item:
        return {'message': 'No files with this id'}
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'Username': item.Username,
        "email": item.email
    }
    return serialized


@app.route('/file/<int:file_id>', methods=['DELETE'])  # метод удаления данных
def delete_file(file_id):
    item = Teach.query.filter(Teach.id == file_id).first()
    if not item:
        return {'message': 'No files with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


'''@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()'''

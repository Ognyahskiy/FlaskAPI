from api.main import app, client
from api.models import Teach


def test_get():
    res = client.get("/file")
    assert res.status_code == 200

    assert len(res.get_json()) == len(Teach.query.all())
    assert res.get_json()[0]['id'] == 2


def test_post():
    data = {
        'Username': 'Asker',
        'email': 'example@box.ru'
    }

    res = client.post('/file', json=data)

    assert res.status_code == 200


def test_put():
    res = client.put('/file/3', json={'Username': 'UPD'})
    assert res.status_code == 200
    assert Teach.query.get(3).Username == 'UPD'


def test_delete():
    res = client.delete('/file/4')

    assert res.status_code == 204
    assert Teach.query.get(1) is None

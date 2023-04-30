from api.main import app, client
from api.models import Resume


def test_get():
    res = client.get("/file")
    assert res.status_code == 200

    assert len(res.get_json()) == len(Resume.query.all())
    assert res.get_json()[0]['id'] == 2


def test_post():
    data = {'full_name': 'Asker',
            'age': '0',
            'description': 'help me'}

    res = client.post('/file', json=data)

    assert res.status_code == 200


def test_put():
    res = client.put('/file/1', json={'full_name': 'UPD'})
    assert res.status_code == 200
    assert Resume.query.get(1).full_name == 'UPD'


def test_delete():
    res = client.delete('/file/1')

    assert res.status_code == 204
    assert Resume.query.get(1) is None

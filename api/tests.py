from api.main import app, client
from api.models import user_data, User, sympathy


'''def test_like_card():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    res = client.get('/cards', headers={'Authorization': f'Bearer {access_token}'})
    print(res.get_json())

    assert like.status_code == 200'''


def test_register():
    reg = client.post('/register', json={'username': 'TEST', 'email': 'TEST', 'password': 'TEST'})

    assert reg.status_code == 200


def test_login():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    assert log.status_code == 200


def test_get_profile_list():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    res = client.get("/profile", headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 200


def test_get_cards():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    res = client.get('/cards', headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 200
    assert len(res.get_json()) <= 5


def test_add_profile():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    data = {'id': '1',
            'full_name': 'TEST',
            'age': '0',
            'description': 'TEST'}

    res = client.post('/profile', json=data, headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 200


def test_update_profile():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    res = client.put('/profile/1', json={'full_name': 'UPD'}, headers={'Authorization': f'Bearer {access_token}'})
    assert res.status_code == 200
    assert user_data.query.get(1).full_name == 'UPD'


def test_delete_file():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    res = client.delete('/profile/1', headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 204
    assert user_data.query.get(1) is None


def test_delete_user():
    log = client.post('/login', json={'email': 'TEST', 'password': 'TEST'})
    token = log.get_json()
    access_token = token['access_token']
    delete = client.delete('/delete', headers={'Authorization': f'Bearer {access_token}'})

    assert delete.status_code == 204

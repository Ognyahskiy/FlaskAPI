from models import Teach

v = Teach.query.all()
vi = Teach(Username='Asker', email='example@box.ru')


def commt():
    from main import session
    session.add(vi)
    session.commit()

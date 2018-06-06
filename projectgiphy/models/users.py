from projectgiphy import app
from projectgiphy.utilities.db import Users, Aux

def get_users():
    aux = Aux()
    return aux.get_users()

def create_user(name, email, id, picture):
    user = Users(username=name, email=email, password=id, status='active', avatar=picture)
    if not user.get_user(name):
        user.add()
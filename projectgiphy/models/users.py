from projectgiphy import app
from projectgiphy.utilities.db import Users, Aux

def get_users():
    """ Abstracted get_all_users call

    Args:
        None
    Returns:
        dict: Dictionary list of all users that have been created
    """
    aux = Aux()
    return aux.get_users()

def create_user(name, email, id, picture):
    """ Creates a user object provided by Google oAuth

    Args:
        name (str): Username
        email (str): Email address of the user
        id (str): Temp placeholder for password since we dont authenticate
        picture (str): Google stored user avatar from oAuth
    Returns:
        None
    """
    user = Users(username=name, email=email, password=id, status='active', avatar=picture)
    if not user.get_user(name):
        user.add()
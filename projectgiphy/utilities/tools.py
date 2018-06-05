import jwt
from projectgiphy import app

def encrypt(key, string):
    secret = app.secret_key
    return jwt.encode({key: string}, secret, algorithm='HS256')

def decrypt(encrypted_string):
    secret = app.secret_key
    return jwt.decode(encrypted_string, secret, algorithms=['HS256'])
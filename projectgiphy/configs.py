import os
# Constants
DEBUG = True
SECRET_KEY = 'SuperSecretProjectGiphyKey'
DATABASE_URI = 'pg.db'
GOOGLE_LOGIN_CLIENT_ID = os.environ.get('GOOGLE_LOGIN_CLIENT_ID')
GOOGLE_LOGIN_CLIENT_SECRET = os.environ.get('GOOGLE_LOGIN_CLIENT_SECRET')
GOOGLE_LOGIN_REDIRECT_URI = 'http://localhost:5000/gCallback'
GOOGLE_LOGIN_SCOPES = 'https://www.googleapis.com/auth/userinfo.email'
GIPHY_KEY = os.environ.get('GIPHY_KEY')
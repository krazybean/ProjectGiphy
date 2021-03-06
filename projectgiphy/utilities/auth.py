from flask import jsonify, url_for, redirect, session, request
from flask_oauthlib.client import OAuth
from projectgiphy import app

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_LOGIN_CLIENT_ID'),
    consumer_secret=app.config.get('GOOGLE_LOGIN_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


from flask import jsonify, url_for, redirect, session, request, render_template
from flask_oauthlib.client import OAuth
from functools import wraps
from projectgiphy import app
from projectgiphy.models import users, giphy
from projectgiphy.utilities import auth

google = auth.google
oauth = OAuth(app)

# oAuth Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('google_token'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))

# Webpage Routes
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                           picture=session.get('picture'))

# API Routes
@app.route('/api/v1/users')
@login_required
def api_user_list():
    all_users = users.get_users()
    return jsonify(all_users)

@app.route('/api/v1/giphy/search/<string>')
@login_required
def api_search_giphy(string):
    offset = request.args.get('offset')
    search_results = giphy.search(string, offset)
    return jsonify(search_results)


# Auth Routes
@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return google.authorize(callback=url_for('authorized', _external=True), prompt='consent')
    # return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if not resp:
        return 'Access denied'
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    name = me.data['name']
    email = me.data['email']
    id = me.data['id']
    picture = me.data.get('picture')
    session['username'] = name
    session['email'] = email
    session['picture'] = picture
    users.create_user(name, email, id, picture)
    return redirect(url_for('dashboard'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
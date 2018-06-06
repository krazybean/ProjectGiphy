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
    """ 
    Login decorator used for validating the session existence
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('google_token'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """
    Base landing route which gets kicked to oAuth
    """
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))

# Webpage Routes
@app.route('/dashboard')
def dashboard():
    """
    Main dashboard panel where actions are originated
    """
    return render_template('dashboard.html',
                           picture=session.get('picture'))

# API Routes
@app.route('/api/v1/users')
@login_required
def api_user_list():
    """
    API route for listing all users created
    """
    all_users = users.get_users()
    return jsonify(all_users)

@app.route('/api/v1/giphy/search/<string>')
@login_required
def api_search_giphy(string):
    """
    API route for searching for giphy images
    """
    offset = request.args.get('offset')
    search_results = giphy.search(string, offset)
    return jsonify(search_results)


# Auth Routes
@app.route('/login')
def login():
    """
    Login route for redirection of authentication
    """
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    """
    Logout and termination of session
    """
    session.pop('google_token', None)
    return google.authorize(callback=url_for('authorized', _external=True), prompt='consent')
    # return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    """
    Callback from oAuth for session setup and potential user creation
    """
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
    """
    google session getter
    """
    return session.get('google_token')
from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for
from flask_micropub import MicropubClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super secret key'
micropub = MicropubClient(app, 'http://localhost:5000')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        for attr in ['me', 'endpoint', 'access_token']:
           if (session.get("_micropub_{}".format(attr)) is None):
                return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.jinja2')

@app.route('/authorize')
def authorize():
    return micropub.authorize(
        request.args.get('me'), next_url=url_for('index'),
        scope=request.args.get('scope'))

@app.route('/micropub-callback')
@micropub.authorized_handler
def micropub_callback(resp):
    session['_micropub_me'] = resp.me
    session['_micropub_endpoint'] = resp.micropub_endpoint
    session['_micropub_access_token'] = resp.access_token
    return redirect(url_for('new_event'))

@app.route('/new')
@login_required
def new_event():
    me = session.get('_micropub_me')
    return render_template('new.jinja2', me=me)

if __name__ == '__main__':
    app.run(debug=True)

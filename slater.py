from functools import wraps
from flask import Flask, redirect, request, session, url_for
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
    return """
    <!DOCTYPE html>
    <html>
      <body>
        <form action="/authorize" method="GET">
          <input type="text" name="me" placeholder="http://example.com" />
          <input type="hidden" name="scope" value="post" />
          <button type="submit">Sign In</button>
        </form>
      </body>
    </html>
    """

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
    endpoint = session.get('_micropub_endpoint')
    access_token = session.get('_micropub_access_token')
    return """
    <!DOCTYPE html>
    <html>
      <body>
        <p>Posting as {}</p>
        <form method="POST" action="{}" enctype="multipart/form-data">
          <input type="hidden" name="access_token" value="{}" />
          <input type="hidden" name="h" value="event" />
          <div><label for="name">Event Name</label><input type="text" name="name" /></div>
          <!-- TODO: date/time picker w/ TZ -->
          <div><label for="start">Start Date/Time</label><input type="text" name="start" placeholder="2016-12-06 19:30-05:00" /></div>
          <!-- TODO: date/time picker w/ TZ -->
          <div><label for="end">End Date/Time</label><input type="text" name="end" placeholder="2016-12-06 21:30-05:00" /></div>
          <!-- TODO: venue picker -->
          <div><label for="location">Location</label><input type="text" name="location" /></div>
          <!-- TODO: split on commas, strip whitespace, make into category[] on submit -->
          <div><label for="category">Categories</label><input type="text" name="category" /></div>
          <div><label for="photo">Poster Image</label><input type="file" name="photo" /></div>
          <div><label for="content">Description</label><div><textarea name="content"></textarea></div></div>
          <div><input type="submit" value="Create Event" /></div>
        </form>
      </body>
    </html>
    """.format(me, endpoint, access_token)


if __name__ == '__main__':
    app.run(debug=True)

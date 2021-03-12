# Timelines API
# CPSC 449: Project 2
# Creators: Stephen Lee
# Date: 3/12/21
#

# imports
#
import sys
import textwrap
import sqlite3

import bottle
from bottle import get, post, error, abort, request, response, HTTPResponse
from bottle.ext import sqlite

# Set up app and plugins
#
app = bottle.default_app()
app.config.load_config('./etc/timelines.ini')

plugin = sqlite.Plugin(app.config['sqlite.dbfile'])
app.install(plugin)

# Return errors in JSON
#
def json_error_handler(res):
    if res.content_type == 'application/json':
        return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
        res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'error': res.body})


app.default_error_handler = json_error_handler

# Disable warnings produced by Bottle 0.12.19.
#
#  1. Deprecation warnings for bottle_sqlite
#  2. Resource warnings when reloader=True
#
if not sys.warnoptions:
    import warnings
    for warning in [DeprecationWarning, ResourceWarning]:
        warnings.simplefilter('ignore', warning)


# Simplify DB access
#
def query(db, sql, args=(), one=False):
    cur = db.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
          for idx, value in enumerate(row))
          for row in cur.fetchall()]
    cur.close()

    return (rv[0] if rv else None) if one else rv


def execute(db, sql, args=()):
    cur = db.execute(sql, args)
    id = cur.lastrowid
    cur.close()

    return id


# Routes
#
# Home Page
#
@get('/')
def home():
    return textwrap.dedent('''
        <h1>Timelines API</h1>
    ''')

# Post a tweet
#
@post('/timeline/')
def post_tweet(db):
    tweet = request.json

    if not tweet:
        abort(400)

    posted_fields = tweet.keys()
    required_fields = {'author', 'text'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        timelines['id'] = execute(db, '''
            INSERT INTO timelines(author, text)
            VALUES(:author, :text)
            ''', tweet)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/timeline/{timelines['id']}")
    return tweet

# Get Public Timeline
#
@get('/timeline/public/')
def public_timeline(db):
    ptl = query(db, 'SELECT * FROM timelines ORDER BY time DESC LIMIT 25') 

    if not ptl:
        abort(400)

    return ptl

# Get User Timeline
#
@get('/timeline/user/<username>')
def user_timeline(db):
    # check if username exists in users table
    user = query(db, 'SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
    if not user:
        abort(404)

    # get the user timeline
    utl = query(db, 'SELECT * FROM timelines WHERE author = ? ORDER BY time DESC LIMIT 25', [username])

    if not utl:
        abort(400)

    return utl

# Get Home Timeline
#
@get('/timeline/home/<username>')
def user_timeline(db):
    # check if username exists in users table
    user = query(db, 'SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
    if not user:
        abort(404)
    
    # get followers
    qlist = query(db, 'SELECT usernameToFollow FROM followers WHERE username = ?', [username])
    qlist.append(username)

    utl = query(db, 'SELECT * FROM timelines WHERE author IN ({seq}) ORDER BY time DESC LIMIT 25'.format(seq=','.join(['?']*len(qlist))), qlist)

    if not utl:
        abort(400)

    return utl




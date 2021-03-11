# Users API
# CPSC 449: Project 2
# Creators: Stephen Lee
# Date: 3/12/21
#

# imports
#
import sys
import textwrap
import logging.config
import sqlite3

import bottle
from bottle import get, post, error, abort, request, response, HTTPResponse
from bottle.ext import sqlite

# Set up app, plugins, and logging
#
app = bottle.default_app()
app.config.load_config('./etc/api.ini')

plugin = sqlite.Plugin(app.config['sqlite.dbfile'])
app.install(plugin)

logging.config.fileConfig(app.config['logging.config'])


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
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
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
        <h1>Project 2: Users API</h1>
    ''')

# Get all users
#
@get('/users/')
def users(db):
    all_users = query(db, 'SELECT * FROM users;')

    return {'users': all_users}

# Search for a specific user
# Can only search by username or email
#
@get('/users')
def search(db):
    sql = 'SELECT * FROM users'

    columns = []
    values = []

    for column in ['username', 'email']:
        if column in request.query:
            columns.append(column)
            values.append(request.query[column])

    if columns:
        sql += ' WHERE '
        sql += ' AND '.join([f'{column} = ?' for column in columns])

    logging.debug(sql)
    users = query(db, sql, values)

    return {'users': users}

# Create a new user
#
@post('/users/')
def create_user(db):
    user = request.json

    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'username', 'email', 'password'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        user['username'] = execute(db, '''
            INSERT INTO users(username, email, password)
            VALUES(:username, :email, :password)
            ''', user)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/users/{user['username']}")
    return user

# Get a specific username's data
#
@get('/users/<username>')
def retrieve_user(username, db):
    user = query(db, 'SELECT * FROM users WHERE username = ?', [username], one=True)
    if not user:
        abort(404)

    return {'users': [user]}

# Add a follower
# 
@post('/users/<username>/followers/<usernameToFollow>')
def add_follower(db):
    user = request.json

    if not user:
        abort(400)

    posted_fields = user.keys()
    required_fields = {'username', 'email', 'password'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    try:
        user['username'] = execute(db, '''
            INSERT INTO users(username, email, password)
            VALUES(:username, :email, :password)
            ''', user)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    response.set_header('Location', f"/users/{user['username']}")
    return user

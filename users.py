# Users API
# CPSC 449: Project 2
# Creators: Stephen Lee, Scott Clary, Armando Lopez
# Date: 3/12/21
#

# imports
#
import sys
import textwrap
import sqlite3

import bottle
from bottle import get, post, delete, error, abort, request, response, HTTPResponse
from bottle.ext import sqlite

# Set up app and plugins
#
app = bottle.default_app()
app.config.load_config('./users.ini')

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
        <h1>Users API</h1>
    ''')

# Create a new user
#
@post('/users/')
def create_user(db):
    user = request.json

    # check if user is in json format
    if not user:
        abort(400, "User is not readable. Must be in json format.")

    # check if user has all required parameters
    posted_fields = user.keys()
    required_fields = {'username', 'email', 'password'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')

    # check if username or email is unique
    try:
        userid = execute(db, '''
            INSERT INTO users(username, email, password)
            VALUES(:username, :email, :password)
            ''', user)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    return {'message': "User created",
            'user': user}

# Check the password of a username
#
@get('/users/<username>/check/<password>')
def check_password(username, password, db):
    # check if username exists
    user = query(db, 'SELECT * FROM users WHERE username = ?', [username], one=True)
    if not user:
        abort(404, f"{username} is not a user.")
    
    # get the password
    pswd = query(db, 'SELECT password FROM users WHERE username = ?', [username], one=True)
    
    if pswd['password'] == password:
    	return {'message': "Password matches."}
    else:
    	return {'message': "Password does not match."}

# Add a follower
# 
@post('/users/<username>/followers/<usernameToFollow>')
def add_follower(username, usernameToFollow, db):
    # check if username exists
    user = query(db, 'SELECT * FROM users WHERE username = ?', [username], one=True)
    if not user:
        abort(404, f"{username} is not a user.")
    
    # check if username to follow exists
    find_userToFollow = query(db, 'SELECT * FROM users WHERE username = ?', [usernameToFollow], one=True)
    if not find_userToFollow:
    	abort(404, f"{username} is not a user.")
    
    try:
        follower = execute(db, '''
            INSERT INTO followers(username, usernameToFollow)
            VALUES(?, ?)
            ''', [username, usernameToFollow])
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    return {'message': "Follow successful.",
            'following': f"{usernameToFollow}"}

# Remove a follower
#
@delete('/users/<username>/followers/<usernameToRemove>')
def remove_follower(username, usernameToRemove, db):
    # check if username exists
    user = query(db, 'SELECT * FROM users WHERE username = ?', [username], one=True)
    if not user:
        abort(404, f"{username} is not a user.")
    
    # check if username to remove exists
    find_userToRemove = query(db, 'SELECT * FROM users WHERE username = ?', [usernameToRemove], one=True)
    if not find_userToRemove:
    	abort(404, f"{usernameToRemove} is not a user.")
    	
    # check if username is following the username to remove
    find_userToRemove = query(db, 'SELECT * FROM followers WHERE username = ? AND usernameToFollow = ?', [username, usernameToRemove], one=True)
    if not find_userToRemove:
    	abort(404, f"{username} is not following {usernameToRemove}.")
    
    # delete
    unfollowed = execute(db, '''
            DELETE FROM followers WHERE username = ? AND usernameToFollow = ?
            ''', [username, usernameToRemove])

    return {'message': "Deletion successful.",
            'unfollowed': f"{usernameToRemove}"}

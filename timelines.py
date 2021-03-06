# Timelines API
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
app.config.load_config('./timelines.ini')

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
# check author in db
@post('/timeline/')
def post_tweet(db):
    tweet = request.json

    # check if tweet is received
    if not tweet:
        abort(400, "Post must be a json format.")

    # check for required parameters for tweets
    posted_fields = tweet.keys()
    required_fields = {'author', 'text'}

    if not required_fields <= posted_fields:
        abort(400, f'Missing fields: {required_fields - posted_fields}')
    
    # check if username exists in users table
    user = query(db, 'SELECT * FROM users WHERE username = ?', [tweet['author']], one=True)
    if not user:
        abort(404, f"{author} is not a user.")

    try:
        timelineid = execute(db, '''
            INSERT INTO timelines(author, text)
            VALUES(:author, :text)
            ''', tweet)
    except sqlite3.IntegrityError as e:
        abort(409, str(e))

    response.status = 201
    return {"message": "Tweet created.",
            "tweet": tweet}

# Get Public Timeline
#
@get('/timeline/public/')
def public_timeline(db):
    ptl = query(db, 'SELECT * FROM timelines ORDER BY time DESC LIMIT 25') 

    # check if public timeline is not found
    if not ptl:
        abort(404, "Public timeline is not found.")

    return {"public_timeline": ptl}

# Get User Timeline
#
@get('/timeline/user/<username>')
def user_timeline(username, db):
    # check if username exists in users table
    user = query(db, 'SELECT * FROM users WHERE username = ?', [username], one=True)
    if not user:
        abort(404, f"{username} is not a user.")

    # get the user timeline
    utl = query(db, 'SELECT * FROM timelines WHERE author = ? ORDER BY time DESC LIMIT 25', [username])

    # check if user timeline is not found
    if not utl:
        abort(404, "User timeline is not found.")

    return {"user_timeline": utl}

# Get Home Timeline
#
@get('/timeline/home/<username>')
def home_timeline(username, db):
    # check if username exists in users table
    user = query(db, 'SELECT * FROM users WHERE username = ?', [username], one=True)
    if not user:
        abort(404, f"{username} is not a user.")
    
    # get followers
    follow_list = query(db, 'SELECT usernameToFollow FROM followers WHERE username = ?', [username])
    
    # convert list to string for sqlite query
    str_list = "("
    for ele in follow_list:
    	str_list += "'"
    	str_list += ele["usernameToFollow"]
    	str_list += "'"
    	str_list += ", "
    str_list += "'"
    str_list += username
    str_list += "')"
    
    # query string
    str_query = "SELECT * FROM timelines WHERE author IN " + str_list + " ORDER BY time DESC LIMIT 25"

    htl = query(db, str_query)

    # check if home timeline is not found
    if not htl:
        abort(404, "Home timeline is not found.")

    return {"home_timeline": htl}




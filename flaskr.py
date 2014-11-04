from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, g


#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


#create the tiny application
app = Flask(__name__)
app.config.from_object(__name__)

from views import *

app.add_url_rule('/', view_func=FlaskrView.as_view('index'))

app.add_url_rule('/add', view_func=AddEntry.as_view('add'))

app.add_url_rule('/login', view_func=Login.as_view('login'))

app.add_url_rule('/logout', view_func=Logout.as_view('logout'))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()


init_db()

if __name__ == '__main__':
    app.run()
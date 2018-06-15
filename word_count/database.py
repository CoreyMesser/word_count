import os
import sqlite3
from flask import Flask, g

#setting override ENV VAR
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'word_count.db'),
    SECRET_KEY='dev key',
))

app.config.from_envvar('WORD_COUNT', silent=True)


def connect_db():
    """connect db"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('word_count.sqlite.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initbd')
def initdb_command():
    """ini db"""
    init_db()
    print('Initialized the database.')


def get_db():
    """new db connect"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """closes db at end of request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

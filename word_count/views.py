import os
import sqlite3
from flask import Flask, render_template, g

from app import app

app = Flask(__name__)
app.config.from_object(__name__)

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


@app.route('/')
@app.route('/index')
def word_dict():
    db = get_db()
    line_n = 0
    words_l = []
    words_s = [] #split words
    words_d = {} #display words

    #open file
    with open('/Users/cmesser/Development/word_count/HRPG.txt', encoding='utf-8') as word_list:
        #split lines
        for a_line in word_list:
            line_n += 1
            line_s = words_l.append(a_line.rstrip())
            #  split words
            for a_word in a_line.split(' '):
                words_s.append(a_word)

        #  isolate words
        for w_word in words_s:
            if w_word not in words_d.keys():
                word_count = words_s.count(w_word)
                words_d.update({w_word: word_count})
            else:
                continue

    return render_template("index.html", words_d=words_d)
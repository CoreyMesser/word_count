from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user

from word_data.services import DatabaseServices

from word_data.main import app
from word_data.main.forms import LoginForm
from word_data.models import User

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'PibbleFiasco'}
    return render_template('index.html', user=user)

@app.route('/login',methods=['GET', 'POST'])
def login():
    ds = DatabaseServices()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = ds.get_user(username=form.username.data)
        if user is None or not User().check_password(password=form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template(url_for('login.html'), title='Sign In', form=form)

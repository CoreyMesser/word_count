from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from word_data.services import DatabaseServices

from word_data.main import app
from word_data.main.forms import LoginForm, RegistrationForm

from word_data.models import User

from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home')

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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template(url_for('login.html'), title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    ds = DatabaseServices()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        ds.add_commit(model=user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    ds = DatabaseServices()
    user = User.query.filter_by(username=username).first_or_404()
    titles = ds.get_titles(username=username)
    return render_template('user.html', user=user, titles=titles)
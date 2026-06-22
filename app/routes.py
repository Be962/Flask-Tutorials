from flask_login import current_user, login_user, logout_user
from app import db
from app.models import User
import sqlalchemy as sa
from flask import redirect, render_template, url_for, flash  
from app import app
from app.forms import LoginForm
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from app.forms import RegistrationForm

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/no_title')
def no_title():
    user = {'username': 'Moose'}
    return render_template('index.html', user=user)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'Cupcake'},
            'body': 'Mreow'
        },
        {
            'author': {'username': 'Tammy'},
            'body': 'Purrrr'
        },
        {
            'author': {'username': 'Coco'},
            'body': 'You know we are fake posts in a flask application, right?'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


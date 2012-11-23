'''
Flask's flaskr tutorial plus
'''
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort,\
        render_template, flash, app
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from flask.ext.pymongo import PyMongo

from flaskr import config
from flaskr.blueprints.entries import entries
from flaskr.models.user import User

app = Flask(__name__)
app.config.from_object(config)

mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return g.mongo.users.find_one({ 'username': userid })

app.register_blueprint(entries)

@app.before_request
def before_request():
    g.mongo = mongo.db

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db_user = g.mongo.users.find_one({ 'username': request.form['username'] })
        print db_user
        if not db_user:
            error = 'Invalid username'
        elif request.form['password'] != db_user.get('password', ''):
            error = 'Invalid password'
        else:
            user = User(db_user.get('username'), db_user.get('_id'))
            login_user(user)
            print user.is_authenticated()
            print current_user
            flash('You are logged in')
            return redirect(url_for('entries.list'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('entries.list'))


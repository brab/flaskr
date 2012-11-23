'''
Flask's flaskr tutorial plus
'''
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort,\
        render_template, flash, app
from flask.ext.admin import Admin
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from flask.ext.pymongo import PyMongo, ObjectId

from flaskr import config
from flaskr.blueprints.admin import UserView
from flaskr.blueprints.entries import entries
from flaskr.models.user import User

app = Flask(__name__)
app.config.from_object(config)

mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.setup_app(app)

admin = Admin(name='Flaskr')
admin.add_view(UserView(name='Users'))
admin.init_app(app)

@login_manager.user_loader
def load_user(userid):
    db_user = mongo.db.users.find_one({ '_id': ObjectId(str(userid)) })
    user = User(db_user)
    return user

app.register_blueprint(entries)

@app.before_request
def before_request():
    g.mongo = mongo.db

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db_user = g.mongo.users.find_one({
            'username': request.form['username'],
            })
        if db_user:
            user = User(db_user)
        else:
            user = None

        if not user:
            error = 'Invalid username'
        elif not user.check_password(request.form['password']):
            error = 'Invalid password'
        else:
            login_user(user)
            flash('You are logged in')
            return redirect(url_for('entries.list'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out')
    return redirect(url_for('entries.list'))


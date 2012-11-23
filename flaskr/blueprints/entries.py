from flask import Blueprint, request, session, g, redirect, url_for, abort,\
        render_template, flash
from flask.ext.login import current_user

entries = Blueprint('entries', __name__, template_folder='templates')

@entries.route('/')
def list():
    print current_user
    entries = g.mongo.entries.find()
    return render_template('show_entries.html', entries=entries)

@entries.route('/add', methods=['POST'])
def add():
    if not current_user.is_authenticated():
        abort(401)
    g.mongo.entries.save({
        'title': request.form['title'],
        'text': request.form['text'],
        })
    flash('New entry was successfully posted')
    return redirect(url_for('entries.list'))


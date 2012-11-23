from flask import Blueprint, request, session, g, redirect, url_for, abort,\
        render_template, flash
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.login import current_user

from flaskr.models.user import User

class UserView(BaseView):
    @expose('/')
    def index(self):
        users =  User.find_all()
        return self.render('admin/users/index.html', users=users)

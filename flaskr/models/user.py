from flask import g
from flask.ext.login import UserMixin 
from flask.ext.pymongo import ObjectId

class User(UserMixin):
    _password ='!'

    def __init__(self, user_dict):
        for key, val in user_dict.iteritems():
            setattr(self, key, val)

    def get_id(self):
        return self._id or self.id

    def check_password(self, password):
        if self.password == '!':
            return False
        return self.password == password

    @classmethod
    def find_all(cls):
        users = []
        for user in g.mongo.users.find():
            users.append(cls(user))
        return users

    @classmethod
    def find_one(cls, userid=None, username=None):
        if not id and not username:
            return None
        if userid:
            if type(userid) is not 'bson.objectid.ObjectId':
                userid = ObjectId(userid)
            db_user = g.mongo.users.find({ '_id': userid, })
        elif username:
            db_user = g.mongo.users.find({ 'username': username, })

        if not db_user:
            return None
        return cls(db_user)

from flask.ext.login import UserMixin 

class User(UserMixin):
    _password ='!'

    def __init__(self, username, id, active=True):
        self.id = id
        self.username = username
        self.active = active

    def check_password(self, password):
        return self._password == password

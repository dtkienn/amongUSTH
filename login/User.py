from flask_login import UserMixin
from login.mongo import User as mongo

class user_info(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        usr = mongo.get_db(user_id)
        if not usr:
            return None
        usr = user_info(
            id_=usr['UID'], name=usr['Fullname'], email=usr['Email'], profile_pic=usr['Profile_pic']
        )
        return usr

    @staticmethod
    def create(id_, name, email, profile_pic):
        mongo.register(id_, name, email, profile_pic)

    def getName(self):
        return self.name
    def getEmail(self):
        return self.email
    def getprofile_pic(self):
        return self.profile_pic
    def getid(self):
        return self.id_

class user_login(UserMixin):
    def __init__(self, id_, username, password):
        self.username = username
        self.password = password
        self.id = id_
        self.name = mongo.get_name(id_)
        self.email = mongo.get_email(id_)
        self.profile_pic = mongo.get_profile_pic(id_)

    def verify(self):
        mdict = mongo.login(self.username, self.password)
        if mdict:
            return True
        return False

    def getid(self):
        return self.id_
    def getName(self):
        return self.name
    def getEmail(self):
        return self.email
    def getprofile_pic(self):
        return self.profile_pic
    
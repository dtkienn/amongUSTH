from flask_login import UserMixin
from login.mongo import User_mongo as mongo

class user(UserMixin):
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
        usr = user(
            id_=usr['UID'], name=usr['Fullname'], email=usr['Email'], profile_pic=usr['Profile_pic']
        )
        return usr

    @staticmethod
    def create(id_, name, email, profile_pic):
        mongo.add_info_stu(id_, name, email, profile_pic)

    def getName(self):
        return self.name
    def getEmail(self):
        return self.email
    def getprofile_pic(self):
        return self.profile_pic
    def getid(self):
        return self.id_

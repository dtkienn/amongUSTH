from flask_login import UserMixin

from login.Db import get_db


class user(UserMixin):
    def __init__(self, id_, name, email, profile_pic=None):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        usr = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not usr:
            return None

        usr = user(
            id_=usr[0], name=usr[1], email=usr[2]#, profile_pic=user[3]
        )
        return usr

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic)"
            " VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()
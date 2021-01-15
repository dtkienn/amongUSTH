import pymongo
from login.User import user as usr
from flask_login import UserMixin

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")

# Create database for User
user = client['User']
u_info = user['User_info']
u_login = user['Login_info']
u_stu = user['Student']
u_lec = user['Lecturer']


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(id_, name, email, profile_pic):
        if u_info.find_one({'Email' : email}):
            print('Existed!')
            pass
        else: 
            mdict = {'UID' : id_, 'Fullname' : name, 'Email' : email, 'Profile_pic' : profile_pic}
            u_info.insert_one(mdict)

    def is_student(email):
        if ".bi" in email or '.ba' in email:
            print('Stuuu')
            return True
        else:
            print('Leccc')
            return False
    
    def add_info_stu(id_, usth_id, major, schoolYear):
        mdict = {'UID' : id_, 'USTH_ID' : usth_id, 'Major': major, 'SchoolYear' : schoolYear}
        u_stu.insert_one(mdict)

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

    def login(username,password):
        mdict = u_login.find_one({'UserName' : username}, {'UserName' :1,'Password' :1})
        print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"+str(mdict)+"/////////////////////////////////////////////////////////////////////////////////")
        if password == mdict["Password"]:
            return User(username, password)
        return None

    def add_info_lec(id_, department):
        mdict = {'UID' : id_, 'Department' : department}
        u_lec.insert_one(mdict)

    def add_login_info(id_, username, password):
        mdict = {'UID' : id_, 'UserName' : username,'Password' : password}  
        u_login.insert_one(mdict)

    def get_profile_pic(id_):
        mdict = u_info.find_one({'UID' : id_}, {'Profile_pic' : 1, '_id' : 0})
        return mdict['Profile_pic']

    def get_name(id_):
        mdict = u_info.find_one({'UID' : id_}, {'Fullname' : 1, '_id' : 0})
        return mdict['Fullname']

    def get_email(id_):
        mdict = u_info.find_one({'UID' : id_}, {'Email' : 1, '_id' : 0})
        return mdict['Email']

    def get_id(username):
        mdict = u_login.find_one({'Username' : username})
        return mdict['UID']

# class Login_info:
#     def login_info_register(id_, username, email, password, profile_pic):
#         if u_login.find_one({'Email' : email}):
#             print('Existed')
#             pass
#         else:
#             mdict = {'UID' : id_, 'UserName' : name, 'Email' : email, 'Password' : password, 'Profile_pic' : profile_pic}
#             u_login.insert_one(mdict)

#     def get_profile_pic(id_):
#         mdict = u_login.find_one({'UID' : id_}, {'Profile_pic' : 1, '_id' : 0})
#         return mdict['Profile_pic']

#     def get_name(id_):
#         mdict = u_login.find_one({'UID' : id_}, {'Fullname' : 1, '_id' : 0})
#         return mdict['Fullname']

#     def get_email(id_):
#         mdict = u_login.find_one({'UID' : id_}, {'Email' : 1, '_id' : 0})
#         return mdict['Email']

#     def get_id(username):
#         mdict = u_login.find_one({'Username' : username})
#         return mdict['UID']        
                
#         
import pymongo
from flask_login import UserMixin
import json

data = json.load(open('login\mongo.json'))
username = data['admin'][0]['username']
password = data['admin'][0]['password']
client = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")

# Create database for User
user = client['AmongUSTH']
u_info = user['User_info']
u_login = user['Login_info']
u_stu = user['Student']
u_lec = user['Lecturer']


class User():
    def register(id_,student_id, name, email, profile_pic):
        student_id = email.split(".")[1].split("@")[0]
        student_id.split(3)
        if u_info.find_one({'Email' : email}):
            print('Existed!')
            pass
        else: 
            mdict = {'UID' : id_, 'Student_ID' : student_id, 'Fullname' : name, 'Email' : email, 'Profile_pic' : profile_pic}
            u_info.insert_one(mdict)
            print('Created new user!')

    def is_registerd(id_):
        if u_login.find_one({'UID' : id_}):
            return True
        return False

    def add_major(id_, major):
        item = u_info.find_one({'UID' : id_})
        u_info.update_one(item, {'$set': {'major' : major}})

    def is_USTHer(email):
        if '@st.usth.edu.vn' in email:
            return 'Student'
        elif '@usth.edu.vn' in email:
            return 'Lecturer'
        else:
            return False

    
    # def add_info_stu(id_, usth_id, major, schoolYear):
    #     mdict = {'UID' : id_, 'USTH_ID' : usth_id, 'Major': major, 'SchoolYear' : schoolYear}
    #     u_stu.insert_one(mdict)


    def login(username,password):
        mdict = u_login.find_one({'UserName' : username}, {'UserName' :1,'Password' :1})
        print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"+str(mdict)+"/////////////////////////////////////////////////////////////////////////////////")
        if password == mdict["Password"]:
            return True
        return False

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
        mdict = u_login.find_one({'UserName' : username})
        return mdict['UID']
    
    def get_db(id_):
        mdict = u_info.find_one({'UID' : id_})
        return mdict

    def set_active(id_, status):
        if status == 'Active':
            return True
        return False

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
#         mdict = u_login.find_one({'UserName' : username})
#         return mdict['UID']        
                
#         
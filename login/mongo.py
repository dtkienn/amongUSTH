import pymongo
from login.User import user as usr
import json

dat = json.load(open('login\mongo.json'))
data = dat
username = data['read_write'][0]['username']
password = data['read_write'][0]['password']
client = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")

# Create database for User
user = client['User']
u_info = user['User_info']
u_login = user['Login_info']
u_stu = user['Student']
u_lec = user['Lecturer']


class User:
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

    def add_info_lec(id_, department):
        mdict = {'UID' : id_, 'Department' : department}
        u_lec.insert_one(mdict)

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

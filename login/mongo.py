import pymongo
#from login.User import User as usr
from flask_login import UserMixin
import json
import re

dat = json.load(open('login\mongo.json'))
data = dat
username = data['read_write'][0]['username']
password = data['read_write'][0]['password']
client = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
pymongo.MongoClient()

# Create database for User
user = client['AmongUSTH']
u_info = user['User_info']
u_login = user['Login_info']
u_stu = user['Student']
u_lec = user['Lecturer']
book_db = client['Book']
book  = book_db['Book_data']
interaction = client['Interact']
vote = interaction['Vote']
comment = interaction['Comment']

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(id_, name, email, profile_pic):
        student_id = email.split(".")[1].split("@")[0]
        student_id.split('3')
        if u_info.find_one({'Email' : email}):
            print('Existed!')
            pass
        else: 
            mdict = {'UID' : id_, 'Student_ID' : student_id, 'Fullname' : name, 'Email' : email, 'Profile_pic' : profile_pic}
            u_info.insert_one(mdict)

    def get(id_):
        return u_info.find_one({"UID": id_})

    def add_major(id_, major):
        item = u_info.find_one({'UID' : id_})
        u_info.update_one(item, {'$set': {'major' : major}})

    def is_USTHer(email):
        if re.match(r"[a-zA-Z\-\.1-9]+[@][s]?[t]?.?usth.edu.vn", email):
           return True
        return False
    
    def add_info_stu(id_, usth_id, major, schoolYear):
        mdict = {'UID' : id_, 'USTH_ID' : usth_id, 'Major': major, 'SchoolYear' : schoolYear}
        u_stu.insert_one(mdict)

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

class Book():
    def __init__(self, file_name, description):
        self.file_name = file_name
        self.description = description

    def post_book(id_, file_name, file, description):
        if book.find_one({'filename' : file_name}):
            print('Existed')
            pass
        else:
            mdict = {'_id' : id_, 'filename' : file_name, 'file' : file, 'description' : description}
            try:
                book.insert_one(mdict)
            except:
                print("Insert failed")

    def get_file_name(id_):
        mdict = book.find_one({'UID' : id_}, {'file_name' : 1, '_id' : 0})
        return mdict['filename']

    def get_file(id_):
        mdict = u_login.find_one({'UID' : id_}, {'file' : 1, '_id' : 0})
        return mdict['file']

    def get_description(id_):
        mdict = u_login.find_one({'UID' : id_}, {'description' : 1, '_id' : 0})
        return mdict['description']

class Vote():
    def __init__(self, up, down):
        self.up = up
        self.down = down

    def make_decision(_id, up, down):
        if vote.find_one({"_id" : _id}):
            print ("Existed")
            pass
        else :
            mdict = {'_id':id_,'up':up,'down':down}
            try:
                vote.insert_one(mdict)
            except:
                print("Insert failed")

    def get_up(id_):
        mdict = vote.find_one({'_id' : id_}, {'up' : 1, '_id' : 0})
        return mdict['up']

    def get_down(id_):
        mdict = vote.find_one({'_id' : id_}, {'down' : 1, '_id' : 0})
        return mdict['down']                        

class Comment():
    def __init__(self, content, user_id, comment_time,book_id):
        self.content = content
        self.user_id = user_id
        self.comment_time = comment_time
        self.book_id = book_id
    
    def post_comment(_id, user_id,book_id,content,comment_time):
        if comment.find_one({'content': user_id}):
            print('Existed')
            pass
        else :
            mdict = {'_id':id_,'book_id':book_id,'user_id':user_id,'content':content,'comment_time':comment_time}
            try:
                comment.insert_one(mdict)
            except:
                print("Insert failed")

    def get_content(id_):
        mdict = book.find_one({'_id' : id_}, {'content' : 1, '_id' : 0})
        return mdict['content']
    def get_file(id_):
        mdict = u_login.find_one({'UID' : id_}, {'file' : 1, '_id' : 0})
        return mdict['file']

    def get_description(id_):
        mdict = u_login.find_one({'UID' : id_}, {'description' : 1, '_id' : 0})
        return mdict['description'] 
    def get_comment_time(id_):
        mdict = u_login.find_one({'_id' : id_}, {'comment_time' : 1, '_id' : 0})
        return mdict['comment_time']

    def set_active(id_, status):
        if status == 'Active':
            return True
        return False

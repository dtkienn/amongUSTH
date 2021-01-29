from __future__ import print_function
import json
import os
from re import template
import sqlite3
from datetime import timedelta
import httplib2
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
# Third party libraries
from flask import Flask, render_template, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
import login.Db as logDb
import login.User as logUsr
from login.mongo import User as mongoUsr
from login.mongo import Book as mongoBook
from flask_bcrypt import Bcrypt
from forms.forms import Password,BookPost
# Configuration
import json

data = json.load(open('app_key.json'))
client_key = data['google_login'][0]['client_key']
client_secret = data['google_login'][0]['client_secret']
discovery_url = data['google_login'][0]['discovery_url']

GOOGLE_CLIENT_ID = client_key
GOOGLE_CLIENT_SECRET = client_secret
GOOGLE_DISCOVERY_URL = discovery_url

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template("login.html", display_navbar="none")


# Naive database setup
try:
    logDb.init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return logUsr.user.get(user_id)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import googledrive_api.auth as auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)
@app.route("/index")
def index():
    if current_user.is_authenticated:
        form = Password()
        id_ = user.get_id()
        name = mongoUsr.get_name(id_)
        email = mongoUsr.get_email(id_)
        profile_pic = mongoUsr.get_profile_pic(id_)
        first_Name = name.split(' ', 1)[0]
        print("Logged in")
        return render_template('profile.html', name=first_Name, email=email, picture=profile_pic, display_navbar="inline")

    else:
        print("Not logged in")
        return render_template("login.html", text="Login", display_noti="none", display_navbar="none", name="SIGN UP NOW!")


def generate_password():
    form = Password()
    hashed_password = str(bcrypt.generate_password_hash("123456").decode('utf-8'))[:8]
    id_ = user.get_id()
    email = mongoUsr.get_email(id_)
    username = email.split(".")[1].split("@")[0]
    profile_pic = mongoUsr.get_profile_pic(id_)
    mongoUsr.add_login_info(id_, username, hashed_password)

    print(hashed_password)
from flask_login import login_user
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #Find out what URL to hit for Google login
    if request.method=="POST" :
        username = request.form["username"]
        password = request.form["password"]
        user = mongoUsr.login(username, password)
        if user:
            # @login_manager.user_loader  
            # login_user(user)
            return redirect(url_for("index"))
        else:
            print("login failed")

        return redirect(url_for("index"))
        
    elif request.method == 'GET' :
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        print (request_uri)
        return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["name"]
        
        if mongoUsr.is_USTHer:
            # Add user information to Online database
            global user            
            user = logUsr.user_info(
                id_=unique_id, name=users_name, email=users_email, profile_pic=picture
            )
            id_ = user.get_id()
            name = user.getName()
            # temp = name.split()
            # name = temp[1] + ' ' + temp[2] + ' ' + temp[0]
            email = user.getEmail()
            profile_pic = user.getprofile_pic()
            mongoUsr.register(id_, name, email, profile_pic)
            generate_password()
            # Doesn't exist? Add to database
            if not user.get(unique_id):
                user.create(unique_id, users_name, users_email, picture)
                # Begin user session by logging the user in
            login_user(user)


            # Create session timeout
            time = timedelta(minutes=60)
            # User will automagically kicked from session after 'time'
            app.permanent_session_lifetime = time
            
            return redirect(url_for('index'))   
        else:
            return redirect(url_for('loginfail'))

      

@app.route('/loginfail')
def loginfail():
    return render_template('login.html', text="LOGIN FAILED :(", display_navbar="none", display_noti="block", loginNotiText="Login failed! The email address that you used is not a valid USTH Email")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    print('Logged out')
    return redirect(url_for("homepage"))

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/')
@app.route('/homepage')
def homepage():
    if current_user.is_authenticated:
        profile_pic = user.getprofile_pic()
        name = user.getName()
        first_Name = name.split(' ', 1)[0]
        return render_template("homepage.html", display_navbar="inline", picture=profile_pic, name=first_Name)

    else:
        return render_template("homepage.html", display_navbar="none", name='SIGN UP NOW!')


@app.route('/browse')
def browse():
    if current_user.is_authenticated:
        name = user.getName()
        profile_pic = user.getprofile_pic()
        first_Name = name.split(' ', 1)[0]

        return render_template("browse.html", display_navbar="inline", name=first_Name, picture=profile_pic)
    else:
        return render_template('login.html', text="You need to login!")


@app.route('/admin')
def admin():
    return render_template("admin.html", display_navbar="none", name="ADMIN")


@app.route('/content')
def content():
    if current_user.is_authenticated:
        name = user.getName()
        profile_pic = user.getprofile_pic()
        first_Name = name.split(' ', 1)[0]

        return render_template("content.html", display_navbar="inline", name=first_Name, picture=profile_pic)
    else:
        return render_template('login.html', text="You need to login!")

@app.route('/book',methods=['GET','POST'])
def new_book():
    form = BookPost()
    # if form.validate_on_submit():
        # book = Book(file_name=form.file_name.data,description=form.description.data,
        #     file=form.file.data,author=current_user)
    try:
        mongoBook.post_book("213123","form.file_name.data","form.file.data","form.description.data")
    except:
        print("insert failed")
    return render_template('homepage.html',title='Created Post')
    # return render_template('homepage.html',title='BookPost',form=form)
import cgi, os, cgitb, sys
import googledrive_api.main as main_drive

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
from pathlib import Path
from werkzeug.utils import secure_filename
# Path("C:/among_usth/upload").mkdir(parents=True, exist_ok=True)
@app.route('/upload',methods=["GET","POST"])
def upload():
    if request.method == "POST":
        if request.files:
            fileitem = request.files["book_upload"]
            filename = secure_filename(fileitem.filename)
            new_path = os.path.abspath(filename)
            uploadFile(filename=fileitem,filepath=new_path,mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            print('The file "' + fileitem + '"was uploaded successfully')
            return redirect(request.url)
    # cgitb.enable()
    # try:
    #     import msvcrt
    #     msvcrt.setmode(0, os.O_BINARY)
    #     msvcrt.setmode(1, os.O_BINARY)
    # except ImportError:
    #     pass
    # form = cgi.FieldStorage()
    # fileitem = form['filename']
    # if fileitem.filename:
    #     fn = os.path.basename(fileitem.filename)
    #     main_drive.uploadFile(filename=fileitem.filename,filepath=fn,mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    #     print('The file "' + fn + '"was uploaded successfully')
    # else:
    #     print('No file was uploaded')
    # # file = request.files['inputFile']
    return render_template('upload.html')

# @app.route('/uploads')
# def upFile():
#     return file.filename
    
if __name__ == '__main__':
    app.run(debug=True, ssl_context="adhoc")

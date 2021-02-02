import json
import os
from re import template
import sqlite3
from datetime import timedelta


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
import login.User as logUsr
from login.mongo import User as mongoUsr
from login.mongo import Book as mongoBook
from flask_bcrypt import Bcrypt
from forms.forms import Password,BookPost
from login.mail import gmail
from werkzeug.utils import secure_filename
# Configuration
import json

data = json.load(open('app_key.json'))
client_key = data['google_login'][0]['client_key']
client_secret = data['google_login'][0]['client_secret']
discovery_url = data['google_login'][0]['discovery_url']

GOOGLE_CLIENT_ID = client_key
GOOGLE_CLIENT_SECRET = client_secret
GOOGLE_DISCOVERY_URL = discovery_url

if not os.path.exists(os.getcwd() + "/fileseduocuploadvaoday"):
    try:
        os.mkdir("fileseduocuploadvaoday")
    except:
        print("can't create folder for download")
    

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["UPLOAD_FOLDER"] = os.getcwd() + "/fileseduocuploadvaoday"
app.config["MAX_CONTENT_PATH"] = 16 * 1024**2 # Maximize size of file

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template("login.html", display_navbar="none", text="You need to login!")



# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    print('loaded')
    return logUsr.user_info.get(user_id)


@app.route("/index")
def index():
    if current_user.is_authenticated:
        # form = Password()
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
    
    id_ = user.get_id()
    email = mongoUsr.get_email(id_)
    username = email.split(".")[1].split("@")[0]
    password = username
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    mongoUsr.add_login_info(id_, username, hashed_password)

    print(hashed_password)
from flask_login import login_user
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #Find out what URL to hit for Google login
    if request.method=="POST" :
        username = request.form["username"]
        password = request.form["password"]
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(hashed_password)
        usr_checked = mongoUsr.login(bcrypt, username, password)
        if usr_checked:
            # @login_manager.user_loader  
            global user
            global first_Name
            global profile_pic
            id_ = mongoUsr.get_id(usr_checked.username)
            user = logUsr.user_info.get(id_)
            name = mongoUsr.get_name(id_)
            first_Name = name.split(' ', 1)[0]
            profile_pic = mongoUsr.get_profile_pic(id_)
            login_user(user)
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
        
        if mongoUsr.is_USTHer(users_email):
            # Add user information to Online database
            global user            
            user = logUsr.user_info(
                id_=unique_id, name=users_name, email=users_email, profile_pic=picture
            )
            global profile_pic 
            global first_Name 
            id_ = user.getid()
            name = user.getName()
            email = user.getEmail()
            profile_pic = user.getprofile_pic()
            student_id = get_studentid(email)
            first_Name = name.split(' ', 1)[0]
            
            if not mongoUsr.account_existed(id_):
                mongoUsr.register(id_, name, email, student_id, profile_pic)
                generate_password()
                print('Generated login info!')
                gmail.send(email, get_studentid(email))
     
            login_user(user)


            # Create session timeout
            time = timedelta(minutes=60)
            # User will automagically kicked from session after 'time'
            app.permanent_session_lifetime = time
            
            return redirect(url_for('index'))   
        else:
            return redirect(url_for('loginfail'))

def get_studentid(email):
    student_id = email.split(".")[1].split("@")[0]
    student_id.split('3')
    return student_id

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
@login_required
def browse():
    return render_template("browse.html", display_navbar="inline", name=first_Name, picture=profile_pic)


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html", display_navbar="none", name="ADMIN")


@app.route('/content')
@login_required
def content():
    return render_template("content.html", display_navbar="inline", name=first_Name, picture=profile_pic)
    
@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', display_navbar="inline", name=first_Name, picture=profile_pic)

@app.route('/upload/get_file', methods = ['GET', 'POST'])
def get_file():
    if request.method == 'GET':
        return redirect(url_for('upload))
    elif request.method == 'POST':
        file = request.files["file"]
        file.save(os.path.join(app["UPLOAD_FOLDER], secure_filename(file.filename)))
        print(file.filename)
        ''' this is for temporary
          -> After this, we're gonna upload this file (with another thread) to server and delete this local file. Or we could just upload from the form to drive instead of save local file.
          Thanks! 
        '''
        print("successfully uploaded")
        return render_template('upload.html', display_navbar="inline", name=first_Name, picture=profile_pic)

if __name__ == '__main__':
    app.run(debug=True, ssl_context="adhoc")

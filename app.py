from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/homepage')
def homepage():
   return render_template("homepage.html")

@app.route('/login')
def login():
   return render_template("login.html")

@app.route('/all_discussion')
def all_discussion():
   return render_template("all_discussion.html")
if __name__ == '__main__':
   app.run(debug=True)

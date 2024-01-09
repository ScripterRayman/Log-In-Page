import os

from cs50 import SQL
from flask import Flask, render_template, request, session, redirect
from flask_session import Session

app = Flask(__name__)

db = SQL("sqlite:///logins.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

m = db.execute("SELECT * FROM logins")


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.form.get('signup'):
        return render_template('signup.html')
    elif request.form.get('login'):
        return render_template('login.html')


@app.route('/signup', methods = ["GET", "POST"])
def signup():
    session["firstname"] = request.form.get('firstname')
    session["lastname"] = request.form.get('lastname')
    session["username"] = request.form.get('username')
    session["password"] = request.form.get('password')
    session["dateofbirth"] = request.form.get('dateofbirth')
    session["emailadress"] = request.form.get('emailadress')

    if session["firstname"] and session["lastname"] and session["username"] and session["password"] and session["dateofbirth"] and session["emailadress"]:
        counts = db.execute("SELECT COUNT(ID) AS n FROM logins")
        session["id"] = int(counts[0]["n"]) + 1
        try:
            db.execute("INSERT INTO logins VALUES (?, ?, ?, ?, ?, ?, ?)", session["id"], session["firstname"], session["lastname"], session["username"], session["password"], session["dateofbirth"], session["emailadress"])
            m = db.execute("SELECT * FROM logins")
            return render_template('index.html', name=m[session["id"] - 1]["First Name"])
        except ValueError:
            return "The data you entered is already taken"
        except RuntimeError:
            return "You are not registered try again later"
    else:
        return "you are not signed up"


@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get('username')
        session["password"] = request.form.get('password')

        if m:
            if session["name"] and session["password"]:
                for i in range(len(m)):
                    if session["name"] == m[i]["Username"] and session["password"] == m[i]["Password"]:
                        session["id"] = m[i]["ID"]
                        session["firstname"] = m[i]["First Name"]
                        session["lastname"] = m[i]["Last Name"]
                        session["dateofbirth"] = m[i]["Date Of Birth"]
                        session["emailadress"] = m[i]["E-Mail Adress"]

                        return render_template('index.html', name=session["firstname"])
                else:
                    return "invalid Username or password"
            else:
                return "Missing Username or Password"
        else:
            return "No data fetched from database, Try again later"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session["id"] = None
    session["firstname"] = None
    session["lastname"] = None
    session["username"] = None
    session["password"] = None
    session["dateofbirth"] = None
    session["emailadress"] = None
    
    return redirect('/')

@app.route('/')
def index():
    if not session.get("username"):
        return render_template("register.html")
    return render_template("index.html", username=session["firstname"])

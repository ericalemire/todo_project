from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.task import Task
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ["post"])
def register():
    if User.validate_new_user(request.form):
        pass_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password" : pass_hash
        }
        user_in_db = User.get_by_email(data)
        if user_in_db:
            flash("Email is already in use!")
            return redirect("/")
        user_id = User.insert_user(data)
        session["user_id"] = user_id
        flash("New User Registered!")
        return redirect("/")
    else: 
        return redirect("/")

@app.route("/login", methods = ["post"])
def login():
    if User.validate_login(request.form):
        data = {
            "email" : request.form["email"]
        }
        user_in_db = User.get_by_email(data)
        if not user_in_db:
            flash("Invalid Email/Password")
            return redirect("/")
        if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
            flash("Invalid Email/Password")
            return redirect("/")

        session["user_id"] = user_in_db.id
        session["first_name"] = user_in_db.first_name
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("User must be logged in!")
        return redirect("/")
    else:
        data = {
        "id" : session["user_id"]
        }
        one_user_tasks = Task.users_tasks(data)
        return render_template("dashboard.html", one_user_tasks = one_user_tasks)

@app.route("/logout")
def logout():
    session.clear()
    flash("User logged out!")
    return redirect("/")
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.task import Task
from flask_app.controllers import users

@app.route("/addTask")
def addTask():
    if "user_id" not in session:
        flash("User must be logged in!")
        return redirect("/")
    return render_template("create.html")

@app.route("/insert_task", methods=["post"])
def insert_task():
    if not Task.validate_task(request.form):
        return redirect("/addTask")
    data = {
        "title" : request.form["title"],
        "due_date" : request.form["due_date"],
        "details" : request.form["details"],
        "user_id" : session["user_id"]
        }
    Task.insert_a_task(data)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit_task(id):
    if "user_id" not in session:
        flash("User must be logged in!")
        return redirect("/")
    data = {
        "id" : id
    }
    task = Task.get_one_task(data)
    return render_template("edit.html", task = task)

@app.route("/update/<int:id>", methods=["post"])
def update_task(id):
    if "user_id" not in session:
        flash("User must be logged in!")
        return redirect("/")
    if not Task.validate_task(request.form):
        return redirect(f"/edit/{id}")
    data = {
        "id" : id,
        "title" : request.form["title"],
        "due_date" : request.form["due_date"],
        "details" : request.form["details"], 
    }
    Task.update_task(data)
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete_task(id):
    if "user_id" not in session:
        flash("User must be logged in!")
        return redirect("/")
    data = {
        "id" : id
    }
    Task.delete_a_task(data)
    return redirect("/dashboard")
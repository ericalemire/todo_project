import imp
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.controllers import users
from flask_app.models.user import User

class Task:
    def __init__(self,data):
        self.id = data["id"]
        self.title = data["title"]
        self.due_date = data["due_date"]
        self.details = data["details"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def insert_a_task(cls, data):
        query = "INSERT INTO tasks (title, due_date, details, user_id) VALUES (%(title)s, %(due_date)s, %(details)s, %(user_id)s)"
        return connectToMySQL("todo_schema").query_db(query, data)

    @classmethod
    def users_tasks(cls, data):
        query = "SELECT * from users JOIN tasks ON users.id = tasks.user_id WHERE users.id = %(id)s"
        users_tasks_db = connectToMySQL("todo_schema").query_db(query, data)

        # ***COME BACK TO THIS - URGENT ***
        # if not users_tasks_db:
        # # create your user object as it should look with no tasks
        # user = func_to_deal_w_user_no_tasks()
        # else:

        user = User(users_tasks_db[0])

        for tasks in users_tasks_db:
            task_data = {
                "id" : tasks["tasks.id"],
                "title" : tasks["title"],
                "due_date" : tasks["due_date"],
                "details" : tasks["details"],
                "created_at" : tasks["created_at"],
                "updated_at" : tasks["updated_at"],
                "user_id" : tasks["user_id"]
            }
            user.tasks.append(Task(task_data))
            return user

    @classmethod
    def get_one_task(cls, data):
        query = "SELECT * FROM tasks WHERE tasks.id = %(id)s"
        task = connectToMySQL("todo_schema").query_db(query, data)
        return cls(task[0])

    @classmethod
    def update_task(cls,data):
        query = "UPDATE tasks SET title = %(title)s, due_date = %(due_date)s, details = %(details)s WHERE id = %(id)s"
        return connectToMySQL("todo_schema").query_db(query, data)

    @classmethod
    def delete_a_task(cls, data):
        query = "DELETE FROM tasks WHERE id = %(id)s"
        return connectToMySQL("todo_schema").query_db(query, data)

    @staticmethod
    def validate_task(data):
        is_valid = True
        if len(data["title"]) < 2:
            flash("Title must be at least 2 characters!")
            is_valid = False
        # add validation to ensure future due date!!
        return is_valid
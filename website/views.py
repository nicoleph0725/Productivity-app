from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json

main_views = Blueprint('main_views', __name__)

# Home Route
@main_views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

# Task page route
@main_views.route('/task_page', methods=['GET', 'POST'])
@login_required
def task_page():
    if request.method == 'POST':
        task = request.form.get('task')
        if len(task) < 1:
            flash('Task is too short', category='error')
        else:
            new_task = Task(description=task, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added', category='success')
    return render_template("task_page.html", user=current_user)


# For deleting tasks, if this is called the task page is returned normally
@main_views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})

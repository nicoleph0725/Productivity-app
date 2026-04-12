from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
from datetime import date, datetime, timedelta

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
        description = request.form.get('description')
        category = request.form.get('category')
        completed = False
        selected_date = request.form.get('task_due_date') # Get date from form

        if not selected_date:
            flash('Please select a date!', category='error')
        if len(description) < 1:
            flash('Task is too short', category='error')
        else:
            task_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            new_task = Task(description=description, category=category, completed=completed, task_due_date=task_date_obj, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added', category='success')

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    start_next_week = date.today() + timedelta(days=7)
    end_next_week = date.today() + timedelta(days=14)

    # Sort tasks by date so they appear in order
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.task_due_date.asc()).all()

    # Grouping logic
    grouped_tasks = {}
    for task in user_tasks:
        # Check if the task date is today
        if task.task_due_date == today:
            header = "Today"
        elif task.task_due_date < today:
            header = "Past"
        elif task.task_due_date == tomorrow:
            header = "Tomorrow"
        elif task.task_due_date < start_next_week:
            header = task.task_due_date.strftime('%A, %B %d')
        elif task.task_due_date > start_next_week and task.task_due_date < end_next_week:
             header = "Next week"
        else:
             header = "Future tasks"
        

        if header not in grouped_tasks:
            grouped_tasks[header] = []
        grouped_tasks[header].append(task)

    return render_template("task_page.html", user=current_user, grouped_tasks=grouped_tasks, today_date=today.isoformat())


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

import json
from datetime import date, datetime, timedelta

from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import current_user, login_required

from . import db
from .models import Task

main_views = Blueprint('main_views', __name__)


@main_views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)


@main_views.route('/task_page', methods=['GET', 'POST'])
@login_required
def task_page():
    if request.method == 'POST':
        description = request.form.get('description')
        category = request.form.get('category')
        completed = False
        selected_date = request.form.get('task_due_date')

        if not selected_date:
            flash('Please select a date!', category='error')
        if len(description) < 1:
            flash('Task is too short', category='error')
        else:
            task_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            new_task = Task(
                description=description,
                category=category,
                completed=completed,
                task_due_date=task_date_obj,
                user_id=current_user.id,
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task added', category='success')

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    start_next_week = date.today() + timedelta(days=7)
    end_next_week = date.today() + timedelta(days=14)

    user_tasks = (
        Task.query.filter_by(user_id=current_user.id)
        .order_by(Task.task_due_date.asc())
        .all()
    )

    grouped_tasks = {}
    for task in user_tasks:
        if task.completed:
            header = 'Completed'
        elif task.task_due_date == today:
            header = 'Today'
        elif task.task_due_date < today:
            header = 'Past'
        elif task.task_due_date == tomorrow:
            header = 'Tomorrow'
        elif task.task_due_date < start_next_week:
            header = task.task_due_date.strftime('%A, %B %d')
        elif start_next_week <= task.task_due_date < end_next_week:
            header = 'Next week'
        else:
            header = 'Future tasks'

        grouped_tasks.setdefault(header, []).append(task)

    return render_template(
        'task_page.html',
        user=current_user,
        grouped_tasks=grouped_tasks,
        today_date=today.isoformat(),
    )


@main_views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
    return jsonify({})


@main_views.route('/toggle-complete', methods=['POST'])
def toggle_complete():
    data = json.loads(request.data)
    task_id = data['taskId']

    task = Task.query.get(task_id)

    if task:
        task.completed = not task.completed
        db.session.commit()

    return jsonify({})


@main_views.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html', user=current_user)


@main_views.route('/get-tasks')
@login_required
def get_tasks():
    first_day_of_month = date.today().replace(day=1)
    tasks = (
        Task.query.filter(
            Task.user_id == current_user.id,
            Task.task_due_date >= first_day_of_month,
            Task.completed == False,
        )
        .order_by(Task.task_due_date.asc())
        .all()
    )

    events = [
        {
            'title': f'{task.category}: {task.description}',
            'start': task.task_due_date.isoformat(),
            'allDay': True,
            'extendedProps': {
                'category': task.category,
                'description': task.description,
            },
        }
        for task in tasks
    ]
    return jsonify(events)

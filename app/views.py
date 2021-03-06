from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort

from flask_login import login_user, logout_user, login_required, current_user

from .models import User, Task
from .forms import LoginForm, RegisterForm, TaskForm

from . import login_manager
from .consts import *

from .email import welcome_email

page = Blueprint('page', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404
    
@page.route('/')
def index():
    return render_template('index.html', title = 'Index')

@page.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))

    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate():
            user = User.create_element(form.username.data, form.password.data, form.email.data)
            flash(USER_CREATED)
            welcome_email(user)
            login_user(user)
            return redirect(url_for('.tasks'))
            #print('Successful user creation!')
            #print(user.id)
    return render_template('auth/register.html', title='Register', form=form,
                            active='register')

@page.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(LOGIN)
            return redirect(url_for('.tasks'))
            '''
            print(form.username.data)
            print(form.password.data)
            print('Nueva sesión creada!')
            '''
        else:
            flash(ERROR_USER_PASSWORD, 'error')

    return render_template('auth/login.html', title='Login', form=form,
                            active='login')

@page.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT)
    return redirect(url_for('.login'))

@page.route('/tasks')
@page.route('/tasks/<int:page>')
@login_required
def tasks(page=1, per_page=2):
    pagination = current_user.tasks.paginate(page, per_page=per_page)
    tasks = pagination.items
    return render_template('tasks/list.html', title='Tareas', tasks=tasks,
                            pagination=pagination, page=page, active='tasks')

@page.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task(): 
    form = TaskForm(request.form)
    
    if request.method == 'POST' and form.validate():
        task = Task.create_element(form.title.data, form.description.data, current_user.id)
        if task:
            flash(TASK_CREATED)

    return render_template('tasks/new.html', title='Nueva Tarea', form=form, 
                            active='new_task')

@page.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if current_user.id != task.user_id:
        abort(404)

    form = TaskForm(request.form, obj=task)
    if request.method == 'POST' and form.validate():
        task = Task.update_element(task.id, form.title.data, form.description.data)
        if task:
            flash(TASK_UPDATED)
    return render_template('tasks/edit.html', title='Editar Tarea', form=form)

@page.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if current_user.id != task.user_id:
        abort(404)
    
    if Task.delete_task(task.id):
        flash(TASK_DELETED)
    
    return redirect(url_for('.tasks'))

@page.route('/tasks/show/<int:task_id>')
def get_task(task_id):
    task = Task.query.get_or_404(task_id)

    return render_template('tasks/show.html', title='Tarea', task=task)
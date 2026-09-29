from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return redirect(url_for('views.login'))

@views_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return render_template('login.html')

@views_bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return render_template('register.html')

@views_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views_bp.route('/tasks')
@login_required
def tasks():
    return render_template('tasks.html', user=current_user)

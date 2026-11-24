from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to continue.', 'warning')
                return redirect(url_for('auth.login'))
            user_role = session.get('role')
            if user_role not in allowed_roles and user_role != 'Administrator':
                flash(f'Access denied. Role required: {", ".join(allowed_roles)}', 'danger')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please provide both username and password.', 'danger')
            return render_template('login.html')

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, username)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            session['email'] = user['email']
            flash(f"Welcome back, {user['full_name']}! Signed in as {user['role']}.", 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard.index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', 'Site Engineer')
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password or not full_name:
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'warning')
            return render_template('register.html')

        valid_roles = ['Administrator', 'Project Manager', 'Site Engineer', 'Inventory Manager']
        if role not in valid_roles:
            role = 'Site Engineer'

        conn = get_db_connection()
        existing = conn.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email)).fetchone()
        if existing:
            conn.close()
            flash('Username or email already registered. Please login.', 'warning')
            return render_template('register.html')

        pw_hash = generate_password_hash(password)
        conn.execute("""
        INSERT INTO users (username, email, password_hash, full_name, role, phone)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (username, email, pw_hash, full_name, role, phone))
        conn.commit()
        conn.close()

        flash('Registration successful! You may now sign in with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('public.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

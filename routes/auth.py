from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# Helper function to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Always show login form for GET requests (clicking login button)
    # Only redirect after successful POST authentication
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember')
        
        # Validation
        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return render_template('login.html')
        
        # Simple test credentials - just admin and user
        test_users = {
            'admin@gmail.com': {
                'password': 'admin123',
                'role': 'admin',
                'name': 'Admin User',
                'id': 'admin_001'
            },
            'user@gmail.com': {
                'password': 'user123',
                'role': 'user',
                'name': 'Test User',
                'id': 'user_001'
            }
        }
        
        # Check credentials
        if email in test_users and test_users[email]['password'] == password:
            user = test_users[email]
            
            # Set session variables
            session['user_id'] = user['id']
            session['user_email'] = email
            session['user_role'] = user['role']
            session['user_name'] = user['name']
            session['login_time'] = datetime.now().isoformat()
            
            # Set permanent session if remember me is checked
            if remember:
                session.permanent = True
            
            flash(f'Welcome back, {user["name"]}!', 'success')
            
            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password. Try admin@gmail.com/admin123 or user@gmail.com/user123', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        organization = request.form.get('organization', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms = request.form.get('terms')
        
        # Basic validation
        errors = []
        
        if not all([first_name, last_name, email, password, confirm_password]):
            errors.append('Please fill in all required fields.')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if not terms:
            errors.append('You must agree to the Terms of Service.')
        
        # Check if email already exists (for demo, just check test emails)
        if email in ['admin@gmail.com', 'user@gmail.com']:
            errors.append('An account with this email already exists.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # For demo purposes, just show success message
        flash('Registration successful! For demo, please use admin@gmail.com/admin123 or user@gmail.com/user123 to login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f'Goodbye {user_name}! You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

# Context processor to make user info available to all templates
@auth_bp.app_context_processor
def inject_auth():
    return {
        'current_user': {
            'is_authenticated': 'user_id' in session,
            'name': session.get('user_name', ''),
            'email': session.get('user_email', ''),
            'role': session.get('user_role', ''),
            'id': session.get('user_id', '')
        }
    }
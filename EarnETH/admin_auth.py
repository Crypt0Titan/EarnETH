from flask import Blueprint, redirect, url_for, flash, session
from functools import wraps

admin_auth = Blueprint('admin_auth', __name__)

# Admin required decorator to protect routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Please log in as admin to access this page.', 'error')
            return redirect(url_for('main.admin_login'))  # Ensure this points to the correct login route
        return f(*args, **kwargs)
    return decorated_function

# Admin logout route
@admin_auth.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)  # Clear the admin session
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.home'))  # Redirect to home after logout

from flask import Blueprint, render_template, redirect, url_for, flash, session  # Import session
from admin_auth import admin_required  # To protect admin routes
from forms import AdminLoginForm  # Import the login form
from models import Admin  # Import your Admin model
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)

# Home Route
@main.route('/')
def home():
    return render_template('home.html')

# Admin Main Route - Only accessible to logged-in admins
@main.route('/admin')
@admin_required  # Protect this route with the admin_required decorator
def admin_main():
    return render_template('admin_main.html')

# Admin Login Route - Handle login form and authentication
@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():  # When the form is submitted
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            # Set session for admin login
            session['admin'] = True
            flash('Logged in successfully as admin', 'success')
            return redirect(url_for('main.admin_main'))  # Redirect to admin main page
        else:
            flash('Invalid username or password', 'danger')  # Flash error message

    return render_template('admin_login.html', form=form)

# Rewards Page Route
@main.route('/rewards')
def rewards():
    return render_template('rewards.html')

# ============================
# Error Handling Routes
# ============================
@main.app_errorhandler(404)
def page_not_found(e):
    """Handles 404 errors."""
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(e):
    """Handles 500 errors."""
    return render_template('500.html'), 500

# ============================
# Utility Routes (Optional)
# ============================
@main.route('/redirect_example')
def redirect_example():
    """Example of a route redirect."""
    return redirect(url_for('main.home'))  # Redirects to the home page

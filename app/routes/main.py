from flask import Blueprint, render_template, send_from_directory, current_app, request, redirect, url_for
import os
import numpy as np
from flask import session



main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Ensure the upload folder exists and return the file
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_folder, filename)

@main_bp.route('/results/<path:filename>')
def result_file(filename):
    # Ensure the result folder exists and return the file
    result_folder = current_app.config.get('RESULT_FOLDER', 'results')
    return send_from_directory(result_folder, filename)



@main_bp.route('/download-report')
def download_report():
    report_folder = os.path.join(current_app.root_path, 'static/report')
    report_filename = 'report.csv'  
    if not os.path.exists(os.path.join(report_folder, report_filename)):
        from flask import abort
        abort(404, description="Report not found.")
    return send_from_directory(report_folder, report_filename, as_attachment=True)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            session['user'] = email  # Set session
            return redirect(url_for('main.home'))
        return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Here you would normally save the user info
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        # Save user logic here...
        # After signup, redirect to login page
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))
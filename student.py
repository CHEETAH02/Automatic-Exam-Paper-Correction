from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps

student = Blueprint('student', __name__)

# To be put between every route decorator and function if student/teacher logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student_login_page"))
    return decorated_func

@student.route("/homePage")
@logged_in
def student_home_page():
    return render_template('student_home_page.html')
from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps

teacher = Blueprint('teacher', __name__)

# To be put between every route decorator and function if teacher logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("teacher_login"))
    return decorated_func

@teacher.route("/homePage")
@logged_in
def teacher_home_page():
    return render_template('teacher_home_page.html')
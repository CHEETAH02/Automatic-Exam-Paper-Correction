from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps
from app import db

admin = Blueprint('admin', __name__)

# To be put between every route decorator and function if admin logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("admin_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("admin_login"))
    return decorated_func


@admin.route("/homePage")
@logged_in
def admin_home_page():
    return render_template('admin_home_page.html')

@admin.route("/addTeacher", methods=['GET', 'POST'])
@logged_in
def add_teacher():
    if request.method == 'POST':
        form = request.form
        teacherID = form['teacher_id']
        teacherName = form['teacher_name']
        teacherPassword = form['teacher_pwd']
        if db.teachers.find_one({"teacherID": teacherID}):
            return render_template("exists.html", person='Teacher')
        db.teachers.insert_one({"teacherID": teacherID, "teacherName": teacherName, "teacherPassword": teacherPassword})
        return redirect(url_for("teacher_login"))
    return render_template("admin_add_teacher.html")

@admin.route("/checkAll")
@logged_in
def check_all():
    students_list = []
    for student in db.students.find({}):
        students_list.append((student['studentID'], student['studentName']))

    teachers_list = []
    for teacher in db.teachers.find({}):
        teachers_list.append((teacher['teacherID'], teacher['teacherName']))
    
    tests_list = []
    for test in db.question_papers.find({}):
        tests_list.append((test['questionPaperID'], test['questionPaperName']))


    return render_template("admin_check_all.html", teachers=teachers_list, students=students_list, tests=tests_list)
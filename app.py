from flask import Flask, render_template, request, session, redirect, url_for
from flask_mail import Mail, Message
import os
from db import db
from student import student
from paper import paper
from teacher import teacher
from admin import admin

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_KEY')

app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(teacher, url_prefix="/teacher")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(paper, url_prefix="/paper")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
@app.route("/home")
def home():
    if session.get('studentID'):
        return redirect("/student/homePage")
    if session.get('teacherID'):
        return redirect("/teacher/homePage")
    return render_template("index.html")


@app.route("/studentRegister", methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':

        data = request.form
        studentID = data['student_id']
        studentName = data['student_name']
        studentEmail = data['student_email']
        studentPassword = data['student_pwd']

        if db.students.find_one({"studentID": studentID}):
            return render_template("exists.html", person="Student")

        dict = {
            "studentID": studentID,
            "studentName": studentName,
            "studentEmail": studentEmail,
            "studentPassword": studentPassword
        }

        db.students.insert_one(dict)
        return render_template("student_login.html")

    return render_template('student_register.html')


@app.route("/studentLogin", methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':

        data = request.form
        studentID = data['student_id']
        studentPassword = data['student_pwd']

        if db.students.find_one({"studentID": studentID, "studentPassword": studentPassword}):
            session['student_logged_in'] = True
            session['studentID'] = studentID
            return redirect("/student/homePage")
        return render_template('not_exists.html', person='Student')

    return render_template('student_login.html')


@app.route("/teacherLogin", methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':

        data = request.form
        teacherID = data['teacher_id']
        teacherPassword = data['teacher_pwd']

        if db.teachers.find_one({"teacherID": teacherID, "teacherPassword": teacherPassword}):
            session['teacher_logged_in'] = True
            session['teacherID'] = teacherID
            return redirect(url_for('teacher.teacher_home_page'))
        return render_template('not_exists.html', person='Teacher')

    return render_template('teacher_login.html')

@app.route("/adminLogin", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.form
        adminID = data['admin_id']
        adminPassword = data['admin_pwd']

        if db.admins.find_one({"adminID": adminID, "adminPassword": adminPassword}):
            session['admin_logged_in'] = True
            session['adminID'] = adminID
            return redirect(url_for('admin.admin_home_page'))
        return render_template('not_exists.html', person='Admin')
    return render_template("admin_login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/sendMail")
def create_mail():
    data = request.args

    paperID = data.get('paperID')
    paperName = data.get('paperName')
    studentList = data.get('studentList').split(',')

    msg = Message(f"Paper {paperName} ({paperID}) has been Corrected",
                  sender='chetansathish02@gmail.com', recipients=studentList)
    msg.body = f"The Paper {paperName} has been corrected. You may check your score (http://127.0.0.1:5000/student/viewScores).\n\nThis mail is automated. Replies to this mail may not be checked."
    mail.send(msg)

    return render_template("teacher_test_corrected.html")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
    
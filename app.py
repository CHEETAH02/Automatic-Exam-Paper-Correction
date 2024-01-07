from flask import Flask, render_template, request, session, redirect, url_for
from pymongo.mongo_client import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_KEY')
#app.secret_key = 'YOUR_SESSION_KEY'

username = 'AEPC_user'
password = os.environ.get('DB_PASSWORD')
# password = 'YOUR_MONGODB_PASSWORD'
uri = "mongodb+srv://%s:%s@cluster0.3fajycc.mongodb.net/?retryWrites=true&w=majority" % (
    username, password)
client = MongoClient(uri)
db = client['AutoExamPaperCorrection']


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
        studentPassword = data['student_pwd']

        if db.students.find_one({"studentID": studentID}):
            return render_template("exists.html", person="Student")

        dict = {
            "studentID": studentID,
            "studentName": studentName,
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
            return redirect(url_for('student.student_home_page'))
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


if __name__ == "__main__":
    from student import student
    from teacher import teacher
    from admin import admin
    from test import test
    app.register_blueprint(student, url_prefix="/student")
    app.register_blueprint(teacher, url_prefix="/teacher")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(test, url_prefix="/test")

    app.run(debug=True)

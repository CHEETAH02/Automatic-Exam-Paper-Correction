from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from student import student

app = Flask(__name__)
app.register_blueprint(student, url_prefix="/student")

client = PyMongo(app, uri="mongodb://localhost:27017/AutoExamPaperCorrection")
db = client.db
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/TeacherLoginPage")
def teacher_login_page():
    return render_template("teacher_login.html")

@app.route("/StudentLoginPage")
def student_login_page():
    return render_template("student_login.html")

@app.route("/StudentRegisterPage")
def student_registration_page():
    return render_template("student_registration.html")

@app.route("/StudentRegistrationPage", methods=['POST'])
def student_registration():
    data = request.form
    studentID = data['student_id']
    studentName = data['student_name']
    studentPassword = data['student_pwd']

    if db.students.find_one({"id": studentID}):
        return render_template("student_exists.html")

    dict = {
        "id": studentID,
        "name": studentName,
        "password": studentPassword
    }

    db.students.insert_one(dict)
    return render_template("student_login.html")

@app.route("/studentLoginAuth", methods=['POST'])
def student_login_authentication():
    data = request.form
    studentID = data['student_id']
    studentPassword = data['student_pwd']

    if db.students.find_one({"id": studentID, "password": studentPassword}):
        session['logged_in'] = True
        session['student'] = studentID
        return redirect(url_for('student.student_home_page'))
    return render_template('student_not_exists.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from student import student
from teacher import teacher

app = Flask(__name__)
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(teacher, url_prefix="/teacher")

client = PyMongo(app, uri="mongodb://localhost:27017/AutoExamPaperCorrection")
db = client.db
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/studentRegister", methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':

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
    
    return render_template('student_register.html')

@app.route("/studentLogin", methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':

        data = request.form
        studentID = data['student_id']
        studentPassword = data['student_pwd']

        if db.students.find_one({"id": studentID, "password": studentPassword}):
            session['logged_in'] = True
            session['student'] = studentID
            return redirect(url_for('student.student_home_page'))
        return render_template('student_not_exists.html')
    
    return render_template('student_login.html')

@app.route("/teacherLogin", methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':

        data = request.form
        teacherID = data['teacher_id']
        teacherPassword = data['teacher_pwd']

        if db.teachers.find_one({"id": teacherID, "password": teacherPassword}):
            session['logged_in'] = True
            session['teacher'] = teacherID
            return redirect(url_for('teacher.teacher_home_page'))
        return render_template('teacher_not_exists.html')
    
    return render_template('teacher_login.html')

if __name__ == "__main__":
    app.run(debug=True)